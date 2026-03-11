#from __future__ import annotations  # 1. Postpones evaluation of types
#from typing import TYPE_CHECKING
import frappe
import re,json
from frappe.cache_manager import clear_controller_cache, clear_user_cache
from advantage.utils import get_detailed_connections,get_lead_phone_numbers,format_datetime,show_how_old


#if TYPE_CHECKING:
from yealink.yealink.doctype.pbx_cdrs.pbx_cdrs import get_phone_cdrs,get_phone_cdrs_by_cdrid
no_cache = 1

logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)


def get_context(context):
     try:          		
        clear_user_cache(frappe.session.user)
     
        #context.update({"activites_data":{"calls":combine_email_with_cdr('CRM-LEAD-2025-00001')}})
        return context
     except Exception as e :
         
            frappe.log_error(message=f"  file => scale.py page method =>  get_context  for context {context} {frappe.get_traceback()} ", title="Advantage Page") 
@frappe.whitelist()
def get_lead_info(lead):
    try:
        
        events = render_event(lead)
        products = render_products(lead)
        issues = render_issues(lead)
        notes =  render_notes(lead)
        opportunities = str(frappe.render_template("templates/includes/opportunities_section.html", {'template_data':{"data":get_opportunities(lead,6)}}))
        maintenance = str(frappe.render_template("templates/includes/maintenance_section.html", {'template_data':{"data":get_maintenance(lead,6)}}))
        critical_notes=str(frappe.render_template("templates/includes/critical_lead_notes.html", {'template_data':get_critical_notes(lead)}))
        activites=combine_email_with_cdr(lead)
        activities_section=None
        if activites is not None:
            activities_section=str(frappe.render_template("templates/includes/activities_section.html",{"template_data":{"lead":lead,"num_of_data":len(activites),"calls":activites}}))
        lead=frappe.get_doc('Lead',lead).as_dict()
        if (frappe.db.exists('User',lead.get("lead_owner"))):
            lead.update({"lead_owner":frappe.get_doc("User",lead.get("lead_owner")).username})
        customer=None
        if (frappe.db.exists('Customer',{"lead_name":lead.name})):
            customer=frappe.get_doc('Customer',{"lead_name":lead.name})
        return events,products,issues,notes,lead,opportunities,maintenance,customer,critical_notes,activities_section
    except Exception as e :
            logger_exception.error(f" file => advantage page.py get_lead_info lead {lead}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage page.py get_lead_info lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


@frappe.whitelist()
def make_opportunity(source_name, target_doc=None):
    from erpnext.crm.doctype.lead.lead import _set_missing_values
    from frappe.model.mapper import get_mapped_doc
    def set_missing_values(source, target):
        _set_missing_values(source, target)
    target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{
			"Lead": {
				"doctype": "Opportunity",
				"field_map": {
					"doctype": "opportunity_from",
					"name": "party_name",
					"lead_name": "contact_display",
					"company_name": "customer_name",
					"email_id": "contact_email",
					"mobile_no": "contact_mobile",
					"lead_owner": "opportunity_owner",
					"notes": "notes",
				},
			}
		},
		target_doc,
		set_missing_values,
	    )
    connections=get_detailed_connections(source_name)
    if len(connections.get('customer')) > 0 :
        customer=frappe.get_doc('Customer',connections.get('customer')[0])
        target_doc.update({"opportunity_from":"Customer","contact_display":customer.customer_name})
    return target_doc

