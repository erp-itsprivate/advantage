
import frappe
from frappe import _
from erpnext.crm.doctype.lead.lead import Lead
from advantage.utils import get_detailed_connections,normalize_syria_number,update_cdrs_data,update_emails_data
logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)


class AdvantageLead(Lead):
    def validate(self):
        phone_fields = ["mobile_no", "phone", "whatsapp_no", "phone_ext","custom_additional_mobile","custom_additional_phone"]

        for fieldname in phone_fields:
            # Get the actual value of the field (equivalent to self.mobile_no)
            value = getattr(self, fieldname)
            
            # Check if value exists (not None and not empty) and doesn't start with "00"
            if value and not value.startswith("00"):
                 frappe.throw(_("Phone / Mobile Number should start with 00"))
        if not self.company :
            frappe.throw(_("Company field is mandatory"))     
        self.check_duplicate_mobile_no()                           
        self.first_name=self.first_name.strip()
        self.last_name=self.last_name.strip()
        super().set_full_name()
        self.title=self.lead_name
        
    def check_duplicate_mobile_no(self):
            phone_ext=self.phone_ext or  self.mobile_no
            phone=self.phone or self.mobile_no
            whatsapp_no=self.whatsapp_no or self.mobile_no
            mobile_no=self.mobile_no  
            custom_additional_mobile=self.custom_additional_mobile or self.mobile_no
            custom_additional_phone=self.custom_additional_phone or self.mobile_no

            values = {'name':self.name,'phone_ext': phone_ext, 'phone':phone,'company':self.company,'whatsapp_no':whatsapp_no,'mobile_no':mobile_no,'custom_additional_mobile':custom_additional_mobile,'custom_additional_phone':custom_additional_phone}
            data=frappe.db.sql("""
                            Select name from `tabLead` where company = %(company)s and name != %(name)s
                            and ( phone_ext in (%(phone_ext)s ,%(phone)s,%(whatsapp_no)s,%(mobile_no)s,%(custom_additional_mobile)s,%(custom_additional_phone)s ) 
                            or phone in (%(phone_ext)s ,%(phone)s,%(whatsapp_no)s,%(mobile_no)s,%(custom_additional_mobile)s,%(custom_additional_phone)s ) 
                            or whatsapp_no in (%(phone_ext)s ,%(phone)s,%(whatsapp_no)s,%(mobile_no)s,%(custom_additional_mobile)s,%(custom_additional_phone)s )
                            or mobile_no in (%(phone_ext)s ,%(phone)s,%(whatsapp_no)s,%(mobile_no)s,%(custom_additional_mobile)s,%(custom_additional_phone)s )
                            or custom_additional_mobile in (%(phone_ext)s ,%(phone)s,%(whatsapp_no)s,%(mobile_no)s,%(custom_additional_mobile)s,%(custom_additional_phone)s )
                            or custom_additional_phone in (%(phone_ext)s ,%(phone)s,%(whatsapp_no)s,%(mobile_no)s,%(custom_additional_mobile)s,%(custom_additional_phone)s )
                            )
                            """,values=values, as_dict=1)
            if len(data) >0 :
                frappe.throw(_("Another Lead {0} with same mobile number").format(data[0].name ))

    def on_update(self):
    #    for link in frappe.get_all('Dynamic Link', filters=[['link_doctype','=','Lead'],['link_name','=',self.name]],pluck='parent'):
    #         for contact in frappe.get_all('Contact Phone', filters=[['parent','=',link],["phone","=",self.mobile_no]],fields=['*']):
    #             contact_phone=frappe.get_doc('Contact Phone',{'parent':link,'phone':self.mobile_no})
    #             contact_phone.db_set('is_primary_mobile_no',True,False,False,True)
        if (self.company is not None and self.company != ""):
            self.check_duplicate_mobile_no()
            try:
                self.db_set('phone_ext',normalize_syria_number(self.phone_ext),False,False,True)
                self.db_set('phone',normalize_syria_number(self.phone),False,False,True)
                self.db_set('whatsapp_no',normalize_syria_number(self.whatsapp_no),False,False,True)
                self.db_set('mobile_no',normalize_syria_number(self.mobile_no),False,False,True)
                self.db_set('custom_additional_mobile',normalize_syria_number(self.custom_additional_mobile),False,False,True)
                self.db_set('custom_additional_phone',normalize_syria_number(self.custom_additional_phone),False,False,True)
                # self.db_set('first_name',  self.first_name.strip(),False,False,True)
                # self.db_set('last_name',  self.last_name.strip(),False,False,True) 
                # self.db_set('title',  self.lead_name,False,False,True) 
                # lead_name = " ".join(
                # 	filter(None, [ (self.salutation or "").strip(), (self.first_name or "").strip(), (self.middle_name or "").strip(), (self.last_name or "").strip()])
                # )
                # self.db_set('lead_name',  lead_name,False,False,True) 
                connections=get_detailed_connections(self.name)
                if len(connections.get('opportunities')) > 0 :
                    for oppor in connections.get('opportunities'):
                        opportunity=frappe.get_doc('Opportunity',oppor)
                        opportunity.db_set('custom_additional_mobile',normalize_syria_number(self.custom_additional_mobile),False,False,True)       
                        opportunity.db_set('custom_additional_phone',normalize_syria_number(self.custom_additional_phone),False,False,True)      
                        opportunity.db_set('contact_email',self.email_id,False,False,True)      
                        opportunity.db_set('contact_mobile',normalize_syria_number(self.mobile_no),False,False,True)      
                        opportunity.db_set('phone',normalize_syria_number(self.phone),False,False,True)    
                        opportunity.db_set('whatsapp',normalize_syria_number(self.whatsapp_no),False,False,True)     
                        opportunity.db_set('phone_ext',normalize_syria_number(self.phone_ext),False,False,True)   
                        opportunity.db_set('contact_display',self.title,False,False,True)        
                        opportunity.db_set('title',self.title,False,False,True)     
                if  len(connections.get('customer')) > 0 :
                    for cust in connections.get('customer'):
                        customer=frappe.get_doc('Customer',cust)
                        customer.db_set('custom_additional_phone',normalize_syria_number(self.custom_additional_mobile),False,False,True)       
                        customer.db_set('custom_phone',normalize_syria_number(self.phone),False,False,True)    
                        customer.db_set('custom_additional_mobile',normalize_syria_number(self.custom_additional_mobile),False,False,True)  
                        customer.db_set('custom_mobile',normalize_syria_number(self.mobile_no),False,False,True)   
                        customer.db_set('custom_email',self.email_id,False,False,True)       
                unique_job_name = f"update_cdrs_data_{self.name}"                
                frappe.enqueue(
                                                update_cdrs_data, # python function or a module path as string
                                                queue="default", # one of short, default, long
                                                timeout=None, # pass timeout manually
                                                is_async=True, # if this is True, method is run in worker
                                                now=False, # if this is True, method is run directly (not in a worker) 
                                                job_id=unique_job_name, # specify a job name
                                                job_name=unique_job_name,
                                                enqueue_after_commit=False, # enqueue the job after the database commit is done at the end of the request
                                                at_front=False, # put the job at the front of the queue
                                                lead=self.name
                                        
                                )
                unique_job_name = f"update_emails_data_{self.name}"   
                frappe.enqueue(
                                                update_emails_data, # python function or a module path as string
                                                queue="default", # one of short, default, long
                                                timeout=None, # pass timeout manually
                                                is_async=True, # if this is True, method is run in worker
                                                now=False, # if this is True, method is run directly (not in a worker) 
                                                job_id=unique_job_name, # specify a job name
                                                job_name=unique_job_name,
                                                enqueue_after_commit=False, # enqueue the job after the database commit is done at the end of the request
                                                at_front=False, # put the job at the front of the queue
                                                lead=self.name
                                        
                                )
            except Exception as e :
                logger_exception.error(f" file => advantagelead.py on_update self {self}  {frappe.get_traceback()} ")
                frappe.log_error(message= f" file => advantagelead.py on_update self {self}  {frappe.get_traceback()} ", title="Advantage")  

        else:
             frappe.throw(_("Company field is mandatory" ))
        
                
                


