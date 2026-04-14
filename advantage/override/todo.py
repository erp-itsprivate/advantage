
import frappe
from frappe import _
from frappe.desk.doctype.todo.todo import ToDo
from advantage.utils import todo_event_additional_data,get_employees_under_user
logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)


class AdvantageToDo(ToDo):
    def validate(self):
        super().validate()
        todo_event_additional_data(self)
    
    def after_insert(self):
        if self.reference_type=="Event":
            event = frappe.get_doc('Event',self.reference_name)
            todo_event_additional_data(event)
    
    

def get_permission_query_conditions(user):
     
    employee_of_user=[]
    if not user:
        user = frappe.session.user
    
    employee_of_user=get_employees_under_user(user)

    sql_tuple = "(" + ",".join(f"'{x}'" for x in employee_of_user) + ")"
    #if any(check in task_roles for check in frappe.get_roles(user)):
    #    return None
    #else:
    if 'ToDo Admin' in  frappe.get_roles(user) :
        return None
    else:
        return """ `tabToDo`.allocated_to = {user} or `tabToDo`.assigned_by = {user} or `tabToDo`.allocated_to in {with_my_team} """.format(
            user=frappe.db.escape(user),with_my_team=sql_tuple
        )


def has_permission(doc, ptype="read", user=None):

    user = user or frappe.session.user  
    employee_of_user= get_employees_under_user(user)
    if 'ToDo Admin' in  frappe.get_roles(user) :
        return True
    if  doc.allocated_to==user or doc.assigned_by==user or doc.allocated_to in employee_of_user :
        return True
    else:
        return False