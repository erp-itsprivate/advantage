frappe.provide("advantage.utils");
function toggle_read_only(frm) {
    if (frm.doc.status !== 'Open') {
        frm.disable_form(true);
    } 
    if (frm.doc.custom_opportunity_cycle !== 'New' && frm.doc.opportunity_owner !== frappe.session.user && frappe.session.user !=='Administrator' ) {
        frm.disable_form(true);
        frappe.show_alert({
            message: __("Only opportunity owner can edit"),
            indicator: 'orange'
        }, 3);
    } 
}
function get_item_rate(frm, cdt, cdn) {
    try {
        const row = locals[cdt][cdn];
        const price_list = frm.doc.custom_price_list;

        if (!row?.item_code || !price_list) return;

        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                doctype: 'Item Price',
                filters: {
                    item_code: row.item_code,
                    price_list: price_list
                },
                fieldname: 'price_list_rate'
            },
            callback: function(res) {
                const rate = res?.message?.price_list_rate;

                if (rate) {
                    frappe.model.set_value(cdt, cdn, 'rate', rate);
                } else {
                    frappe.show_alert({
                        message: __(`No price found for {0} in {1}`, [row.item_code, price_list]),
                        indicator: 'orange'
                    });
                    frappe.model.set_value(cdt, cdn, 'rate', 0);
                }
            }
        });

    } catch (err) {
        console.error("Error in get_item_rate:", err);
    }
}

frappe.ui.form.on("Opportunity", {
    onload_post_render(frm) {
        frm.remove_custom_button('Customer', 'Create');
        frm.remove_custom_button('Supplier Quotation','Create'); 
        frm.remove_custom_button('Request For Quotation','Create'); 
        frm.remove_custom_button('Close'); 
    },
    onload: function(frm) {
       
        advantage.utils.set_leaf_filter(frm, "territory");
        frm.doc.opportunity_type = "Sales";
        frm.remove_custom_button('Customer', 'Create');
        frm.remove_custom_button('Supplier Quotation','Create'); 
        frm.remove_custom_button('Request For Quotation','Create'); 
        frm.remove_custom_button('Close'); 
       // toggle_read_only(frm);
        frm.set_df_property('items', 'cannot_add_rows', false);
        frm.get_docfield('items', 'rate').read_only = 1;
    },
    setup: function(frm) {
       
        advantage.utils.set_leaf_filter(frm, "territory");
        frm.doc.opportunity_type = "Sales";
        frm.remove_custom_button('Customer', 'Create');
        frm.remove_custom_button('Supplier Quotation','Create'); 
        frm.remove_custom_button('Request For Quotation','Create'); 
        frm.remove_custom_button('Close'); 
        //toggle_read_only(frm);
        frm.set_df_property('items', 'cannot_add_rows', false);
        frm.get_docfield('items', 'rate').read_only = 1;
    },
    status: function(frm) {
        // Run when status changes
        toggle_read_only(frm);
    },
    refresh: function(frm) {
        if (frm.is_new()) {
            frm.set_value('opportunity_owner', frappe.session.user);
        }
        frm.set_query('custom_price_list', () => ({
            filters: {
                currency: frm.doc.currency,
                enabled: 1
            }
        }));
        console.log(frm.doc.opportunity_type);
        console.log(frm.doc.custom_domain);
        console.log(frm.doc.opportunity_owner) ;
        frm.remove_custom_button('Customer', 'Create');
        frm.remove_custom_button('Supplier Quotation','Create'); 
        frm.remove_custom_button('Request For Quotation','Create'); 
        frm.remove_custom_button('Close'); 
        toggle_read_only(frm);
        
        frm.set_query("item_code", "items", function() {
            return {
                filters: {
                    custom_type: frm.doc.opportunity_type,
                    
                }
            };
        });
        const forbidden_statuses = ['Lost', 'Closed'];
        if (forbidden_statuses.includes(frm.doc.status))
        {
            frm.remove_custom_button('Customer','Create'); 
        }
        const forbidden_statuses1 = ['Converted', 'Handed Over','Closed','New'];
        if (forbidden_statuses1.includes(frm.doc.custom_opportunity_cycle) || frm.doc.opportunity_owner != frappe.session.user) 
        {
            frm.remove_custom_button('Quotation','Create'); 
        }
    },
    currency(frm) {
        // Clear price list
        if (frm.doc.custom_price_list) {
            frm.set_value('custom_price_list', '');
            frappe.show_alert(__('Price List cleared as it may not match the new currency.'));
        }

        // Clear items safely
        try {
            if (frm.doc.items?.length > 0) {
                frappe.model.clear_table(frm.doc, 'items');
                frm.refresh_field('items');
                frappe.show_alert(__('Items removed because currency changed.'));
            }
        } catch (err) {
            console.error("Error clearing items on currency change:", err);
        }
    },

    // When price list changes
    custom_price_list(frm) {
        try {
            if (frm.doc.custom_price_list && frm.doc.items?.length) {
                frm.doc.items.forEach(row => {
                    get_item_rate(frm, row.doctype, row.name);
                });
            }
        } catch (err) {
            console.error("Error updating item rates:", err);
        }
    }
});
frappe.ui.form.on('Opportunity Item', {

    item_code(frm, cdt, cdn) {
        try {
            get_item_rate(frm, cdt, cdn);
        } catch (err) {
            console.error("Error fetching item rate:", err);
        }
    },

    items_add(frm) {
        try {
            if (!frm.doc.custom_price_list) {

                // Remove all items safely
                frappe.model.clear_table(frm.doc, 'items');
                frm.refresh_field('items');

                frappe.msgprint({
                    title: __('Warning'),
                    indicator: 'red',
                    message: (__('Please select a Price List before adding items.'))
                });

                throw new Error(__("Price List required"));
            }
        } catch (err) {
            
        }
    }
});