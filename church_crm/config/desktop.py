from frappe import _


def get_data():
    return [
        {
            "module_name": "Church CRM",
            "color": "#6C5CE7",
            "icon": "/assets/church_crm/images/church_crm.svg",
            "type": "module",
            "label": _("Church CRM"),
            "description": _("Church membership, donations, events, and ministry management."),
            "onboard_present": 1,
        }
    ]
