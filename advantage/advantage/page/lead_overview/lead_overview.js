frappe.pages['lead-overview'].on_page_load = function(wrapper) {
    
/*	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Lead Overview"),
		single_column: true
	});
	*/
	//$(frappe.render_template("lead_overview")).appendTo(page.main);

	// Hide Page Title
    //

	/*page.wrapper.find('.page-body').css({
        'max-width': '100% !important',
    'display': 'flex',
    'flex-direction': 'row',
    'flex-shrink': '0',
    'height': 'fit-content',
    'width': '100%',
    'overflow': 'hidden',
    'position': 'relative',
    'flex-wrap': 'wrap',
    'padding': '5px !important',
    });
    */
    // Optional: Remove default padding from the page body
    //page.wrapper.find('.page-body').css({
    //    'min-height': 'calc(100vh - 100px)' // Ensure full height usage
    //});
	//$('header.navbar').hide();
  

    // 3. Register the Shortcut (Ctrl+S)
    function isNumberString(value) {
        return /^\d+$/.test(value);
      }
      
    
    let route = frappe.get_route(); 
    
    // route[0] is 'my-custom-page'
    // route[1] is 'detail-view' (passed parameter)
    // route[2] is '1050' (passed parameter)
    let lead_summary = new LeadOverview(wrapper);
    //
    if (route[1]) {
        console.log("View:", route[1]);
        if (isNumberString(route[1]) )
        {
            lead_summary.mobile_no_field.set_value(route[1]);
            lead_summary.mobile_no_field.df.read_only = 1;
           // lead_summary.lead_field.df.read_only = 1;
            lead_summary.mobile_no_field.refresh();
            lead_summary.lead_field.refresh();
         
            //lead_summary.has_unsaved_changes=true;
            lead_summary.setup_browser_guard();
            //lead_summary.mobile_no_field.set_disabled(true);
        }
        else if ( route[1] != "NA" && route[1] != "Unknown" ) {
        lead_summary.lead_field.set_value(route[1]);
        lead_summary.refresh_data(route[1],wrapper);
        }
        // Run your logic here
    }
    // if (route[2])
    // {
    //     console.log("View:", route[2]);
    //     lead_summary.company_field.df.read_only = 1;
    //     lead_summary.company_field.refresh();
        

    // }
    // Remove spacing
    //$('.page-container').css('padding-top', '0');
   
}
LeadOverview = class {
    constructor(wrapper) {
        this.is_programmatic_update = false; 
        this.has_unsaved_changes=false;
        this.lead_field=null;
        this.wrapper = wrapper;
        this.is_cleared=false;
        this.last_lead_value = null; 
        this.page = frappe.ui.make_app_page({
            parent: this.wrapper,
            title: __('Lead Overview'),
            single_column: true
        });
       this.page.wrapper.find('.page-head').hide();
         this.customer=null;
        this.is_dirty=false;
        // 2. Render Content
        this.render();
        // $(wrapper).find('.page-body').css({
            

        //     'max-width': '100% !important',
        //     'display': 'flex',
        //     'flex-direction': 'row',
        //     'flex-shrink': '0',
        //     'height': 'fit-content',
        //     'width': '100%',
        //     'overflow': 'hidden',
        //     'position': 'relative',
        //     'flex-wrap': 'wrap',
        //     'padding': '5px !important'
        // });
        // 3. Setup Buttons
    

        // 4. Setup Keyboard Shortcuts
        this.setup_shortcuts();
        this.watch_changes();
        this.setup_browser_guard();
      //this.wrapper = $(wrapper).find(".layout-main-section");
      this.market_segment_field = frappe.ui.form.make_control(
        { df:
            { fieldname: 'market_segment',
              label:__('Market Segment'),
              fieldtype: 'Link', 
              options: 'Market Segment' ,
              
            }, 
            parent: $(this.wrapper).find("#market_segment"), 
            
            render_input: true       
        });

    this.gender_field=frappe.ui.form.make_control(
        { df:
            { fieldname: 'gender',
              label:__('Gender'),
              fieldtype: 'Link', 
              options: 'Gender' ,
               
              
            }, 
            parent: $(this.wrapper).find("#gender"), 
            
            render_input: true       
        });
        this.company_field=frappe.ui.form.make_control(
            { df:
                { fieldname: 'company',
                  label:__('Company'),
                  fieldtype: 'Link', 
                  options: 'Company' ,
                  reqd:'1',
                  read_only:1
                   
                  
                }, 
                parent: $(this.wrapper).find("#company"), 
                
                render_input: true       
            });
            this.first_name_field=frappe.ui.form.make_control(
                { df:
                    { fieldname: 'first_name',
                      label:__('First Name'),
                      fieldtype: 'Data', 
                      
                      reqd:'1'
                      
                    }, 
                    parent: $(this.wrapper).find("#first_name"), 
                    
                    render_input: true       
                });
                this.last_name_field=frappe.ui.form.make_control(
                    { df:
                        { fieldname: 'last_name',
                          label:__('Last Name'),
                          fieldtype: 'Data', 
                          
                          reqd:'1'
                          
                        }, 
                        parent: $(this.wrapper).find("#last_name"), 
                        
                        render_input: true       
                    });
                    this.job_title_field=frappe.ui.form.make_control(
                        { df:
                            { fieldname: 'job_title',
                              label:__('Job Title'),
                              fieldtype: 'Data'
                              
                            }, 
                            parent: $(this.wrapper).find("#job_title"), 
                            
                            render_input: true       
                        });
                        this.organization_field=frappe.ui.form.make_control(
                            { df:
                                { fieldname: 'organization',
                                  label:__('Organization'),
                                  fieldtype: 'Data'
                                  
                                }, 
                                parent: $(this.wrapper).find("#organization"), 
                                
                                render_input: true       
                            });
                            
        this.mobile_no_field=frappe.ui.form.make_control(
            { df:
                { fieldname: 'mobile_num',
                  label:__('Mobile Number'),
                  fieldtype: 'Data',
                  reqd:'1',
                  
                  
                }, 
                parent: $(this.wrapper).find("#mobile_num"), 
                
                render_input: true       
            });
            
            
         
            this.phone_no_field=frappe.ui.form.make_control(
                { df:
                    { fieldname: 'phone_num',
                      label:__('Phone Number'),
                      fieldtype: 'Data'
                      
                    }, 
                    parent: $(this.wrapper).find("#phone_num"), 
                    
                    render_input: true       
                });
                this.whatsapp_field=frappe.ui.form.make_control(
                    { df:
                        { fieldname: 'whatsapp',
                          label:__('WhatsApp'),
                          fieldtype: 'Data'
                          
                        }, 
                        parent: $(this.wrapper).find("#whatsapp"), 
                        
                        render_input: true       
                    });
                
                    this.email_field=frappe.ui.form.make_control(
                        { df:
                            { fieldname: 'email',
                              label:__('Email'),
                              fieldtype: 'Data'
                              
                            }, 
                            parent: $(this.wrapper).find("#email"), 
                            
                            render_input: true       
                        });    
        this.industry_field=frappe.ui.form.make_control(
                { df:
                    { fieldname: 'industry',
                      label:__('Industry'),
                      fieldtype: 'Link', 
                      options: 'Industry Type' ,
                      
                      
                    }, 
                    parent:$(this.wrapper).find("#industry"), 
                    
                    render_input: true       
                });
        this.territory_field=frappe.ui.form.make_control(
            { df:
                { fieldname: 'territory',
                    label:__('Territory'),
                    fieldtype: 'Link', 
                    options: 'Territory' ,
                    get_query: function() {
                        return {
                            filters: {
                                is_group : "0"
                            }
                        };
                    }
                    
                }, 
                parent: $(this.wrapper).find("#territory"), 
                
                render_input: true       
            });
            this.birth_date_field=frappe.ui.form.make_control(
                { df:
                    { fieldname: 'birth_date',
                        label:__('Birth Date'),
                        fieldtype: 'Date', 
                      
                        
                        
                    }, 
                    parent: $(this.wrapper).find("#birth_date"), 
                    
                    render_input: true       
                });    
               this.company_field.set_value(frappe.defaults.get_default("company"));
      this.init(wrapper);
     
     
    }
    watch_changes() {
        // Listen for 'change' or 'input' on all form elements inside this page
        // Arrow function ensures 'this' refers to the Class
        $(this.wrapper).on('change input', '.custom-form-input', (mm) => {
           
            console.log(this.is_programmatic_update);
            console.log(this.has_unsaved_changes);
            console.log(mm);
            if (this.is_programmatic_update) {
             

                return;
            }
            if (!this.has_unsaved_changes) {
                this.has_unsaved_changes = true;
                this.setup_actions();
                this.page.set_indicator('Not Saved', 'orange'); // Visual cue
                console.log('Form is dirty');
            }
        });
    }
    setup_browser_guard() {
        // This event fires when closing tab, refreshing, or navigating to Google.com
        window.addEventListener('beforeunload', (e) => {
            
            // Only trigger if we have changes AND this page is currently visible
            if (this.has_unsaved_changes && $(this.wrapper).is(':visible')) {
                // Cancel the event
                e.preventDefault(); 
                
                // Chrome requires returnValue to be set
                e.returnValue = ''; 
                
                // Legacy browsers show this message, modern ones show a generic message
            return "You have unsaved changes. Are you sure you want to leave?";
            }
        });
    }
    render() {
        // Example content
        $(frappe.render_template("lead_overview")).appendTo(this.page.main);
      
       
        
    }

    setup_actions() {
        // Add the primary button to the top right
        // We use arrow function () => to keep 'this' bound to the class
        $(this.wrapper).find("#save_button").removeClass("hidden");
        $(this.wrapper).find("#save_button").off('click').on('click', () => {
            this.save_data();
        });
        //this.page.set_primary_action(__('Save'), () =>this.add_opportunities(this.lead_field.get_value()) );
        //this.save_data()
    }
    add_mintenance()
    {
         
        if (this.lead_field.get_value() != "" && this.lead_field.get_value() != undefined )
        {
            if (this.customer != null)
            {
                 
                let party_name=this.customer.name
                frappe.new_doc("Maintenance Visit"); 
                frappe.ui.form.on("Maintenance Visit", 
                { onload: function(frm) { 
                
                    
                    frm.set_value("customer", party_name);
                    frm.set_df_property("customer", "read_only", 1);
            
                
                    
                
                
                
                }
                
                });
            }
        
        }
    }
    add_opportunities()
    {   
         let me=this;
         let party_name=null;
         let type=null;
      
        if (me.lead_field.get_value() != "" && me.lead_field.get_value() != undefined )
        {
            party_name=me.lead_field.get_value();
             type="Lead";
            if (me.customer != null)
            {
                type="Customer";
                party_name=this.customer.name
            }
        frappe.route_options = {}; 
        frappe.new_doc("Opportunity",{
            "opportunity_from":type,
            
        });
        frappe.ui.form.on("Opportunity", 
        { onload: function(frm) { 
           
            console.log(party_name);
           
                frm.set_value("party_name", party_name).then(() => {
                    
                    frm.set_df_property("party_name", "read_only", 1);
                    frm.refresh_field("party_name"); 
                    console.log(frm.doc)
                }); 
           
            //frm.set_df_property("opportunity_from", "read_only", 1);
           // frm.refresh();
          
            
            
           
        }
         
        });
        }
    }
      async save_data()
    {
        let me=this;
        let lead_source;
        console.log('save');
        if (frappe.defaults.get_default("lead_source") != undefined )
        {
            lead_source=frappe.defaults.get_default("lead_source");
        }
        console.log(lead_source);
        if ( this.has_unsaved_changes == true )
        {
            const mandatory_fields = [
                { field: this.first_name_field, label: __('First Name') },
                { field: this.last_name_field,  label: __('Last Name') },
                { field: this.mobile_no_field,  label: __('Mobile') }
            ];
            
            for (let item of mandatory_fields) {
                if (!item.field.get_value()) {
                    frappe.throw(__('{0} is mandatory', [item.label]));
                    // The script stops here immediately after the first error
                }
            }
        let lead = { lead_id: this.lead_field.get_value() || "NA", 
        market_segment: this.market_segment_field.get_value(), 
        gender: this.gender_field.get_value(),
        company: this.company_field.get_value(),
        first_name: this.first_name_field.get_value(),
        last_name:this.last_name_field.get_value(),
        job_title :  this.job_title_field.get_value(),
        organization :this.organization_field.get_value() ,
        mobile_no : this.mobile_no_field.get_value(),
        phone_no :this.phone_no_field.get_value(),
        whatsapp : this.whatsapp_field.get_value(),
        email : this.email_field.get_value(),
        industry : this.industry_field.get_value(),
        territory : this.territory_field.get_value(),
        birth_date :this.birth_date_field.get_value(),
        source : lead_source
        };
         
       
         frappe.call({
            method: 'advantage.advantage.page.lead_overview.lead_overview.save_lead',
            args: {
                'lead': lead
            },
            async :false,
            callback: function(r) {
                if (r && r.message) 
                {
                me.has_unsaved_changes = false;
                me.page.set_indicator('', '');
                frappe.show_alert({message: __('Saved Successfully'), indicator: 'green'});
                me.empty_fields(me.wrapper);
                
                me.lead_field.set_value(r.message);
                me.lead_field.refresh();
                } 
            }
        });
        
       
        
        // 3. Visual Feedback
       
     }
     else 
     {
        frappe.show_alert({message: __('No Changes Found'), indicator: 'orange'});
     }
    }
    setup_shortcuts() {
        frappe.ui.keys.add_shortcut({
            shortcut: 'ctrl+s',
            action: (e) => {
                // Prevent browser save dialog
                e.preventDefault();
                e.stopPropagation();

                // CRITICAL: Only run if this specific page is currently visible.
                // Frappe keeps pages in the DOM even when you navigate away.
                if ($(this.wrapper).is(':visible')) {
                    this.save_data();
                   
                }
                
                return false;
            },
            description: __('Save Data')
        })}
   
    
    refresh_data(ff,wrapper){
        let me=this;
   
        if (ff.value != "")
        {
            frappe.call({
                method: 'advantage.advantage.page.lead_overview.lead_overview.get_lead_info',
                args: {
                    'lead': ff
                },
                callback: function(r) {
                    if (r.message) {
                        // Render template with new data
                      
                      
                        me.is_programmatic_update=true;
                       
                        // Update DOM
                        $(wrapper).find("#events").html(r.message[0]);
                        $(wrapper).find("#product").html(r.message[1]);
                        $(wrapper).find("#issues").html(r.message[2]);
                        $(wrapper).find("#notes").html(r.message[3]);
                        $(wrapper).find("#activity").html(r.message[9]);
                        $(wrapper).find('#critical_lead_notes').html(r.message[8]);
                        $(wrapper).find("#main-opportunity").html(r.message[5]);
                        $(wrapper).find("#main-maintenance").html(r.message[6]);
                        me.birth_date_field.set_value(r.message[4].custom_birth_date);
                        me.market_segment_field.set_value(r.message[4].market_segment);
                        me.gender_field.set_value(r.message[4].gender);
                        me.company_field.set_value(r.message[4].company);
                        me.industry_field.set_value(r.message[4].industry);
                        me.territory_field.set_value(r.message[4].territory);
                        me.phone_no_field.set_value(r.message[4].phone);
                        $(wrapper).find("#industry").val(r.message[4].industry);
                       
                       
                        me.job_title_field.set_value(r.message[4].job_title);
                        me.first_name_field.set_value(r.message[4].first_name);
                        me.last_name_field.set_value(r.message[4].last_name);
                        me.organization_field.set_value(r.message[4].company_name);
                        $(wrapper).find("#full_name").val(r.message[4].lead_name);
                        me.mobile_no_field.set_value(r.message[4].mobile_no);
                        me.customer=r.message[7];
                     
                        me.whatsapp_field.set_value(r.message[4].whatsapp_no);
                        
                     
                        me.email_field.set_value(r.message[4].email_id);

                        $(wrapper).find("#qualification_status").removeClass("hidden");
                        $(wrapper).find("#status").removeClass("hidden");
                        $(wrapper).find("#lead_owner").removeClass("hidden");
                        
                        $(wrapper).find("#qualification_status").text(__(r.message[4].qualification_status));
                        $(wrapper).find("#status").text(__(r.message[4].status));
                      
                        $(wrapper).find("#add_opportunity_button").removeClass("hidden");
                        $(wrapper).find("#add_opportunity_button").off('click').on('click', () => {
                           
                             me.add_opportunities();
                             
                        }); 
                        $(wrapper).find("#add_mintenance_button").removeClass("hidden");
                        $(wrapper).find("#add_mintenance_button").off('click').on('click', () => {
                            
                             me.add_mintenance();
                             
                        }); 
                        
                      
                                     
                        $(wrapper).find("#status").addClass('gray');
                        if (r.message[4].status=="Open")
                        {
                            $(wrapper).find("#status").removeClass('gray');
                            $(wrapper).find("#status").addClass('red');
                        }
                        if (r.message[4].status=="Converted")
                        {
                            $(wrapper).find("#maintenance_tab").removeClass("hidden");
                            $(wrapper).find("#status").removeClass('gray');
                            $(wrapper).find("#status").addClass('green');
                        }
                         
                        $(wrapper).find("#lead_owner").text(r.message[4].lead_owner);
                        setTimeout(() => {
                            me.is_programmatic_update = false; // Unlock
                             
                        }, 10);
                        me.add_product(wrapper);
                        me.add_event(wrapper);
                        me.add_issue(wrapper);
                        me.add_note(wrapper);
                    }
                }
            });
        }
        else {
            this.empty_fields(wrapper);
        }
    }
    add_event(wrapper){
        let me=this;
        let mock_frm = {
            
            doc: {
                doctype: "Lead",
                name: me.lead_field.get_value(),
            
                
                
            },
          
        };
        let _create_event = () => {
            const args = {
                doc: me.lead_field.get_value(),
                frm: mock_frm,
                title: __("New Event"),
            };
            class ExtendedClass extends  frappe.views.InteractionComposer {  create_action() { 
                
                 super.create_action(); // "Data loaded!" });
                 setTimeout(() => {   frappe.call({
                    method: 'advantage.advantage.page.lead_overview.lead_overview.render_event',
                    args: {
                        'lead': me.lead_field.get_value(),
                      
                        
                        
                    },
                    callback: function(r) {
                        if (r.message) {
                            
                          // $(wrapper).find("#product").empty();
                          $(wrapper).find("#events").html(r.message);
                            
                        }
                    }
                }); }, 1000);
              
            
            } }
            let composer = new ExtendedClass(args);
            composer.dialog.get_field("interaction_type").set_value("Event");
         
          
            $(composer.dialog.get_field("interaction_type").wrapper).hide();
         
            
        };
        $(wrapper).find("#add_event").off('click').on('click', _create_event);
    }   
    add_product(wrapper){
        let me=this;
        
        $(wrapper).find("#add_product").off('click').on('click', function() {
             
            let d = new frappe.ui.Dialog({
                title: __("Add Owned Product"),
                fields: [
                    {
                        label: __("Product"),
                        fieldname: "product_name",
                        fieldtype: "Data",
                        reqd:1
                       
                    },
                    {
                        label: __("Buy Date"),
                        fieldname: "buy_date",
                        fieldtype: "Date",
                        reqd:1
                    },
                    {
                        label: __("Company Product"),
                        fieldname: "is_company_brand",
                        fieldtype: "Check",
                       
                    }
                ],
                primary_action_label: __("Confirm"),
                primary_action(values) {
                    // frappe.call({
                    //     method: 'advantage.advantage.page.lead_overview.lead_overview.add_product',
                    //     args: {
                    //         'lead': me.lead_field.get_value(),
                    //         'data_':values
                            
                            
                    //     },
                    //     callback: function(r) {
                    //         if (r.message) {
                    //             console.log(r.message); 
                    //           // $(wrapper).find("#product").empty();
                    //           $(wrapper).find("#product").html(r.message);
                                
                    //         }
                    //     }
                    // });
                    values.doctype="Advantage Products";
                    values.parentfield="custom_products";
                    values.parent=me.lead_field.get_value();
                    values.parenttype="Lead";
                    
                    frappe.call({
                        method: "frappe.client.insert",
                        args: { doc: values },                    
                        callback: function (r) {
                            if (!r.exc) {
                                
                                frappe.call({
                                        method: 'advantage.advantage.page.lead_overview.lead_overview.render_products',
                                        args: {
                                            'lead': values.parent
                                            
                                            
                                            
                                        },
                                        callback: function(r) {
                                            if (r.message) {
                                              
                                              // $(wrapper).find("#product").empty();
                                              $(wrapper).find("#product").html(r.message);
                                                
                                            }
                                        }
                                    });
                            
                            } else {
                                frappe.msgprint(
                                    __("There were errors while creating the document. Please try again.")
                                );
                            }
                        },
                    });
                    d.hide();
                }
            });
            
            d.show();
            
        });
    }
    add_note(wrapper)
    {
        let me=this;
        let _add_note = () => {
			var d = new frappe.ui.Dialog({
				title: __("Add a Note"),
				fields: [
					{
						label: "Note",
						fieldname: "note",
						fieldtype: "Text Editor",
						reqd: 1,
						enable_mentions: true,
					},
				],
                primary_action(values) {
                    
                    values.doctype="CRM Note"                 
                    values.parentfield="notes";
                    values.parent=me.lead_field.get_value();
                    values.parenttype="Lead";
                    values.added_on= frappe.datetime.now_datetime();
                    values.added_by=frappe.session.user;
                    frappe.call({
                        method: "frappe.client.insert",
                        args: { doc: values },                    
                        callback: function (r) {
                            if (!r.exc) {
                                frappe.call({
                                    method: 'advantage.advantage.page.lead_overview.lead_overview.render_notes',
                                    args: {
                                        'lead': values.parent
                                        
                                        
                                        
                                    },
                                    callback: function(r) {
                                        if (r.message) {
                                            
                                          // $(wrapper).find("#product").empty();
                                          $(wrapper).find("#notes").html(r.message);
                                            
                                        }
                                    }
                                });
                            
                            } else {
                                frappe.msgprint(
                                    __("There were errors while creating the document. Please try again.")
                                );
                            }
                        },
                    });
                    d.hide();
                },
				primary_action_label: __("Add"),
			});
			d.show();
		};
		$(wrapper).find("#add_note").off('click').on('click', _add_note);
    }
    add_issue(wrapper){
        let me=this;
        let _add_issue = () => {let d = new frappe.ui.Dialog({
            title: __("Add Issue"),
            fields: [
                {
                    label: __("Subject"),
                    fieldname: "subject",
                    fieldtype: "Data",
                    reqd:1
                   
                },
                {
                    label: __("Priority"),
                    fieldname: "priority",
                    fieldtype: "Link",
                    options: "Issue Priority",
                    reqd:1
                },
                {
                    label: __("Issue Type"),
                    fieldname: "issue_type",
                    fieldtype: "Link",
                    options:"Issue Type"
                   
                },
                {
                    label: __("Description"),
                    fieldname: "description",
                    fieldtype: "Text Editor",
                    options:"Issue Type",
                    enable_mentions: true,
                    reqd:1
                   
                },
                {
                    label: __("Lead"),
                    fieldname: "lead",
                    fieldtype: "Link",
                    options:"Lead",
                    hidden:1,
                    read_only:1,
                    default :me.lead_field.get_value()
                }
            ],
            primary_action_label: __("Confirm"),
            primary_action(values) {
                
                values.doctype="Issue"
                frappe.call({
                    method: "frappe.client.insert",
                    args: { doc: values },                    
                    callback: function (r) {
                        if (!r.exc) {
                            frappe.call({
                                method: 'advantage.advantage.page.lead_overview.lead_overview.render_issues',
                                args: {
                                    'lead': values.lead
                                    
                                    
                                    
                                },
                                callback: function(r) {
                                    if (r.message) {
                                        
                                      // $(wrapper).find("#product").empty();
                                      $(wrapper).find("#issues").html(r.message);
                                        
                                    }
                                }
                            });
                        
                        } else {
                            frappe.msgprint(
                                __("There were errors while creating the document. Please try again.")
                            );
                        }
                    },
                });
                d.hide();
            }
        });
        
        d.show();}
        $(wrapper).find("#add_issue").off('click').on('click', _add_issue);
    }
    empty_fields(wrapper)
    {
        let me=this;
        $(wrapper).find("#events").empty();
        $(wrapper).find("#product").empty();
        $(wrapper).find("#issues").empty();
        $(wrapper).find("#notes").empty();    
        $(wrapper).find("#main-opportunity").empty();
        $(wrapper).find("#critical_lead_notes").empty();
        $(wrapper).find("#activity").empty();
        $(wrapper).find("#main-maintenance").empty();
        me.market_segment_field.set_value('');
        me.industry_field.set_value('');
        
         
    //    me.gender_field.$wrapper.addClass('has-error');       
    //    me.gender_field.$input.val('');
       me.gender_field.set_value('');
    
        me.company_field.$wrapper.addClass('has-error');    
           
       

        me.first_name_field.$wrapper.addClass('has-error');    
        me.first_name_field.$input.val('');
        me.last_name_field.$wrapper.addClass('has-error');    
        me.last_name_field.$input.val('');
        me.territory_field.set_value('');
        $(wrapper).find("#industry").val("");
        
      
        me.organization_field.set_value('');
        me.job_title_field.set_value('');
        me.birth_date_field.set_value('');
        
        me.mobile_no_field.$wrapper.addClass('has-error');    
        me.mobile_no_field.$input.val('');


        $(wrapper).find("#full_name").val("");
        
        
        me.phone_no_field.set_value('');
        me.whatsapp_field.set_value('');
        
        
        me.email_field.set_value('');

        $(wrapper).find("#qualification_status").addClass("hidden");
        $(wrapper).find("#status").addClass("hidden");
        $(wrapper).find("#status").removeClass("red");
        $(wrapper).find("#status").removeClass("gray");
        $(wrapper).find("#status").removeClass("green");
        $(wrapper).find("#lead_owner").addClass("hidden");
        $(wrapper).find("#maintenance_tab").addClass("hidden");
        $(wrapper).find("#save_button").addClass("hidden");
        $(wrapper).find("#add_opportunity_button").addClass("hidden");
        $(wrapper).find("#add_mintenance_button").addClass("hidden");
        
      
        
        
    }
    async init(wrapper) {  
    
      var me = this;
      $(me.wrapper).find("#main-opportunity")[0].style.display = "none";
       
      // make expand action
      $(me.wrapper).find("#expand")[0].addEventListener(
        "click",
        function () {
         
          if ($(this).find("#expand_icon")[0].getAttribute("href") === "#es-line-sidebar-expand") {
            $(this).find("#expand_icon")[0].setAttribute("href", "#es-line-sidebar-collapse");
            $(me.wrapper).find("#left_side")[0].style.display = "none";
          } else {
            $(this).find("#expand_icon")[0].setAttribute("href", "#es-line-sidebar-expand");
            $(me.wrapper).find("#left_side")[0].style.display = "";
          }
         
        }
      );
      $(me.wrapper).find("#expand_information")[0].addEventListener(
        "click",
        function () {
         
          if ($(this).find("#expand_information_icon")[0].getAttribute("href") === "#es-line-up") {
            $(this).find("#expand_information_icon")[0].setAttribute("href", "#es-line-down");
            $(me.wrapper).find("#lead_info_section")[0].style.display = "none";
          } else {
            $(this).find("#expand_information_icon")[0].setAttribute("href", "#es-line-up");
            $(me.wrapper).find("#lead_info_section")[0].style.display = "";
          }
         
        }
      );
      $(me.wrapper).find("#expand_contact_information")[0].addEventListener(
        "click",
        function () {
         
          if ($(this).find("#expand_contact_information_icon")[0].getAttribute("href") === "#es-line-up") {
            $(this).find("#expand_contact_information_icon")[0].setAttribute("href", "#es-line-down");
            $(me.wrapper).find("#contact_info_section")[0].style.display = "none";
          } else {
            $(this).find("#expand_contact_information_icon")[0].setAttribute("href", "#es-line-up");
            $(me.wrapper).find("#contact_info_section")[0].style.display = "";
          }
         
        }
      );
      //-------------------------------------------<end of make expand action > ---------------------------

      // add Lead Link Field 
       me.lead_field = frappe.ui.form.make_control(
        { df:
            { fieldname: 'linked_customer',
              label:'Lead',
              fieldtype: 'Link', 
              options: 'Lead' ,
              change: frappe.utils.debounce(  function() {    // Event handler
                // code on change
                let current_value = this.get_value();
                 
                    if (me.is_cleared==true)
                    {
                        me.is_cleared=false;
                        me.lead_field.set_value(null);
                        me.last_lead_value=null;
                        return;
                    }
                // 2. THE FIX: Compare current value with the last processed value
                if (me.lead_field.$input.val() != "") {
               
                  
                    if (current_value.length > 1 ) {
                        me.last_lead_value=current_value;
                        // Case A: User selected a Lead
                      
                        me.page.set_indicator("", "");
                      
                          me.refresh_data(this.value,wrapper);
                          
                        me.has_unsaved_changes=false;
                        
                    } 
                 
                       
                }
                else {
                    
                
                        // Case B: User CLEARED the field (Clicked X)
                       
                         
                        me.empty_fields(wrapper);
                        me.page.set_indicator("", "");
                        // You must explicitly clear your data here
                        // For example:
                        
                        // OR call a clear function:
                        // me.clear_data(wrapper);
                    
                    return;
                }
               },100 )
            }, 
            parent: $(me.wrapper).find("#lead"), 
            
            render_input: true       
        });
        me.lead_field.$wrapper.on('click', '.btn-clear', function() {
            // 1. Optional: Ensure the value is actually cleared in the model
            
          //  me.empty_fields(wrapper);
           
            // 2. Run your clear function immediately
            console.log("X button pressed - Immediate Trigger");
          me.is_cleared=true;
            me.lead_field.set_value(null);
             me.empty_fields(wrapper); 
           
        });
        
      //-------------------------------------------<end of add Lead Link Field  > ---------------------------
      
      $(".custom-nav-item .custom-nav-link").on("click", function() {
        // Toggle active class
        $(".custom-nav-item .custom-nav-link").removeClass("active");
        $(this).addClass("active");
    
        // Update content
        let text = $(this).text().trim();
        if (text === "Lead" || text==='عميل محتمل') {
            $(me.wrapper).find("#main-lead")[0].style.display = "";
            $(me.wrapper).find("#main-opportunity")[0].style.display = "none";
            $(me.wrapper).find("#main-maintenance")[0].style.display = "none";
           
            
        } else if (text === "Opportunities" || text ==='الفرص') {
            $(me.wrapper).find("#main-lead")[0].style.display = "none";
            $(me.wrapper).find("#main-opportunity")[0].style.display = "";
            $(me.wrapper).find("#main-maintenance")[0].style.display = "none";
            
        } else if (text === "Maintenance" || text ==='الصيانة' ) {
            $(me.wrapper).find("#main-lead")[0].style.display = "none";
            $(me.wrapper).find("#main-opportunity")[0].style.display = "none";
            $(me.wrapper).find("#main-maintenance")[0].style.display = "";
        }
    });
    
    }
}