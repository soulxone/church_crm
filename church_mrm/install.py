import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    create_contact_custom_fields()
    create_default_donation_types()
    create_default_membership_types()
    create_default_relationship_types()
    create_default_expense_categories()
    create_expense_manager_role()
    create_workspace_sidebar()
    create_desktop_icon()


def create_contact_custom_fields():
    custom_fields = {
        "Contact": [
            dict(
                fieldname="church_member",
                fieldtype="Link",
                label="Church Member",
                options="Church Member",
                insert_after="user",
                module="Church MRM",
            ),
            dict(
                fieldname="is_church_member",
                fieldtype="Check",
                label="Is Church Member",
                insert_after="church_member",
                module="Church MRM",
            ),
        ]
    }
    create_custom_fields(custom_fields, update=True)


def create_default_donation_types():
    types = [
        {"donation_type_name": "Tithe", "label": "Tithe", "is_tax_deductible": 1},
        {"donation_type_name": "General Offering", "label": "General Offering", "is_tax_deductible": 1},
        {"donation_type_name": "Building Fund", "label": "Building Fund", "is_tax_deductible": 1},
        {"donation_type_name": "Missions", "label": "Missions", "is_tax_deductible": 1},
        {"donation_type_name": "Benevolence Fund", "label": "Benevolence Fund", "is_tax_deductible": 1},
        {"donation_type_name": "Special Offering", "label": "Special Offering", "is_tax_deductible": 1},
        {"donation_type_name": "Youth Ministry", "label": "Youth Ministry", "is_tax_deductible": 1},
        {"donation_type_name": "Music Ministry", "label": "Music Ministry", "is_tax_deductible": 1},
    ]
    for t in types:
        if not frappe.db.exists("Donation Type", t["donation_type_name"]):
            doc = frappe.new_doc("Donation Type")
            doc.update(t)
            doc.is_active = 1
            doc.flags.ignore_mandatory = True
            doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_default_membership_types():
    types = [
        {"type_name": "Regular Member", "title": "Regular Member", "duration_interval": 1, "duration_unit": "Year", "period_type": "Rolling"},
        {"type_name": "Youth Member", "title": "Youth Member", "duration_interval": 1, "duration_unit": "Year", "period_type": "Rolling"},
        {"type_name": "Senior Member", "title": "Senior Member", "duration_interval": 1, "duration_unit": "Year", "period_type": "Rolling"},
        {"type_name": "Associate Member", "title": "Associate Member", "duration_interval": 1, "duration_unit": "Year", "period_type": "Rolling"},
    ]
    for t in types:
        if not frappe.db.exists("Membership Type", t["type_name"]):
            doc = frappe.new_doc("Membership Type")
            doc.update(t)
            doc.is_active = 1
            doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_default_relationship_types():
    types = [
        {"relationship_type": "Spouse", "label_a_to_b": "is spouse of", "label_b_to_a": "is spouse of"},
        {"relationship_type": "Parent-Child", "label_a_to_b": "is parent of", "label_b_to_a": "is child of"},
        {"relationship_type": "Sibling", "label_a_to_b": "is sibling of", "label_b_to_a": "is sibling of"},
        {"relationship_type": "Head of Household", "label_a_to_b": "is head of household for", "label_b_to_a": "is member of household of"},
    ]
    for t in types:
        if not frappe.db.exists("Church Relationship Type", t["relationship_type"]):
            doc = frappe.new_doc("Church Relationship Type")
            doc.update(t)
            doc.is_active = 1
            doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_default_expense_categories():
    categories = [
        {"category_name": "Travel", "description": "Mileage, fuel, lodging, airfare"},
        {"category_name": "Supplies", "description": "Office and ministry supplies"},
        {"category_name": "Food/Meals", "description": "Meals and refreshments for events"},
        {"category_name": "Ministry Materials", "description": "Bibles, curriculum, study materials"},
        {"category_name": "Utilities", "description": "Electric, water, internet, phone"},
        {"category_name": "Office", "description": "Printing, postage, office equipment"},
        {"category_name": "Maintenance", "description": "Building and grounds maintenance"},
        {"category_name": "Other", "description": "Miscellaneous expenses"},
    ]
    for c in categories:
        if not frappe.db.exists("Expense Category", c["category_name"]):
            doc = frappe.new_doc("Expense Category")
            doc.update(c)
            doc.is_active = 1
            doc.flags.ignore_mandatory = True
            doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_expense_manager_role():
    if not frappe.db.exists("Role", "Expense Manager"):
        doc = frappe.new_doc("Role")
        doc.role_name = "Expense Manager"
        doc.desk_access = 1
        doc.insert(ignore_permissions=True)
        frappe.db.commit()


