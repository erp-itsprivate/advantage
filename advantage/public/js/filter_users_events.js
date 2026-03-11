// apps/your_app/your_app/public/js/custom_communication.js

// Ensure the original class is loaded before we try to extend it
$(document).ready( function() {
    
    if (frappe.views.InteractionComposer ) {
        console.log("InteractionComposer");
        // 1. Save the original class reference (optional, if you need super calls)
        const OriginalComposer = frappe.views.InteractionComposer ;

        // 2. Override the class directly in the global namespace
        frappe.views.InteractionComposer  = class CustomInteractionComposer   extends OriginalComposer {
            
            // Example 1: Overriding the 'make' function (Initial rendering)
            get_fields() {
                let me=this;
                // Call the original logic first
                let fields = super.get_fields();
                
               
                let senderIndex = fields.findIndex(f => f.fieldname === 'assigned_to');
                if (senderIndex !== -1) {
                    let a={
                        label: __("Assigned To"),
                        fieldtype: "Link",
                        fieldname: "assigned_to",
                        options: "User",
                        get_query: function () {
                            return { query: "advantage.utils.get_user_same_company" };
                        },
                    };
                     
                    fields[senderIndex] = a;
                }
                
               
                return fields;
               
                // Add your custom logic here
                // Example: Pre-fill the subject field differently
                // this.dialog.set_value('subject', 'Custom Subject Prefix: ');
            }

           
        };
    }
});