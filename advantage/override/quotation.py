
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
    
    @frappe.whitelist()
    def declare_enquiry_lost(
            self, lost_reasons_list: list, competitors: list, detailed_reason: str | None = None
        ):
            if not (self.is_fully_ordered() or self.is_partially_ordered()):
                get_lost_reasons = frappe.get_list("Quotation Lost Reason", fields=["name"])
                lost_reasons_lst = [reason.get("name") for reason in get_lost_reasons]
                self.db_set("status", "Lost")

                if detailed_reason:
                    self.db_set("order_lost_reason", detailed_reason)

                for reason in lost_reasons_list:
                    if reason.get("lost_reason") in lost_reasons_lst:
                        self.append("lost_reasons", reason)
                    else:
                        frappe.throw(
                            _("Invalid lost reason {0}, please create a new lost reason").format(
                                frappe.bold(reason.get("lost_reason"))
                            )
                        )

                for competitor in competitors:
                    self.append("competitors", competitor)

                #self.update_opportunity("Lost")
                #self.update_lead()
                self.save()

            else:
                frappe.throw(_("Cannot set as Lost as Sales Order is made."))
