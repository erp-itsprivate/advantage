app_name = "advantage"
app_title = "Advantage"
app_publisher = "ItsPrivate"
app_description = "CRM enhancement "
app_email = "developer@itsprivate.net"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "advantage",
# 		"logo": "/assets/advantage/logo.png",
# 		"title": "Advantage",
# 		"route": "/advantage",
# 		"has_permission": "advantage.api.permission.has_app_permission"
# 	}
# ]

fixtures = [  {"dt": "Custom Field", "filters": [["Module", "in", ["Advantage"]]]}, {"dt": "Property Setter"} ]
# Includes in <head>
# ------------------
doc_events = {
    "Email Queue": {
        "before_insert": "advantage.utils.email_queue"
    },
    
}
# include js, css files in header of desk.html
# app_include_css = "/assets/advantage/css/advantage.css"
# app_include_js = "/assets/advantage/js/advantage.js"

# include js, css files in header of web template
# web_include_css = "/assets/advantage/css/advantage.css"
# web_include_js = "/assets/advantage/js/advantage.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "advantage/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
app_include_js = [
	"/assets/advantage/js/utils.bundle.js",
	"/assets/advantage/js/lib/datepicker.ar.js",
    "/assets/advantage/js/filter_users_events.js"
]
# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "advantage/public/icons.svg"

# Home Pages
# ----------
doctype_js ={"Lead": "public/js/lead.js" ,"Opportunity":"public/js/opportunity.js"}
# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }
permission_query_conditions = {
	"Task": "advantage.utils.get_permission_query_conditions",	
    "ToDo": "advantage.override.todo.get_permission_query_conditions"
}

has_permission = {
 	"Task": "advantage.utils.has_permission",
    "ToDo": "advantage.override.todo.has_permission"
	
 }
override_doctype_class = {
	#"Contact": "advantage.override.contact.AdvantageContact",
    	"Lead": "advantage.override.lead.AdvantageLead",
    "Customer":"advantage.override.customer.AdvantageCustomer"   ,
    "ToDo":"advantage.override.todo.AdvantageToDo"  ,  
    "Event":"advantage.override.event.AdvantageEvent"     
}
# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "advantage.utils.jinja_methods",
# 	"filters": "advantage.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "advantage.install.before_install"
# after_install = "advantage.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "advantage.uninstall.before_uninstall"
# after_uninstall = "advantage.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "advantage.utils.before_app_install"
# after_app_install = "advantage.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "advantage.utils.before_app_uninstall"
# after_app_uninstall = "advantage.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "advantage.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }
jinja = {
	"methods": [
        "advantage.utils.format_datetime",      "advantage.utils.show_how_old"
        ] 
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"advantage.tasks.all"
# 	],
# 	"daily": [
# 		"advantage.tasks.daily"
# 	],
# 	"hourly": [
# 		"advantage.tasks.hourly"
# 	],
# 	"weekly": [
# 		"advantage.tasks.weekly"
# 	],
# 	"monthly": [
# 		"advantage.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "advantage.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "advantage.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "advantage.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["advantage.utils.before_request"]
# after_request = ["advantage.utils.after_request"]

# Job Events
# ----------
# before_job = ["advantage.utils.before_job"]
# after_job = ["advantage.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"advantage.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

