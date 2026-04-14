
import frappe
from frappe import _
from erpnext.crm.doctype.opportunity.opportunity import Opportunity



logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)
logger = frappe.logger("advantage", allow_site=True, file_count=50)
logger.setLevel(20)
class AdvantageOpportunity(Opportunity):
    # def after_insert(self):
    #      if len(self.custom_opportunity_cycle_history) == 0 :
    #             # Set your custom datetime field to the current time
    #             #doc.custom_opportunity_cycle_latest_datetime = frappe.utils.now()
    #             new_item = self.append("custom_opportunity_cycle_history", {})

    #             # 3. Set the values for the new row
    #             new_item.user = frappe.session.user
    #             new_item.action_date = frappe.utils.now()
    #             new_item.state = self.custom_opportunity_cycle
    #             self.save()
    def validate(self):
        super().validate()
        try:
            if len(self.custom_opportunity_cycle_history) == 0 :
                # Set your custom datetime field to the current time
                #doc.custom_opportunity_cycle_latest_datetime = frappe.utils.now()
                new_item = self.append("custom_opportunity_cycle_history", {})

                # 3. Set the values for the new row
                new_item.user = frappe.session.user
                new_item.action_date = frappe.utils.now()
                new_item.state = self.custom_opportunity_cycle

        
            # 1) Ensure opportunity_owner is set
            if not self.opportunity_owner:
                self.opportunity_owner=frappe.session.user
                
                

        
            # First: check if owner is a group manager for this company
            group = frappe.get_all(
                "User Group",
                filters={
                    "custom_group_manager": self.opportunity_owner,
                    "custom_company": self.company
                },
                fields=["name","custom_domain"]
            )

            if group:
                self.custom_user_group=group[0].name
                self.custom_domain =group[0].custom_domain
            
            else:
                # Second: check if owner is a member of a group for this company
                memberships = frappe.get_all(
                    "User Group Member",
                    filters={"user": self.opportunity_owner},
                    fields=["parent"]
                )

                for m in memberships:
                    parent_group = frappe.get_doc("User Group", m.parent)
                    if parent_group.custom_company == self.company:
                        self.custom_user_group=parent_group.name 
                        self.custom_domain =parent_group.custom_domain
                        break
            #frappe.msgprint(self.custom_domain)
            #print(self.custom_domain)
            frappe.db.commit()
            logger.info(f" file => advantage opportunity.py on_update opportunity {self.name} custom_user_group {self.custom_user_group}  custom_domain {self.custom_domain}  ")
        except Exception as e :
            logger_exception.error(f" file => advantage opportunity.py on_update opportunity {self.name}  {frappe.get_traceback()} ")
            frappe.log_error(message= f" file => advantage opportunity.py on_update opportunity {self.name}  {frappe.get_traceback()} ", title="Advantage")  
