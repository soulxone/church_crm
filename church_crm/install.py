import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    create_contact_custom_fields()
    create_default_donation_types()
    create_default_membership_types()
    create_default_relationship_types()


def create_contact_custom_fields():
    custom_fields = {
        "Contact": [
            dict(
                fieldname="church_member",
                fieldtype="Link",
                label="Church Member",
                options="Church Member",
                insert_after="user",
                module="Church CRM",
            ),
            dict(
                fieldname="is_church_member",
                fieldtype="Check",
                label="Is Church Member",
                insert_after="church_member",
                module="Church CRM",
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
