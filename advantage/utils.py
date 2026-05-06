import frappe
from frappe.permissions import AUTOMATIC_ROLES
import datetime
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from erpnext.selling.doctype.quotation.quotation import create_customer_from_lead,handle_mandatory_error
from erpnext.crm.doctype.lead.lead import _make_customer 


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

def advantage_make_customer(source_name, ignore_permissions=False):
    frappe.log_error(f"Customer Create from Quotation: {source_name}", "Cutomer Creation")
    quotation = frappe.db.get_value(
                "Quotation",
                source_name,
                ["order_type", "quotation_to", "party_name", "customer_name","opportunity"],
                as_dict=1,
        )
    if quotation.quotation_to == "Customer":
        return frappe.get_doc("Customer", quotation.party_name)
    existing_customer = None
    if quotation.quotation_to == "Lead":
        existing_customer = frappe.db.get_value("Customer", {"lead_name": quotation.party_name})
    elif quotation.quotation_to == "Prospect":
        existing_customer = frappe.db.get_value("Customer", {"prospect_name": quotation.party_name})
    if existing_customer:
        return frappe.get_doc("Customer", existing_customer)
    if quotation.quotation_to == "Lead":
        return  advantage_create_customer_from_lead(quotation.party_name,quotation.opportunity, ignore_permissions=ignore_permissions)
    elif quotation.quotation_to == "Prospect":
       return   advantage_make_customer_prospect(quotation.party_name, ignore_permissions=ignore_permissions)
        
     
    return None

def advantage_create_customer_from_lead(lead_name, opportunity,ignore_permissions=False):
    
    customer = _make_customer(lead_name, ignore_permissions=ignore_permissions)
    customer.opportunity_name=opportunity
    customer.flags.ignore_permissions = ignore_permissions
    try:
        customer.insert()
        return customer
    except frappe.MandatoryError as e:
        handle_mandatory_error(e, customer, lead_name)

@frappe.whitelist()
def advantage_make_customer_prospect(source_name: str, target_doc: str | Document | None = None):
    
    def set_missing_values(source, target):
        target.customer_type = "Company"
        target.company_name = source.name
        target.customer_group = source.customer_group or frappe.db.get_default("Customer Group")
    doclist = get_mapped_doc(
                "Prospect",
                source_name,
                {
                        "Prospect": {
                                "doctype": "Customer",
                                "field_map": {"company_name": "customer_name", "currency": "default_currency", "fax": "fax","name":"prospect_name"},
                        }
                },
                target_doc,
                set_missing_values,
                ignore_permissions=False,
        )
    return doclist

def todo_event_additional_data(doc):
    user=None
    if doc.doctype=="ToDo":
        if doc.reference_type == 'Opportunity' and doc.reference_name:
            opp = frappe.get_doc('Opportunity',doc.reference_name)
            if opp:
                doc.custom_opportunity_domain = opp.opportunity_type
        if doc.reference_type=="Event":
            event = frappe.get_doc('Event',doc.reference_name)
            doc.date=event.starts_on.date()

        user = doc.allocated_to
    else:
       
        if len(doc.event_participants) > 0 :
            for row in doc.event_participants:
                if row.reference_doctype == 'Opportunity' and row.reference_docname:
                    opp = frappe.get_doc('Opportunity',doc.reference_docname)
                    if opp:
                        doc.custom_opportunity_domain = opp.opportunity_type
        
        for todo in frappe.get_all('ToDo', filters=[["reference_type",'=','Event'],['reference_name','in',doc.name]]):
            todo_doc=frappe.get_doc('ToDo',todo.name)
            #todo_doc.date=doc.starts_on.date()
            user=todo_doc.allocated_to
            #todo_doc.save()          
    
    company = frappe.defaults.get_user_default("Company")
    
    #company = 'KIA'
    #user = 'obay.t@kia-sy.com'
    if company and user:
        domains = frappe.db.sql("""
            select 
                distinct custom_domain , grp.name 
            from 
                `tabUser Group` as grp left outer join 
                `tabUser Group Member` as mem 
                    on grp.name = mem.parent
            where
                grp.custom_company = %(company)s and
                (
                    grp.custom_group_manager = %(user)s or
                    mem.user =%(user)s
                )
        """, {"user": user,"company":company}, as_dict=True)
        
        if domains:
            #doc.custom_user_domain = domains[0].custom_domain
            #doc.custom_user_group = domains[0].name
            doc.db_set('custom_user_domain',domains[0].custom_domain,False,False,False) 
            doc.db_set('custom_user_group',domains[0].name,False,False,True)    
          
            
   
    

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_user_same_company(doctype: str, txt: str, searchfield: str, start: int, page_len: int, filters: dict | list):
    users=[]
    company = frappe.defaults.get_user_default("company")
    if company:
        memberships = frappe.get_all(
                "User Group",
    
        filters={"custom_company":company},
                fields=["name"]
    
    
        )
        list_of_all=[]
        if len(memberships)>0:
            for us_gr in memberships :
                list_of_all.append(frappe.get_all("User Group Member",filters={"parent":us_gr.name},fields=["user"]))
        users = [item.user for sublist in list_of_all for item in sublist]
        set_users=set(users)
        users=list(set_users)
        values = {'users': users,"txt": "%" + txt + "%",}
        return frappe.db.sql("""
            select name from  `tabUser` 
            where  name in %(users)s and   tabUser.name LIKE %(txt)s""",values=values)

