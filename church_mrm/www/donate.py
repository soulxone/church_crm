import frappe

no_cache = 1


def get_context(context):
    context.page_title = "Donate to Pleasant Springs Church | Pinson, TN"
    context.title = context.page_title
    context.metatags = {
        "title": context.page_title,
        "description": "Support the ministry of Pleasant Springs Church — Bible study, discipleship, the AHAVAH app, and the cemetery. Online giving with a tax-deductible receipt.",
        "keywords": "donate pleasant springs church, christian giving tennessee, church donation pinson tn, tithe online",
        "image": "https://ps-church.com/files/og-default.png",
        "og:type": "website",
        "og:title": "Donate to Pleasant Springs Church",
        "og:description": "Support free Bible teaching, the AHAVAH app, and cemetery care in Pinson, Tennessee.",
        "og:image": "https://ps-church.com/files/og-default.png",
        "og:url": "https://ps-church.com/donate",
        "twitter:card": "summary_large_image",
    }
    context.donation_types = frappe.get_all(
        "Donation Type",
        filters={"is_active": 1},
        fields=["name", "label"],
        order_by="sort_order asc",
    )
    return context


@frappe.whitelist(allow_guest=True)
def submit_donation(donor_name, email, donation_type, amount):
    company = frappe.db.get_single_value("Global Defaults", "default_company")
    donation = frappe.new_doc("Donation")
    donation.donor_name = donor_name
    donation.donation_type = donation_type
    donation.amount = float(amount)
    donation.donation_date = frappe.utils.today()
    donation.payment_method = "Online"
    donation.company = company
    donation.source = "Website"
    donation.insert(ignore_permissions=True)
    return {"status": "success", "donation": donation.name}
