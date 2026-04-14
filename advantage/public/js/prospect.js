frappe.ui.form.on("Prospect", {
onload: function(frm) {
        
        frm.remove_custom_button('Customer', 'Create');
       
    },
    setup: function(frm) {
       
         
        frm.remove_custom_button('Customer', 'Create');
       
    },
    refresh: function(frm) {
        frm.remove_custom_button('Customer', 'Create');
    }

    }
         );