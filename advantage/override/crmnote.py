
from frappe import _
import frappe
from erpnext.crm.utils import CRMNote
from datetime import *

class AdvantageCRMNote(CRMNote):
    @frappe.whitelist()
    def delete_note(self, row_id):         
        if "Delete CRMNote" in frappe.get_roles():
            super().delete_note(row_id)
        else:
            frappe.throw(_("You haven't priviliage to delete this "))
                
                

    @frappe.whitelist()
    def edit_note(self, note, row_id): 
        note_doc=frappe.get_doc("CRM Note",{"name":row_id})
        if note_doc.added_by == frappe.session.user :
            diff=datetime.strptime(frappe.utils.now(), '%Y-%m-%d %H:%M:%S.%f')-note_doc.added_on
            minutes=frappe.get_single('Advantage Page Settings').minutes_change_note or 0
            if diff.total_seconds()  >= minutes*60 :
                frappe.throw(_("You can't edit note in this time"))
            else:
                super().edit_note(note, row_id)
        else:
            frappe.throw(_("You haven't priviliage to edit this "))
                
                
