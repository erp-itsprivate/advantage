import frappe
from frappe.utils import get_url_to_form

def execute(filters=None):
    filters = frappe._dict(filters or {})
    #filters.meeting= frappe.get_doc('Meeting',{'closed':False}).meet_name
    columns = get_columns(filters)
    data = get_data(filters)
    #data=[]
    #columns =[]
    #data.append({"Shareholdernn":"ahmad","b_party":"ll"})
   #tr_date <= %(trx_date)s
    return columns, data

def get_conditions(filters):
    conditions = {}
    #current_day=frappe.utils.nowdate()
    #conditions="where cast(ts.creation as date) >= cast('"+current_day+"' as Date) and cast(ts.creation as date) <= cast('"+current_day+"' as Date)"
    #conditions="where 1=1 "
    conditions.update({'lead':filters.get("lead")})
    # if filters.get("status") is not None:
    #     if filters.get("status") != "All":
    #     #conditions["status"] = filters.status
    #     #return conditions
    #         conditions += "and  srv_status  =  %(status)s "
    # if filters.get("from_service_creation"):
    #     conditions += "and  cast(ts.creation as date)  >=  cast(%(from_service_creation)s as date) "
    
    # if filters.get("to_service_creation"):
    #     conditions += "and  cast(ts.creation as date)  <=  cast(%(to_service_creation)s as date) "
    return conditions
	

def get_columns(filters):
    columns = [
           {
            "label": "Email/Call",
            "fieldtype": "Data",
            "fieldname": "rec_type",
            
            "width": 100,
        },
          {
            "label": "Type",
            "fieldtype": "Data",
            "fieldname": "type",
            
            "width": 100,
        },
        {
            "label": "From",
            "fieldtype": "Data",
            "fieldname": "from",
         
            "width": 250,
        },
         {
            "label": "To",
            "fieldtype": "Data",
            
            "fieldname": "to",
         
            "width":250,
        }, 
       
        
           {
            "label": "Date",
            "fieldtype": "Datetime",
           
            "fieldname": "creation",
         
            "width":200,
        }, 
        {
            "label": "Subject",
            "fieldtype": "Data",
           
            "fieldname": "subject",
         
            "width":100,
        }, 
			{
			"label": "Link",
			"fieldname": "tracking_url_html",
			"fieldtype": "Data", 
			"width": 50
		}
    
        
         
    ]

    return columns

 

def get_data(filters):
		data = []
		conditions = get_conditions(filters)
		lead=conditions.get('lead')
		if lead is not None and lead != "" :
			lead_doc=frappe.get_doc('Lead',lead)
			values = {'email': '',  'lead_name':lead_doc.name,'company':lead_doc.company}
			if lead_doc.email_id is not None and lead_doc.email_id != "":
				values.update({'email': '%'+lead_doc.email_id+'%'})
			 
			if lead_doc.mobile_no is not None and lead_doc.mobile_no != '':
				values.update({'mobile_no': lead_doc.mobile_no})
			phone=lead_doc.phone or lead_doc.mobile_no
			 
			values.update({'phone': phone})
				#STR_TO_DATE(cdr_time, "%d/%m/%Y %H:%M:%S")
			result=frappe.db.sql("""

			select B.sent_or_received,B.sender,B.creation,B.recipients,B.subject,B.name,'email' rec_type from  `tabCommunication` B  
			where B.communication_medium='Email' and  (B.recipients like  %(email)s
			or B.sender like  %(email)s )
			and B.company =%(company)s
			union all 
			select call_type,call_from_name ,STR_TO_DATE(cdr_time, '%%d/%%m/%%Y %%H:%%i:%%s')  creation,call_to_name ,'' ,name,'call' from `tabPBX CDRs` 
				where call_to_number = %(mobile_no)s  or  call_from_number = %(mobile_no)s 
					or call_from_number=  %(phone)s or call_to_number=  %(phone)s             
			order by creation desc
			""",values=values, as_dict=1)



			for d in result:
				
				#row = {"shareholder": d['name'] ,"shareholdername":d['full_name'],"nationality":d["nationality"] ,"type":d["type"] ,
				#"tranasction": d["transaction_type"],"volume":d["volume"],"price":d["price"],"date":d["tr_date"]
				
				
				#}
				



				row = { "type":d.sent_or_received,"from":d.sender,"to":d.recipients ,"creation":d.creation,"starts_on":d.starts_on ,"subject":d.subject,
					"rec_type":d.rec_type
				
				}
				if (d.rec_type == "email"):
					url = get_url_to_form("Communication", d.name)
					html_link = f"<a href='{url}' target='_blank'> Email </a>"
				
				else:
					url = get_url_to_form("PBX CDRs", d.name)
					html_link = f"<a href='{url}' target='_blank'> Call </a>"
				row.update({"tracking_url_html":html_link})
				data.append(row)

		return data