@frappe.whitelist()
def change_cdrs(source_lead,target_lead):
    frappe.db.sql("""
        update `tabPBX CDRs` set related_doctype_id=%(trg_lead)s   where related_doctype_id=%(src_lead)s   
                  """,{
        "src_lead": source_lead,
        "trg_lead": target_lead
    })
    frappe.db.commit()

 
@frappe.whitelist()
def get_cdr_html(lead):
    # 1. Fetch raw data, strictly sorted by time descending
    raw_cdrs = frappe.db.sql("""
        SELECT 
            call_id, call_type, call_from_number, duration, 
            disposition, call_to_number, call_to_name, cdr_time
        FROM `tabPBX CDRs`
         where related_doctype_id=%(lead)s  
         ORDER BY STR_TO_DATE(cdr_time, '%%d/%%m/%%Y %%H:%%i:%%s') DESC
    """,{
        "lead": lead} ,as_dict=True)

    # 2. Group the data manually while preserving the time-based sorting
    grouped_cdrs = []
    processed_ids = set()

    for cdr in raw_cdrs:
        cid = cdr.call_id
        if cid not in processed_ids:
            processed_ids.add(cid)
            
            # Find all call legs for this specific Call ID
            calls_in_group = [c for c in raw_cdrs if c.call_id == cid]
            
            # Append as a grouped dictionary
            grouped_cdrs.append({
                "call_id": cid,
                "latest_time": cdr.cdr_time, # The first one is the newest due to DESC SQL sort
                "calls": calls_in_group
            })

    # 3. Render the HTML template (Assuming the HTML above is saved in a file or field)
    html_output = frappe.render_template(
        "advantage/templates/includes/lead_cdrs.html", 
        {"grouped_cdrs": grouped_cdrs}
    )
    
    return html_output