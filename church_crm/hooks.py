app_name = "church_crm"
app_title = "Church CRM"
app_publisher = "PS Church"
app_description = "Church CRM - Nonprofit CRM for Frappe/ERPNext inspired by CiviCRM"
app_email = "soulxone@gmail.com"
app_license = "AGPLv3"
required_apps = ["frappe", "erpnext"]

# App Icon (shown in Desk sidebar and module page)
app_icon = "/assets/church_crm/images/church_crm.svg"
app_color = "#6C5CE7"
app_icon_color = "#FFFFFF"

after_install = "church_crm.install.after_install"

# Include CSS and JS in all pages
app_include_css = "/assets/church_crm/css/church_crm.css"
app_include_js = "/assets/church_crm/js/church_crm.js"

# Extend existing ERPNext DocTypes
doctype_js = {
    "Contact": "public/js/contact.js"
}

doc_events = {
    "Contact": {
        "validate": "church_crm.overrides.contact.validate_contact",
    }
}

# Fixtures - Custom Fields added to existing DocTypes
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Church CRM"]]
    },
    {
        "dt": "Property Setter",
        "filters": [["module", "=", "Church CRM"]]
    },
    {
        "dt": "Number Card",
        "filters": [["module", "=", "Church CRM"]]
    },
    {
        "dt": "Dashboard Chart",
        "filters": [["module", "=", "Church CRM"]]
    },
    {
        "dt": "Onboarding Step",
        "filters": [["module", "=", "Church CRM"]]
    },
    {
        "dt": "Module Onboarding",
        "filters": [["module", "=", "Church CRM"]]
    }
]

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "church_crm.tasks.update_membership_statuses",
        "church_crm.tasks.send_pledge_reminders"
    ],
}

# Website routes
website_route_rules = [
    {"from_route": "/donate", "to_route": "donate"},
    {"from_route": "/church-events", "to_route": "church_events"},
    {"from_route": "/membership-signup", "to_route": "membership_signup"},
]

# Website context for portal
website_context = {
    "favicon": "/assets/church_crm/images/church_crm.svg",
    "splash_image": "/assets/church_crm/images/church_crm.svg",
}
