
import frappe
from frappe import _
from frappe.desk.doctype.event.event import Event
from advantage.utils import todo_event_additional_data
logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)


class AdvantageEvent(Event):
    def on_update(self):
        super().on_update()
        todo_event_additional_data(self)
         
        