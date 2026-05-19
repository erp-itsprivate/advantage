
from frappe import _
import frappe
from erpnext.crm.utils import CRMNote
import erpnext.crm.utils
from datetime import *

class AdvantageCRMNote(CRMNote):
    @frappe.whitelist()
    def delete_note(self, row_id):         
        if "Delete CRMNote" in frappe.get_roles():
            super().delete_note(row_id)
        else:
            frappe.throw(_("You haven't priviliage to delete this "))
                
    @frappe.whitelist()
    def add_note(self, note: str):  
        super().add_note(note)
        #frappe.msgprint(_("You haven't priviliage to delete this "))
        from frappe.desk.doctype.notification_log.notification_log import enqueue_create_notification
        if self.doctype=="Opportunity" and self.custom_opportunity_cycle != "New" and self.opportunity_owner != frappe.session.user :
            email="""
                    <table style="width: 100%; border-collapse: collapse; border: 1px solid #ccc;">
                    <thead>
                        <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ccc; padding: 10px;">In English</th>
                        <th style="border: 1px solid #ccc; padding: 10px;">باللغة العربية</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                        <td dir="ltr" style="border: 1px solid #ccc; padding: 15px; text-align: left;">

                    Dear Mr/Ms. {{frappe.get_fullname(doc.opportunity_owner)}}

                    Please note that <b>{{frappe.get_fullname(frappe.session.user)}}</b> added a note to the opportunity: ({{doc.name}})
                    <br> <br>
                    <a href="{{frappe.utils.get_url_to_form(doc.doctype, doc.name)}}">Click here to view opportunity {{doc.name}}</a>
                    <br> <br>
                    Thanks

                        </td>
                        <td dir="rtl" style="border: 1px solid #ccc; padding: 15px; text-align: right;">

                    السيد(ة) {{frappe.get_fullname(doc.opportunity_owner)}}

                    يرجى اخذ العلم بانه قد تم اضافة ملاحظة من قبل <b>{{frappe.get_fullname(frappe.session.user)}}</b>
                    على الفرصة: ({{doc.name}}) 
                      <br> <br>
                    <a href="{{frappe.utils.get_url_to_form(doc.doctype, doc.name)}}">اضغط هنا لمشاهدة الفرصة {{doc.name}}</a>
                    <br> <br>
                    شكرا


                        </td>
                        </tr>
                    </tbody>
                    </table>
            """
            notification_doc = {
                        "type": "Mention",
                        "document_type": self.doctype,
                        "document_name":self.name,
                        "subject": "Change",
                        "from_user": frappe.session.user, #doc.modified_by or doc.owner,
                        "email_content":  frappe.render_template(email, {"doc":self}),
                        
                    }
            enqueue_create_notification(self.opportunity_owner, notification_doc)

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
                
                
erpnext.crm.utils.CRMNote = AdvantageCRMNote