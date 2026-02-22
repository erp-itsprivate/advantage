frappe.provide("advantage.utils");
frappe.ui.form.on("Opportunity", {
    onload: function(frm) {
       
        advantage.utils.set_leaf_filter(frm, "territory");
        frm.doc.opportunity_type = "Sales";
    }
});
