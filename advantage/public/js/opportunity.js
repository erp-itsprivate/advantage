frappe.provide("advantage.utils");
function toggle_read_only(frm) {
    if (frm.doc.status !== 'Open') {
        frm.disable_form(true);
    } 
}
frappe.ui.form.on("Opportunity", {
    onload: function(frm) {
       
        advantage.utils.set_leaf_filter(frm, "territory");
        frm.doc.opportunity_type = "Sales";
        toggle_read_only(frm);
    },
    refresh: function(frm) {
       
        
        toggle_read_only(frm);
     
        frm.set_query("item_code", "items", function() {
            return {
                filters: {
                    custom_type: frm.doc.opportunity_type,
                    
                }
            };
        });
    
    }
});
