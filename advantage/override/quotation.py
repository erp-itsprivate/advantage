
import frappe
from frappe import _
from erpnext.selling.doctype.quotation.quotation import Quotation

 
logger_exception = frappe.logger("advantage.error", allow_site=True, file_count=50)
logger_exception.setLevel(20)
logger = frappe.logger("advantage", allow_site=True, file_count=50)
logger.setLevel(20)
class AdvantageQuotation(Quotation): 
    def validate(self):
        super().validate()
        if not self.opportunity :
            frappe.throw(frappe._("You can't create a quotation  without opportunity"))
        else:
            opportunity=frappe.get_doc('Opportunity',self.opportunity)
            if opportunity.opportunity_owner != frappe.session.user:
                frappe.throw(frappe._("You can't create a quotation if you are not the opportunity owner"))
            if self.selling_price_list != opportunity.custom_price_list :
                frappe.throw(frappe._("You can't create quotation with different price list"))