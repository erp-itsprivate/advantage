
import frappe
from frappe import _
from erpnext.crm.doctype.opportunity.opportunity import Opportunity
from frappe.utils import get_link_to_form

from frappe.utils import get_datetime, now_datetime
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
     
        same_opportunities=frappe.get_all('Opportunity',filters=[['name','!=',self.name],['opportunity_from','=',self.opportunity_from],['party_name','=',self.party_name],['opportunity_type','=',self.opportunity_type],['custom_opportunity_cycle','not in',['Lost','Converted','Handed Over','Closed']]],fields=['name'])
      
        if (len(same_opportunities) > 0):
            message = "<ul>"
            for doc in same_opportunities:
                # This automatically generates: <a href="/app/task/TASK-0001">TASK-0001</a>
                doc_link = get_link_to_form('Opportunity', doc.get("name"))
                
                # Add it to the list as an HTML list item <li>
                message += f"<li>{doc_link}</li>"

            # 3. Close the list
            message += "</ul>"

            # 4. Show the message
            html_message = """ Can't create new opportunity ,opportunities exists  :<br><br>
                <div style="padding: 10px;">
                    {0}
                </div>
            """.format(message)

            frappe.throw(html_message)
           
        old_doc = self.get_doc_before_save()
        checkbox_is_being_set_to_true = (self.custom_need_test_drive == 1 and 
                                         (not old_doc or old_doc.custom_need_test_drive == 0))

        # Condition 3: The document's status is in the restricted list
        status_is_restricted = (self.custom_opportunity_cycle in ['Lost', 'Converted','Handed Over','Closed'])

        if checkbox_is_being_set_to_true and status_is_restricted:
            frappe.throw(frappe._("You cannot check this field when in this status"))
        if len(self.custom_test_drive_history) > 0 and self.custom_need_test_drive == False:
            frappe.throw(frappe._("You need to check test drive"))
        if  len(self.custom_test_drive_history) > 0 and self.custom_cancel_test_drive == True:
                frappe.throw(frappe._("You need to cancel test drive rows"))
        if  len(self.custom_test_drive_history) > 0  :
            for row in  self.custom_test_drive_history :
                    if row.test_drive_execution_date and row.test_drive_plan_date:
                        start_dt = get_datetime(row.test_drive_plan_date)
                        end_dt = get_datetime(row.test_drive_execution_date)

                        if end_dt <= start_dt :
                            frappe.throw(frappe._("execution date must be more than plan date"))
                    #if  get_datetime(row.test_drive_plan_date) < now_datetime():
                     #       frappe.throw(frappe._("Test drive execution date can't be in the past"))
       
        # if len(self.custom_opportunity_cycle_history) == 0 :
        #     # Set your custom datetime field to the current time
        #     #doc.custom_opportunity_cycle_latest_datetime = frappe.utils.now()
        #     new_item = self.append("custom_opportunity_cycle_history", {})

        #     # 3. Set the values for the new row
        #     new_item.user = frappe.session.user
        #     new_item.action_date = frappe.utils.now()
        #     new_item.state = self.custom_opportunity_cycle
        if self.custom_opportunity_cycle != self.get_db_value("custom_opportunity_cycle"):
            # Set your custom datetime field to the current time
            #doc.custom_opportunity_cycle_latest_datetime = frappe.utils.now()
            action_date=frappe.utils.now()
            cycle_rows = self.get("custom_opportunity_cycle_history") 
        
            # 2. Find rows with no action_end_date
            open_rows = [row for row in cycle_rows if not row.action_end_date]
            
            if open_rows:
                # 3. Sort them so the newest action_date is first (descending)
                open_rows.sort(key=lambda x: x.action_date or "", reverse=True)
                
                # 4. Update the most recent one in memory!
                previous_record = open_rows[0]
                previous_record.action_end_date = action_date

                
            new_item = self.append("custom_opportunity_cycle_history", {})

            # 3. Set the values for the new row
            new_item.user = frappe.session.user
            new_item.action_date = action_date
            new_item.state = self.custom_opportunity_cycle

            self.custom_last_action_date=action_date
    
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
    