def get_critical_notes(lead):
    try:
        if frappe.has_permission('Critical Lead Notes', "read"):
            critical_notes=frappe.get_all('Critical Lead Notes',fields=['name'],order_by='creation desc',filters=[['lead','=', lead],['disable','=','0'],['creation','>=',frappe.utils.get_datetime()]],limit=1,pluck='name')
            if (critical_notes is not None and len(critical_notes) > 0):
                return frappe.get_all('Critical Lead Notes',filters=[['name','in',critical_notes]],fields=['note'])[0]
            else:
                return []
        else:
            return []
    except Exception as e :
            logger_exception.error(f" file => advantage page.py get_critical_notes lead {lead}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage page.py get_critical_notes lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


def get_opportunities(lead,limit):
    if frappe.has_permission('Opportunity', "read"):
        return frappe.get_all('Opportunity', filters=[['party_name','=',lead]],fields=['creation','probability','opportunity_type','name','status','owner'],order_by='creation DESC',limit=limit)

@frappe.whitelist()
def render_products(lead):
    # from frappe.utils import get_datetime
    # data=json.loads(data_)	
    # lead_name=frappe.get_list('Lead',filters=[['name','=',lead]])[0]
    # lead_doc=frappe.get_doc('Lead',lead_name.name)
    # lead_doc.append("custom_products", { "product_name": data.get("product"), "buy_date": get_datetime(data.get("buy_date")), "is_company_brand": data.get("company_product") }) # Save changes doc.save()
    # lead_doc.save()
    # frappe.db.commit()
    try:
        limit=frappe.get_single('Advantage Page Settings').num_of_products or 0
        if limit > 0:
            data=get_products(lead,[],limit)
            if data is not None :
                return  str(frappe.render_template("templates/includes/product_section.html", {'template_data':{"lead":lead,"data":data,"num_of_data":len(data)}}))
    except Exception as e :
            logger_exception.error(f" file => advantage page.py render_products lead {lead}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage page.py render_products lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  



@frappe.whitelist()
def render_issues(lead):
    try:
        limit=frappe.get_single('Advantage Page Settings').num_of_issues or 0
        if limit > 0:
            data=get_issues(lead,['name','creation','description','status'],limit)
            if data is not None   :
                return  str(frappe.render_template("templates/includes/issue_section.html", {'template_data':{"lead":lead,"data":data,"num_of_data":len(data)}}))
    except Exception as e :
            logger_exception.error(f" file => advantage page.py render_issues lead {lead}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage page.py render_issues lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


@frappe.whitelist()
def render_notes(lead):
    try:
        limit=frappe.get_single('Advantage Page Settings').num_of_notes or 0
        if limit > 0:
            data=get_notes(lead,['owner','note','parent','added_on','parenttype'],limit)
            if data is not None   :
                return   str(frappe.render_template("templates/includes/note_section.html", {'template_data':{"lead":lead,"data":data,"num_of_data":len(data)}}))  
    except Exception as e :
            logger_exception.error(f" file => advantage page.py render_notes lead {lead}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage page.py render_notes lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


@frappe.whitelist()
def render_event(lead):
    try: 
        limit=frappe.get_single('Advantage Page Settings').num_of_events or 0
        if limit > 0:
            data=get_events(lead,['subject','status','name','creation'],limit)
            if data is not None   :
                return  str(frappe.render_template("templates/includes/event_section.html", {'template_data':{"lead":lead,"data":data,"num_of_data":len(data)}}))
    except Exception as e :
            logger_exception.error(f" file => advantage page.py render_event lead {lead}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage page.py render_event lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


def get_events(lead,fields,limit):
    try:
        
        connections=get_detailed_connections(lead)
        event_participants=[]
        event_participants.append(frappe.get_all('Event Participants', filters=[["reference_doctype",'=','Lead'],['reference_docname','=',lead]],fields=['parent']))
        if len(connections.get('prospects')) > 0 :
            event_participants.append(frappe.get_all('Event Participants', filters=[["reference_doctype",'=','Prospect'],['reference_docname','in',connections.get('prospects')]],fields=['parent']))
        if len(connections.get('opportunities')) > 0 :
            event_participants.append(frappe.get_all('Event Participants', filters=[["reference_doctype",'=','Opportunity'],['reference_docname','in',connections.get('opportunities')]],fields=['parent']))
        event_names =  [d.get('parent') for sublist in event_participants for d in sublist]
        #frappe.get_all('ToDo', filters=[["reference_type",'=','Event'],['reference_name','in',event_names]],fields=['allocated_to,reference_name'])
        events= frappe.get_all('Event',filters=[['name','in',event_names]],fields=fields,limit=limit)
        event_owner=frappe.get_all('ToDo', filters=[["reference_type",'=','Event'],['reference_name','in',event_names]],fields=['allocated_to','reference_name'])
        
        alloc_map = {} 
        for a in event_owner: 
            alloc_map.setdefault(a['reference_name'], []).append(a['allocated_to'])
        for e in events: 
            e['allocated_users'] = alloc_map.get(e['name'], [])
        #lookup = {item['reference_name']: item['allocated_to'] for item in event_owner}
        #for entry in events:                
        #    if entry['name'] in lookup:
        #        entry['allocated_to'] = lookup[entry['name']]
        ordered = sorted(events, key=lambda x: x['creation'],reverse=True)
        return ordered
    except Exception as e :
            logger_exception.error(f" file => advantage page.py get_events lead {lead}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage page.py get_events lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


def get_maintenance(lead,limit):
    try:
        connections=get_detailed_connections(lead)
        maintenances=[]
        if len(connections.get('customer')) > 0 :
                if frappe.has_permission("Maintenance Visit", "read"):
                    pre_data=frappe.get_list('Maintenance Visit', filters=[['customer','in',connections.get('customer')]],pluck='name',limit=limit)
                else:
                    pre_data=[]
                all_fields=['name','maintenance_type','completion_status','mntc_date','creation']

                data=frappe.get_all('Maintenance Visit', filters=[['name','in',pre_data]],fields=all_fields)
                maintenances.append(data)
                flat_list = [obj for sublist in maintenances for obj in sublist]
        
                ordered = sorted(flat_list, key=lambda x: x['creation'],reverse=True)
                return ordered
        else:
            return maintenances
    except Exception as e :
        logger_exception.error(f" file => advantage page.py get_maintenance lead {lead}  {frappe.get_traceback()} ")
        frappe.log_error(message= f" file => advantage page.py get_maintenance lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  

  
def get_products(lead,fields,limit):
    try:
        connections=get_detailed_connections(lead)
        products=[]
        pre_data=frappe.get_all('Advantage Products', filters=[['parent','=',lead]],pluck='name',limit=limit)
        pre_fields=['product_name','buy_date']
        meta = frappe.get_meta("Advantage Products")
        doctype_fields=[item.fieldname for item in meta.fields]
        filtered = [item for item in fields if item in doctype_fields] 
        all_fields = pre_fields + filtered
        
        

        data=frappe.get_all('Advantage Products', filters=[['name','in',pre_data]],fields=all_fields)
        for item in data: 
            item['subject'] = 'Owns'
            item['item'] =item.pop('product_name')
            item['creation'] =item.pop('buy_date')
            item['link']="lead/"+lead
        products.append(data)
        if len(connections.get('opportunities')) > 0 :
                pre_data=frappe.get_all('Opportunity Item', filters=[["parenttype",'=','Opportunity'],['parent','in',connections.get('opportunities')]],pluck='name',limit=limit)
                pre_fields=['item_name','creation','parent']
            
                meta = frappe.get_meta("Opportunity Item")
                doctype_fields=[item.fieldname for item in meta.fields]
                filtered = [item for item in fields if item in doctype_fields] 
                all_fields = pre_fields + filtered
                data=frappe.get_all('Opportunity Item', filters=[['name','in',pre_data]],fields=all_fields)
                for item in data: 
                    item['subject'] = 'Interested In'
                    item['item'] =item.pop('item_name')
                    item['link']="opportunity/"+item.pop('parent')
                products.append(data)
        if len(connections.get('customer')) > 0 :
                pre_data=frappe.get_all('Customer Items', filters=[['parent','in',connections.get('customer')]],pluck='name',limit=limit)
                pre_fields=['item','sell_date','parent']
                meta = frappe.get_meta("Customer Items")
                doctype_fields=[item.fieldname for item in meta.fields]
                filtered = [item for item in fields if item in doctype_fields] 
                all_fields = pre_fields + filtered    
                data=frappe.get_all('Customer Items', filters= [['name','in',pre_data]],fields=all_fields)
                for item in data: 
                    item['subject'] = 'Sold'
                    item['item'] =frappe.get_doc("Item",item.pop('item')).item_name
                    item['creation'] =item.pop('sell_date')
                    item['link']="customer/"+item.pop('parent')
                products.append(data)  
            
        flat_list = [obj for sublist in products for obj in sublist]
        
        ordered = sorted(flat_list, key=lambda x: x['creation'],reverse=True)
        return ordered
    except Exception as e :
        logger_exception.error(f" file => advantage page.py get_products lead {lead}  {frappe.get_traceback()} ")
        frappe.log_error(message= f" file => advantage page.py get_products lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


def get_issues(lead,fields,limit):
    try:
        connections=get_detailed_connections(lead)
        products=[]
        if frappe.has_permission("Issue", "read"):
            products.append(frappe.get_list('Issue', filters=[['lead','=',lead]],fields=fields,limit=limit))
        if len(connections.get('customer')) > 0 :
            if frappe.has_permission("Issue", "read"):
                products.append(frappe.get_list('Issue', filters=[['customer','in',connections.get('customer')]],fields=fields,limit=limit))
        flat_list = [obj for sublist in products for obj in sublist]
        ordered = sorted(flat_list, key=lambda x: x['creation'],reverse=True)
        for item in ordered:            
                item['description'] =  re.sub(r"<.*?>", "",item.pop('description'))          
        return ordered
    except Exception as e :
        logger_exception.error(f" file => advantage page.py get_issues lead {lead}  {frappe.get_traceback()} ")
        frappe.log_error(message= f" file => advantage page.py get_issues lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


def get_notes(lead,fields,limit):
    try:
        connections=get_detailed_connections(lead)
        notes=[]
        pre_data=frappe.get_all('CRM Note', filters=[['parent','=',lead],["parenttype","=","Lead"]],pluck='name',limit=limit)     
        notes.append(frappe.get_all('CRM Note', filters=[['name','in',pre_data]],fields=fields))
        #if len(connections.get('opportunities')) > 0 :
        #    pre_data=frappe.get_all('CRM Note', filters=[['parent','in',connections.get('opportunities')],["parenttype","=","Opportunity"]],pluck='name',limit=limit)   
        #   notes.append(frappe.get_all('CRM Note', filters=[['name','in',pre_data]],fields=fields))
        flat_list = [obj for sublist in notes for obj in sublist]
        ordered = sorted(flat_list, key=lambda x: x['added_on'],reverse=True)
        for item in ordered:            
            if 'note' in item:
                item['note'] =  re.sub(r"<.*?>", "",item.pop('note'))  
            else:
                item['note']="NA" 
            item['link']=item.get('parenttype')[0].lower() + item.pop('parenttype')[1:] +"/"+item.pop('parent')  
        return ordered
    except Exception as e :
        logger_exception.error(f" file => advantage page.py get_notes lead {lead}  {frappe.get_traceback()} ")
        frappe.log_error(message= f" file => advantage page.py get_notes lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  


@frappe.whitelist()
def save_lead(lead):
    try:
        data=json.loads(lead)	
        if data.get("lead_id") != "NA":
        
        
            
            
            
            updates= {
                "market_segment" : data.get("market_segment")  ,
            "gender": data.get("gender"),
            "first_name": data.get("first_name"),
            "last_name":data.get("last_name"),
            "company":data.get("company") ,
            "job_title":data.get("job_title"),
            "company_name": data.get("organization"),
            "mobile_no" : data.get("mobile_no"),
            "whatsapp_no" : data.get("whatsapp"),
            "phone": data.get("phone_no"),
            "email_id": data.get("email"),
            "industry":data.get("industry"),
            "territory":data.get("territory"),
            "custom_birth_date":data.get("birth_date"),
            


            }
            if data.get("source") is not None and data.get("source") != "":
                updates.update({"source": data.get("source")})
            frappe.db.set_value("Lead", data.get("lead_id"), updates)
            return data.get("lead_id")
        else:
            if data.get("source") is not None and data.get("source") != "":
                doc = frappe.get_doc({
                    "doctype": "Lead",
                "gender": data.get("gender"),
                "first_name": data.get("first_name"),
                "last_name":data.get("last_name"),
                "custom_birth_date":data.get("birth_date"),
                "mobile_no" : data.get("mobile_no"),
                    "company":data.get("company") ,
                    "market_segment" : data.get("market_segment")  ,
                    "job_title":data.get("job_title"),
                    "whatsapp_no" : data.get("whatsapp"),
                "phone": data.get("phone_no"),
                "email_id": data.get("email"),
                "industry":data.get("industry"),
                "territory":data.get("territory"),
                "company_name": data.get("organization"),
                "source": data.get("source")
                })
            
            else: 
                doc = frappe.get_doc({
                    "doctype": "Lead",
                "gender": data.get("gender"),
                "first_name": data.get("first_name"),
                "last_name":data.get("last_name"),
                "custom_birth_date":data.get("birth_date"),
                "mobile_no" : data.get("mobile_no"),
                    "company":data.get("company") ,
                    "market_segment" : data.get("market_segment")  ,
                    "job_title":data.get("job_title"),
                    "whatsapp_no" : data.get("whatsapp"),
                "phone": data.get("phone_no"),
                "email_id": data.get("email"),
                "industry":data.get("industry"),
                "territory":data.get("territory"),
                "company_name": data.get("organization")
                
                })   
            doc.insert()
            frappe.db.commit()
            return doc.name
    except Exception as e :
        logger_exception.error(f" file => advantage page.py save_lead lead {lead}  {frappe.get_traceback()} ")
        frappe.log_error(message= f" file => advantage page.py save_lead lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  
    


 
def get_emails(lead,limit):
    try:
        import datetime
        emails=[]
        lead_doc=frappe.get_doc('Lead',lead)
        if lead_doc.email_id is not None and lead_doc.email_id != "":
            values = {'email': '%'+lead_doc.email_id+'%', 'lead_name':lead_doc.name,'company':lead_doc.company,'limit':limit}
            emails=frappe.db.sql("""

            select B.sent_or_received,B.sender,B.creation,B.recipients,B.uid,B.subject,B.name from  `tabCommunication` B  
            where B.communication_medium='Email' and  (B.recipients like  %(email)s
            or B.sender like  %(email)s )
            and B.company =%(company)s
            order by creation desc
            limit %(limit)s """,values=values, as_dict=1)
            #emails= frappe.get_all("Communication", filters=[["communication_medium","=","Email"]],or_filters=['recipients','=',email],fields=['sent_or_received','sender','creation','recipients','uid','subject','name'],order_by='creation desc',limit=4)
            for email in emails:
                # 1. Change 'sent_or_received' -> 'disposition'
                # .pop() gets the value of the old key and deletes the old key from the dict
                email['call_type'] = email.pop('sent_or_received')
                
                # 2. Change 'sender' -> 'call_from'
                email['call_from_name'] = email.pop('sender')
                email['call_to_name'] = email.pop('recipients')
                email['call_id'] = str(email.pop('uid'))
                email['creation'] = email['creation'].replace(microsecond=0)
                email['disposition'] = str(email.pop('subject'))
                email['link']="/app/communication/"+email.pop('name')  
            
        return emails
    except Exception as e :
        logger_exception.error(f" file => advantage page.py get_emails lead {lead}  {frappe.get_traceback()} ")
        frappe.log_error(message= f" file => advantage page.py get_emails lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  
    

def combine_email_with_cdr(lead):
    try:
        lead_doc=frappe.get_doc('Lead',lead)
        aa=[]
        calls=[]
        limit=frappe.get_single('Advantage Page Settings').num_of_calls or 0
        if limit > 0:
            if lead_doc.mobile_no is not None and lead_doc.mobile_no != '':
                calls.extend(get_phone_cdrs_by_cdrid(lead_doc.mobile_no,limit))
            if lead_doc.phone is not None and lead_doc.phone != '':
                calls.extend(get_phone_cdrs_by_cdrid(lead_doc.phone,limit))

            for call in calls:
                    # 1. Change 'sent_or_received' -> 'disposition'
                    # .pop() gets the value of the old key and deletes the old key from the dict
                    if len(call['call_from_number'])==3:
                        call['call_from_number'] = call.pop('call_from_name')
                    
        limit=frappe.get_single('Advantage Page Settings').num_of_emails or 0
        if limit > 0:
            emails=get_emails(lead,limit)
        
            combined_timeline = emails + calls

        # 4. Sort by 'creation' (Reverse=True means Newest First)
        aa = sorted(combined_timeline, key=lambda x: x['creation'], reverse=True)
        return aa
    except Exception as e :
        logger_exception.error(f" file => advantage page.py combine_email_with_cdr lead {lead}  {frappe.get_traceback()} ")
        frappe.log_error(message= f" file => advantage page.py combine_email_with_cdr lead {lead}  {frappe.get_traceback()} ", title="Advantage Page")  
    