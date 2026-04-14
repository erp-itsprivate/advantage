
import frappe
from frappe import _
from frappe.desk.doctype.event.event import Event
from frappe.utils import get_datetime

from advantage.utils import todo_event_additional_data
logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)


class AdvantageEvent(Event):
        
    def on_update(self):
        #super().on_update()
        if len(frappe.get_all('ToDo', filters=[["reference_type",'=','Event'],['reference_name','in',self.name]])) > 0 :
            for todo in frappe.get_all('ToDo', filters=[["reference_type",'=','Event'],['reference_name','in',self.name]]):
                todo_doc=frappe.get_doc('ToDo',todo.name)
                todo_doc.date=get_datetime(self.starts_on).date()
            
                todo_doc.save()  
                todo_event_additional_data(self)      
        #     frappe.db.commit() 
        
         
        