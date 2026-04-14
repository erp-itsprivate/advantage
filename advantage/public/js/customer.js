function init(frm) {
    // disable create connections 
    if (frm.dashboard && frm.dashboard.links_area) {
         
       frm.dashboard.links_area.wrapper.find('[data-doctype="Sales Order"] .btn-new').hide(); 
       frm.dashboard.links_area.wrapper.find('[data-doctype="Opportunity"] .btn-new').hide(); 
       frm.dashboard.links_area.wrapper.find('[data-doctype="Quotation"] .btn-new').hide(); 
       frm.dashboard.links_area.wrapper.find('[data-doctype="Delivery Note"] .btn-new').hide(); 
       
    }    
    // disable edit 
    if (frm.doc.account_manager !== frappe.session.user && frappe.user.has_role('CRM Sales Manager') == false  && frappe.user.has_role('CRM Finance') == false && frappe.user.has_role('System Manager') == false ) {
        frm.disable_form(true);
    }
}

frappe.ui.form.on("Customer", {
    onload: function(frm) {
        init(frm);
        
    },
    setup: function(frm) {
        init(frm);
    },
	refresh: function (frm) { 
        init(frm);
      
}


} );