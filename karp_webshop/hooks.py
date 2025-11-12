app_name = "karp_webshop"
app_title = "Karp Webshop"
app_publisher = "Karp Infotech"
app_description = "Karp Webshop"
app_email = "sushil.pal@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "karp_webshop",
# 		"logo": "/assets/karp_webshop/logo.png",
# 		"title": "Karp Webshop",
# 		"route": "/karp_webshop",
# 		"has_permission": "karp_webshop.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/karp_webshop/css/karp_webshop.css"
# app_include_js = "/assets/karp_webshop/js/karp_webshop.js"

# include js, css files in header of web template
# web_include_css = "/assets/karp_webshop/css/karp_webshop.css"
# web_include_js = "/assets/karp_webshop/js/karp_webshop.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "karp_webshop/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "karp_webshop/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "karp_webshop.utils.jinja_methods",
# 	"filters": "karp_webshop.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "karp_webshop.install.before_install"
# after_install = "karp_webshop.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "karp_webshop.uninstall.before_uninstall"
# after_uninstall = "karp_webshop.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "karp_webshop.utils.before_app_install"
# after_app_install = "karp_webshop.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "karp_webshop.utils.before_app_uninstall"
# after_app_uninstall = "karp_webshop.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "karp_webshop.notifications.get_notification_config"

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




# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"karp_webshop.tasks.all"
# 	],
# 	"daily": [
# 		"karp_webshop.tasks.daily"
# 	],
# 	"hourly": [
# 		"karp_webshop.tasks.hourly"
# 	],
# 	"weekly": [
# 		"karp_webshop.tasks.weekly"
# 	],
# 	"monthly": [
# 		"karp_webshop.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "karp_webshop.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "karp_webshop.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "karp_webshop.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["karp_webshop.utils.before_request"]
# after_request = ["karp_webshop.utils.after_request"]

# Job Events
# ----------
# before_job = ["karp_webshop.utils.before_job"]
# after_job = ["karp_webshop.utils.after_job"]

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
# 	"karp_webshop.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

website_route_rules = [
  {'from_route': '/pc/women-eg', 'to_route': 'pc'},
  {'from_route': '/pc/men-eg', 'to_route': 'pc'},
  {'from_route': '/pc/kids-eg', 'to_route': 'pc'},
  {'from_route': '/pc/women-sg', 'to_route': 'pc'},
  {'from_route': '/pc/sunglasses', 'to_route': 'pc'},
  {'from_route': '/pc/men-sg', 'to_route': 'pc'},
  {'from_route': '/pc/kids-sg', 'to_route': 'pc'},
  {'from_route': '/pc/kids', 'to_route': 'pc'},
  {'from_route': '/pc/sports', 'to_route': 'pc'},
  {'from_route': '/pc/professional', 'to_route': 'pc'},
  {'from_route': '/pc/trendy', 'to_route': 'pc'},
  {'from_route': '/pc/classic', 'to_route': 'pc'},
  {'from_route': '/pc/colorful', 'to_route': 'pc'},
  {'from_route': '/pc/bestsellers', 'to_route': 'pc'},
  {'from_route': '/brand/optivo', 'to_route': 'pc'},
  {'from_route': '/brand/regalis', 'to_route': 'pc'},
  {'from_route': '/pc/optivo', 'to_route': 'pc'},
  {'from_route': '/pc/regalis', 'to_route': 'pc'},
  {'from_route': '/pc/foldables', 'to_route': 'pc'},
  {'from_route': '/pc/clipons', 'to_route': 'pc'},
  {'from_route': '/pc/round', 'to_route': 'pc'},
  {'from_route': '/pc/rhombus', 'to_route': 'pc'},
  {'from_route': '/pc/square', 'to_route': 'pc'},
  {'from_route': '/pc/hexa', 'to_route': 'pc'},
  {'from_route': '/pc/penta', 'to_route': 'pc'},
  {'from_route': '/pc/cateye', 'to_route': 'pc'},
  {'from_route': '/pc/clubmaster', 'to_route': 'pc'},
  {'from_route': '/pc/oval', 'to_route': 'pc'},
  {'from_route': '/pc/aviator', 'to_route': 'pc'},
  {'from_route': '/pc/rectanngle', 'to_route': 'pc'},
  {'from_route': '/pc/screen', 'to_route': 'pc'},
  {'from_route': '/pc/screen-men', 'to_route': 'pc'},
  {'from_route': '/pc/screen-women', 'to_route': 'pc'}
]

app_include_js = [
    "/assets/karp_webshop/js/product_ui/karp_grid.js"
]

web_include_js = [
    "/assets/karp_webshop/js/guest_session.js"
]

web_include_css = [
                "/assets/karp_webshop/css/karp_webshop.css",
                "/assets/karp_webshop/css/mobile_filter.css"
]

web_template_overrides = {
    "Item Card Group": "karp_webshop/webshop/webshop/web_template/item_card_group/item_card_group.html"
}

web_include_js = [
    "https://cdnjs.cloudflare.com/ajax/libs/OwlCarousel2/2.3.4/owl.carousel.min.js",
    "/assets/karp_webshop/js/guest_session.js",
    "/assets/karp_webshop/js/home_service.js",
    "/assets/karp_webshop/js/karp_shopping_cart.js"
]

# Run patch after boot
app_include = "karp_webshop.karp_webshop.overrides.query"

# This ensures your patch runs before any request (web or desk)
before_app_request = [
    "karp_webshop.karp_webshop.overrides.boot_patch"
]

doc_events = {
    "Sales Order": {
        "on_update": "karp_webshop.karp_webshop.overrides.order_hooks.update_guest_customer_info",
        "before_save": [
            "karp_webshop.karp_webshop.overrides.promotions.apply_tiered_discount",
            "karp_webshop.karp_webshop.overrides.promotions.calculate_savings"
        ]          
    },
    "Quotation": {
        "before_save": [
            "karp_webshop.karp_webshop.overrides.promotions.apply_tiered_discount",
            "karp_webshop.karp_webshop.overrides.promotions.calculate_savings"
        ]       
    }
}


override_whitelisted_methods = {
    "frappe.frappe.core.doctype.user.user.sign_up": "karp_webshop.api.karp_user.karp_sign_up"
}