def create_workspace_sidebar():
    """Create the Workspace Sidebar record so Church MRM appears in the desk sidebar with full rail nav."""
    # Delete and recreate to ensure latest items
    if frappe.db.exists("Workspace Sidebar", "Church MRM"):
        frappe.delete_doc("Workspace Sidebar", "Church MRM", ignore_permissions=True, force=True)

    doc = frappe.new_doc("Workspace Sidebar")
    doc.name = "Church MRM"
    doc.title = "Church MRM"
    doc.header_icon = "heart"
    doc.module = "Church MRM"
    doc.standard = 0

    sidebar_items = [
        # Home link
        {"label": "Home", "link_type": "Workspace", "type": "Link", "link_to": "Church MRM",
         "child": 0, "collapsible": 1, "indent": 0, "icon": "home"},

        # --- Contacts & Members ---
        {"label": "Contacts & Members", "link_type": "DocType", "type": "Section Break", "link_to": None,
         "child": 0, "collapsible": 1, "indent": 1, "icon": "users"},
        {"label": "Church Member", "link_type": "DocType", "type": "Link", "link_to": "Church Member",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Church Group", "link_type": "DocType", "type": "Link", "link_to": "Church Group",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Church Relationship", "link_type": "DocType", "type": "Link", "link_to": "Church Relationship",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Contact", "link_type": "DocType", "type": "Link", "link_to": "Contact",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},

        # --- Contributions & Accounting ---
        {"label": "Contributions", "link_type": "DocType", "type": "Section Break", "link_to": None,
         "child": 0, "collapsible": 1, "indent": 1, "icon": "income"},
        {"label": "Donation", "link_type": "DocType", "type": "Link", "link_to": "Donation",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Donation Type", "link_type": "DocType", "type": "Link", "link_to": "Donation Type",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Pledge", "link_type": "DocType", "type": "Link", "link_to": "Pledge",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Journal Entry", "link_type": "DocType", "type": "Link", "link_to": "Journal Entry",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Payment Entry", "link_type": "DocType", "type": "Link", "link_to": "Payment Entry",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Chart of Accounts", "link_type": "DocType", "type": "Link", "link_to": "Account",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},

        # --- Memberships ---
        {"label": "Memberships", "link_type": "DocType", "type": "Section Break", "link_to": None,
         "child": 0, "collapsible": 1, "indent": 1, "icon": "membership"},
        {"label": "Membership", "link_type": "DocType", "type": "Link", "link_to": "Membership",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Membership Type", "link_type": "DocType", "type": "Link", "link_to": "Membership Type",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},

        # --- Expenses ---
        {"label": "Expenses", "link_type": "DocType", "type": "Section Break", "link_to": None,
         "child": 0, "collapsible": 1, "indent": 1, "icon": "expense"},
        {"label": "Expense Claim", "link_type": "DocType", "type": "Link", "link_to": "Expense Claim",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Expense Category", "link_type": "DocType", "type": "Link", "link_to": "Expense Category",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Receipt Scanner", "link_type": "URL", "type": "Link", "link_to": "/expense-scanner",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},

        # --- Events ---
        {"label": "Events", "link_type": "DocType", "type": "Section Break", "link_to": None,
         "child": 0, "collapsible": 1, "indent": 1, "icon": "calendar"},
        {"label": "Church Event", "link_type": "DocType", "type": "Link", "link_to": "Church Event",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},

        # --- Reports ---
        {"label": "Reports", "link_type": "DocType", "type": "Section Break", "link_to": None,
         "child": 0, "collapsible": 1, "indent": 1, "icon": "chart"},
        {"label": "Giving Statement", "link_type": "Report", "type": "Link", "link_to": "Giving Statement",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Donation Summary", "link_type": "Report", "type": "Link", "link_to": "Donation Summary",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Membership Report", "link_type": "Report", "type": "Link", "link_to": "Membership Report",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Pledge Fulfillment", "link_type": "Report", "type": "Link", "link_to": "Pledge Fulfillment",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Event Attendance", "link_type": "Report", "type": "Link", "link_to": "Event Attendance",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},

        # --- Settings ---
        {"label": "Settings", "link_type": "DocType", "type": "Section Break", "link_to": None,
         "child": 0, "collapsible": 1, "indent": 1, "icon": "setting-gear"},
        {"label": "Church Relationship Type", "link_type": "DocType", "type": "Link", "link_to": "Church Relationship Type",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
        {"label": "Expense Settings", "link_type": "DocType", "type": "Link", "link_to": "Expense Settings",
         "child": 1, "collapsible": 1, "indent": 0, "icon": ""},
    ]

    for idx, item in enumerate(sidebar_items, 1):
        item["idx"] = idx
        doc.append("items", item)

    doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_desktop_icon():
    """Create the Desktop Icon so Church MRM appears on the desk home page."""
    if not frappe.db.exists("Desktop Icon", "Church MRM"):
        doc = frappe.new_doc("Desktop Icon")
        doc.label = "Church MRM"
        doc.icon_type = "Link"
        doc.link_type = "Workspace Sidebar"
        doc.link_to = "Church MRM"
        doc.icon = "heart"
        doc.app = "church_mrm"
        doc.bg_color = "blue"
        doc.hidden = 0
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
