import frappe
from frappe.permissions import AUTOMATIC_ROLES
import datetime

def update_cdrs_data(lead):
    lead_doc=frappe.get_doc('Lead',lead)
    if ( len (frappe.get_all("PBX CDRs",filters=[['related_doctype_id','!=',lead_doc.name]],or_filters=[[ "call_from_number","=", lead_doc.phone_ext],[ "call_from_number","=", lead_doc.phone],[ "call_from_number","=", lead_doc.whatsapp_no],[  "call_from_number","=",lead_doc.mobile_no],["call_from_number","=",lead_doc.custom_additional_mobile],[  "call_from_number","=", lead_doc.custom_additional_phone]],pluck='name'))  > 0):
            for a in frappe.get_all("PBX CDRs",filters=[['related_doctype_id','!=',lead_doc.name]],or_filters=[[ "call_from_number","=", lead_doc.phone_ext ],[ "call_from_number","=", lead_doc.phone],[ "call_from_number","=", lead_doc.whatsapp_no],[  "call_from_number","=",lead_doc.mobile_no],["call_from_number","=",lead_doc.custom_additional_mobile],[  "call_from_number","=", lead_doc.custom_additional_phone]],pluck='name') :
                cdr=frappe.get_doc("PBX CDRs",a)
                cdr.db_set('related_doctype_id',lead_doc.name,False,False,True)   
    if ( len (frappe.get_all("PBX CDRs",filters=[['related_doctype_id','!=',lead_doc.name]],or_filters=[[ "call_to_number","=", lead_doc.phone_ext],[ "call_to_number","=", lead_doc.phone],[ "call_to_number","=", lead_doc.whatsapp_no],[  "call_to_number","=",lead_doc.mobile_no],["call_to_number","=",lead_doc.custom_additional_mobile],[  "call_to_number","=", lead_doc.custom_additional_phone]],pluck='name'))  > 0):
            for a in frappe.get_all("PBX CDRs",filters=[['related_doctype_id','!=',lead_doc.name]],or_filters=[[ "call_to_number","=", lead_doc.phone_ext ],[ "call_to_number","=", lead_doc.phone],[ "call_to_number","=", lead_doc.whatsapp_no],[  "call_to_number","=",lead_doc.mobile_no],["call_to_number","=",lead_doc.custom_additional_mobile],[  "call_to_number","=", lead_doc.custom_additional_phone]],pluck='name') :
                cdr=frappe.get_doc("PBX CDRs",a)
                cdr.db_set('related_doctype_id',lead_doc.name,False,False,True)                   

def get_sender_details():
    return "John Doe", "johndoe@example.com"
@frappe.whitelist()
def get_sender_email(user=None):
    if not user:
        user = frappe.session.user
    company = frappe.defaults.get_user_default("company")
    if len(frappe.get_all('Email Account',filters=[['company','=',company],['enable_outgoing','=','1']],pluck='email_id')) > 0 :
        return frappe.get_all('Email Account',filters=[['company','=',company],['enable_outgoing','=','1']],pluck='email_id')

def update_emails_data(lead):
    lead_doc=frappe.get_doc('Lead',lead)
    if (lead_doc.email_id is not None and lead_doc.email_id != "") :
        values = {'email': '%'+lead_doc.email_id+'%', 'lead_name':lead_doc.name,'company':lead_doc.company}
        
        data=frappe.db.sql("""

        select B.name from  `tabCommunication` B  
        where (B.recipients like  %(email)s
        or B.sender like  %(email)s )
        and B.company =%(company)s 
        and B.name not in ( select parent from  `tabCommunication Link`  TT where     TT.link_doctype='Lead'
        and TT.link_name=%(lead_name)s )
                    """,values=values, as_dict=1)
        for r in data :
            communication=frappe.get_doc('Communication',r.name)
            contact=communication.append("timeline_links", {})
                
            
            contact.link_name=lead_doc.name
            contact.link_doctype=lead_doc.doctype
                
            contact.save(ignore_permissions=True)
        frappe.db.commit()

