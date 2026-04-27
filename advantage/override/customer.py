
import frappe
from erpnext.selling.doctype.customer.customer import Customer
from advantage.utils import get_detailed_connections
logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)
class AdvantageCustomer(Customer):
    def validate(self):
        super().validate()
        if self.account_manager is None or self.account_manager == "":
            self.account_manager=frappe.session.user

            
    def on_update(self):
        try:
            if self.lead_name is not None and self.lead_name != "" and self.opportunity_name is not None and self.opportunity_name != "":
                connections=get_detailed_connections(self.lead_name)
                if len(connections.get('opportunities')) > 0 :
                    if self.opportunity_name not in  connections.get('opportunities') :
                        frappe.throw(frappe._("Lead and Opportunities not to same Person"))
        except Exception as e :
            logger_exception.error(f" file => advantagecustomer.py on_update self {self}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantagecustomer.py on_update self {self}  {frappe.get_traceback()} ", title="Advantage")  


        
                
                

