frappe.provide("advantage.utils");
function init(frm) {
    // disable create connections 
    if (frm.dashboard && frm.dashboard.links_area) {
         
       frm.dashboard.links_area.wrapper.find('[data-doctype="Customer"] .btn-new').hide(); 
       frm.dashboard.links_area.wrapper.find('[data-doctype="Opportunity"] .btn-new').hide(); 
       frm.dashboard.links_area.wrapper.find('[data-doctype="Quotation"] .btn-new').hide(); 
       frm.dashboard.links_area.wrapper.find('[data-doctype="Prospect"] .btn-new').hide(); 
       
    }    
    // disable edit 
     
}

frappe.ui.form.on("Lead", {
    onload_post_render(frm) {
        frm.add_custom_button = function() {
            // Check if the first argument (the button name) is the one we want to hide
             
            if ( arguments[3] !== undefined && arguments[3] == true )
                return original_add_button.apply(frm, arguments);
            let arr=['Quotation','Customer','عرض أسعار','العميل']
            if ( arr.includes(arguments[0])  ) {
                 
                return null; // Block the button from being created!
            }
           
            // Otherwise, let Frappe create the button normally
            return original_add_button.apply(frm, arguments);
        };
		init(frm);
        frm.remove_custom_button('Quotation','Create'); 
        frm.remove_custom_button('Customer','Create'); 
        const forbidden_statuses1 = ['Do Not Contact'];
        if (forbidden_statuses1.includes(frm.doc.status)) {
              
            frm.remove_custom_button('Opportunity','Create'); 
       
        }
		if (!frm.doc.__islocal && frm.perm[0].write && frm.doc.docstatus == 0) {
			if (frm.doc.status === "Open") {
				frm.add_custom_button(__("Do Not Contact"), function () {
				    frm.set_value("status","Do Not Contact");
					
					frm.save();
				});
			} 
		}
        advantage.utils.set_leaf_filter(frm, "territory");
        
    },
	setup: function(frm) {
        init(frm);
    },
    refresh(frm) {
		init(frm);
        frm.remove_custom_button('Quotation','Create'); 
        
        frm.remove_custom_button('Customer','Create'); 
       
        const forbidden_statuses1 = ['Do Not Contact'];
        if (forbidden_statuses1.includes(frm.doc.status)) {
              
            frm.remove_custom_button('Opportunity','Create'); 
       
        }

		if (!frm.doc.__islocal && frm.perm[0].write && frm.doc.docstatus == 0) {
			if (frm.doc.status === "Open") {
				frm.add_custom_button(__("Do Not Contact"), function () {
				    frm.set_value("status","Do Not Contact");
					
					frm.save();
				});
			} 
		}
	}
});