def get_permission_query_conditions(user):
    if not user:
        user = frappe.session.user

    task_roles = frappe.permissions.get_doctype_roles("Task")
    task_roles = set(task_roles) - set(AUTOMATIC_ROLES)

    #if any(check in task_roles for check in frappe.get_roles(user)):
    #    return None
    #else:
    if 'Task Admin' in  frappe.get_roles(user) :
        return None
    else:
        return """ ( `tabTask`.name in (select reference_name from `tabToDo` where `tabToDo`.reference_type='Task' and `tabToDo`.status !='Cancelled' and   (`tabToDo`.allocated_to = {user} or `tabToDo`.assigned_by = {user}))) """.format(
            user=frappe.db.escape(user)
        )

def normalize_syria_number(number):
    import re
    if (number is not None and number != ''):
        return re.sub(r'^0(?![0])', '00963', number)
    else:
        return 


def has_permission(doc, ptype="read", user=None):

    user = user or frappe.session.user   
    if 'Task Admin' in  frappe.get_roles(user) :
        return True
    if len(frappe.get_all('ToDo', filters=[["reference_type",'=','Task'],['reference_name','=',doc.name],['status','!=','Cancelled']],or_filters=[["ToDo", "allocated_to", "=", user],["ToDo", "assigned_by", "=", user],],fields=['*'])) ==1:
        return True
    else:
        return False



def get_lead_phone_numbers(lead_name):
    connections=get_detailed_connections(lead_name)
    combined = sum(connections.values(), [])
    combined.append(lead_name)
    data_set=set(combined)
    final_list=list(data_set)    
    dynamic_link=frappe.get_all('Dynamic Link', filters=[["parenttype",'=','Contact'],['parentfield','=','links'],['link_name','in',final_list]],fields=['parent'])
    if len(dynamic_link) > 0 :
        contacts =list(set( [d['parent'] for d in dynamic_link]))
        phones=frappe.get_all('Contact Phone', filters=[["parenttype",'=','Contact'],['parent','in',contacts]],fields=['phone'])
        if len(phones) > 0 :
            return   list(set( [ str(d['phone']).strip() for d in phones]))

def get_detailed_connections(lead_name):
    connections = {}

    # 1. Get Opportunities
    connections['opportunities'] = frappe.db.get_list("Opportunity", 
        filters={"party_name": lead_name, "opportunity_from": "Lead"},
        pluck='name'
    )

    # 2. Get Quotations
    connections['quotations'] = frappe.db.get_list("Quotation", 
        filters={"party_name": lead_name, "quotation_to": "Lead"},
       pluck='name'
    )

    # 3. Get Prospects (If linked)
    # Note: Prospects usually link TO leads, or Leads link TO prospects depending on flow
    connections['prospects'] = frappe.db.get_list("Prospect",
        filters={"lead": lead_name},
        pluck='name'
    )

    # 4. Get Customer (If converted)
    connections['customer'] = frappe.db.get_list("Customer",
        filters={"lead_name": lead_name},
       pluck='name'
    )

    return connections



 

def format_datetime(dt: datetime.datetime) -> str:
    # Helper: add suffix to day
    def day_with_suffix(day: int) -> str:
        if 11 <= day <= 13:
            return f"{day}th"
        else:
            return f"{day}{['th','st','nd','rd','th'][min(day % 10, 4)]}"
    
    # Build formatted string
    return f"{day_with_suffix(dt.day)} {dt.strftime('%B %Y %I:%M%p')}"
 
def show_how_old(dt: datetime.datetime) -> str:
    now = datetime.datetime.now()

    # Calculate difference
     
    delta = now - dt

    # Format as "X days ago"
    days_ago = f"{delta.days} days ago"
    return days_ago