def email_queue(doc, method=None):
    import ast
    allowed_domains=[]
    setting = frappe.get_single('Advantage Settings')
    allowed_domains_list=setting.allowed_domains
    allowed_emails_list=setting.allowed_emails
    if allowed_emails_list is not None:
        try:
            allowed_emails=ast.literal_eval(allowed_emails_list)
        except Exception as e:
            frappe.throw("Please Correct the email list in Advantage Settings")
    if allowed_domains_list is not None:
        try:
            allowed_domains = ast.literal_eval(allowed_domains_list)
        except Exception as e:
            frappe.throw("Please Correct the email domains in Advantage Settings")
    # 2. We will build a list of only the recipients that pass the filter
    filtered_recipients = []

    for row in doc.recipients:
        email_address = row.recipient.lower().strip()
        # Check if the email ends with any of the allowed domains
        # We add the '@' to ensure we don't accidentally match 'othercompany.com' with 'company.com'
        for domain in allowed_domains :
            is_internal = email_address.endswith("@" + domain)
            if is_internal :
                break

        if is_internal :
            filtered_recipients.append(row)
        else:
            for email in allowed_emails:
                if email.lower().strip()==email_address:
                    filtered_recipients.append(row)
                else:
            # Optional: Log the blocked email in the Error Log for your reference
                    frappe.log_error(f"Blocked email to external recipient: {email_address}", "Email Filter")

    # 3. Update the document's recipient list
    if not filtered_recipients:
        # If NO recipients are internal, we stop the email from being sent
        doc.recipients = []
        doc.status = "Not Sent" 
        # This prevents the background worker from picking it up
        
        # Optional: If you want to see a message on screen when this happens:
        # frappe.msgprint("Email blocked: No internal recipients found.")
    else:
        # If there were mixed recipients (internal + external), 
        # this line removes the external ones and keeps the internal ones.
        doc.recipients = filtered_recipients


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

def get_employees_under_user(login_user):
    employee_of_user=[]
    user=login_user or frappe.session.user
    owner_of = list(set(frappe.get_all('User Group',filters=[["custom_group_manager",'=',user]],fields=['*'],pluck='name')))
    if len(owner_of) > 0 :
        employee_of_user=list(set(frappe.get_all('User Group Member',filters=[["parent",'in',owner_of]],fields=['user'],pluck='user')))           
    else:
        employee_of_user.append(user)
    return employee_of_user

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
    if frappe.has_permission('Opportunity', "read"):
        connections['opportunities'] = frappe.db.get_list("Opportunity", 
            filters={"party_name": lead_name, "opportunity_from": "Lead"},
            pluck='name'
        )

    # 2. Get Quotations
    if frappe.has_permission('Quotation', "read"):
        connections['quotations'] = frappe.db.get_list("Quotation", 
            filters={"party_name": lead_name, "quotation_to": "Lead"},
        pluck='name'
        )

    # 3. Get Prospects (If linked)
    # Note: Prospects usually link TO leads, or Leads link TO prospects depending on flow
    if frappe.has_permission('Prospect', "read"):
        connections['prospects'] = frappe.db.get_list("Prospect",
            filters={"lead": lead_name},
            pluck='name'
        )

    # 4. Get Customer (If converted)
    if frappe.has_permission('Customer', "read"):
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
