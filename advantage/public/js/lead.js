frappe.provide("advantage.utils");
frappe.ui.form.on("Lead", {
    onload_post_render(frm) {
         
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
    refresh(frm) {
		
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
