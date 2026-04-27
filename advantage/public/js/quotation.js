frappe.ui.form.on("Quotation", {
	refresh: function (frm) {
         
        if (frm.doc.opportunity) {
           
            // Add a button under the "Links" or as a custom button
            frm.add_custom_button(__('Open Opportunity'), function() {
                // Route to the Opportunity document
                frappe.set_route('Form', 'Opportunity', frm.doc.opportunity);
            },__('Links')); // Adds it under a dropdown named "Links"
        }
    }
});