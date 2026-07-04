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
    custom_make_opportunity_for_customer: async function (frm){
          let mobile_no =frm.doc.mobile_no;
          let phone=frm.doc.phone;
           let phone_ext =frm.doc.phone_ext; 
            let whatsapp_no =frm.doc.whatsapp_no; 
            let email=frm.doc.email_id;
		let existing_customer = (
			await frappe.db.get_value(
				"Customer",
				{
					"lead_name": frm.doc.name,
				},
				"name"
			)
		).message.name;
		if (existing_customer){
		 
		 
			
			frappe.new_doc("Opportunity"); 
        frappe.ui.form.on("Opportunity", 
        { onload: function(frm) { 
           
          frm.doc.opportunity_from="Customer";
        frm.doc.party_name=existing_customer;
        frm.doc.phone=phone;
        frm.doc.phone_ext=phone_ext;
        frm.doc.whatsapp=whatsapp_no;
        frm.doc.contact_mobile=mobile_no;
        frm.doc.contact_email=email;
        frm.set_df_property("opportunity_from", "read_only", 1);
        frm.set_df_property("party_name", "read_only", 1);
		frm.set_df_property("phone", "read_only", 1);
		frm.set_df_property("phone_ext", "read_only", 1);
		frm.set_df_property("whatsapp", "read_only", 1);
		frm.set_df_property("contact_mobile", "read_only", 1);
		frm.set_df_property("contact_email", "read_only", 1);
           
           
        }
         
        });
		}
		
		
	},

	custom_make_opportunity: async function (frm) {
		let existing_prospect = (
			await frappe.db.get_value(
				"Prospect Lead",
				{
					lead: frm.doc.name,
				},
				"name",
				null,
				"Prospect"
			)
		).message.name;

		
		let existing_contact = (
			await frappe.db.get_value(
				"Contact",
				{
					first_name: frm.doc.first_name || frm.doc.lead_name,
					last_name: frm.doc.last_name,
				},
				"name"
			)
		).message.name;

		

		frappe.model.open_mapped_doc({
		method: "erpnext.crm.doctype.lead.lead.make_opportunity",
		frm: frm,
		});
		
	},
    onload_post_render(frm) {
        
        const original_add_button = frm.add_custom_button;
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
	validate: function(frm) {
        // 1. Get the value from the field (replace 'phone_field' with your actual field name)
        let moblie_no = frm.doc.mobile_no ;
        let prefix = "009639";
        let targetLength = 14; // The length of "00963997777073"
		let whatsapp_no =frm.doc.whatsapp_no;
        if (moblie_no) {
            // 2. Check if it starts with the specific prefix
            if (moblie_no.startsWith(prefix)) {
                
                // 3. Check if the length is exactly 14
                if (moblie_no.length !== targetLength) {
                    
                    // 4. Show error and stop the save
                    frappe.msgprint({
                        title: __('Invalid Moblie Number'),
                        indicator: 'blue',
                        message: __('Numbers starting with {0} must be exactly {1} digits long. Current length: {2}', 
                                    [prefix, targetLength, moblie_no.length])
                    });
                    
                    
                }
            }
        }
		 if (whatsapp_no) {
            // 2. Check if it starts with the specific prefix
            if (whatsapp_no.startsWith(prefix)) {
                
                // 3. Check if the length is exactly 14
                if (whatsapp_no.length !== targetLength) {
                    
                    // 4. Show error and stop the save
                    frappe.msgprint({
                        title: __('Invalid WhatsApp Number'),
                        indicator: 'blue',
                        message: __('Numbers starting with {0} must be exactly {1} digits long. Current length: {2}', 
                                    [prefix, targetLength, whatsapp_no.length])
                    });
                    
                    
                }
            }
        }

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
        setTimeout(() => {
           frm.remove_custom_button('Opportunity', 'Create'); 
        }, 10);
        if (!frm.is_new() && frm.doc.__onload && !frm.doc.__onload.is_customer) {
            setTimeout(() => {
    			frm.add_custom_button(
    				__("Opportunity"),
    				function () {
    					frm.trigger("custom_make_opportunity");
    				},
    				__("Create")
    			);
            }, 50);
        }
		if (!frm.is_new() && frm.doc.__onload && frm.doc.__onload.is_customer) {
            setTimeout(() => {
    			frm.add_custom_button(
    				__("Opportunity"),
    				function () {
    					frm.trigger("custom_make_opportunity_for_customer");
    				},
    				__("Create")
    			);
            }, 50);
        }
        frappe.call({
            method: "advantage.override.lead.get_cdr_html",
            args: {
                lead: frm.doc.name,     // ID of current document
              
            },
            callback: function(r) {
                if(r.message) {
                    // Set the HTML inside your HTML field (e.g., named 'cdr_display_field')
                    $(frm.fields_dict.custom_calls_log.wrapper).html(r.message);
                }
            }
        });
        if (frappe.user.has_role('CRM Manager') && !frm.is_new())  {
            frm.add_custom_button(__('Move CDRs'), function() {
                
                // 2. Create the Dialog
                let dialog = new frappe.ui.Dialog({
                    title: __('Select Target Lead'),
                    fields: [
                        {
                            label: __('Target Lead'),
                            fieldname: 'selected_lead',
                            fieldtype: 'Link',
                            options: 'Lead', // <--- Change this to the DocType you want to link to!
                            reqd: 1,          // Makes the field mandatory
                            description: __('Please select the record to process.')
                        }
                    ],
                    size: 'small', // Can be 'small', 'large', or 'extra-large'
                    primary_action_label: __('Submit Process'),
                    
                    // 3. This triggers when the user clicks "Submit Process" in the dialog
                    primary_action(values) {
                        console.log(values);
                        // Extract the selected value from the dialog
                        let selected_record = values.selected_lead;
                          
                        // 4. Call the backend Python script
                       frappe.call({
                            // REPLACE THIS PATH WITH YOUR ACTUAL PYTHON SCRIPT PATH
                            method: "advantage.override.lead.change_cdrs",
                            args: {
                                source_lead: frm.doc.name,     // ID of current document
                                target_lead: selected_record  // ID selected in the dialog
                            },
                            freeze: true,
                            freeze_message: __('Processing...'),
                            callback: function(response) {
                                if (!response.exc) { // If there are no Python errors
                                    // Close the dialog
                                    dialog.hide();
                                    
                                    // Show success alert
                                    frappe.show_alert({
                                        message: __('Successfully processed ' + selected_record),
                                        indicator: 'green'
                                    });
                                    
                                    // Reload form to show any backend changes
                                    frm.reload_doc();
                                }
                            }
                        }); 
                    }
                });
                
                // Show the dialog to the user
                dialog.show();
                
            });
        }

	}
    
});
