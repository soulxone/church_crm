import frappe

no_cache = 1


def get_context(context):
    context.page_title = "Become a Member | Pleasant Springs Church, Henderson TN"
    context.title = context.page_title
    context.metatags = {
        "title": context.page_title,
        "description": "Join Pleasant Springs Church in Henderson, Tennessee. Sign up to become a member of our community of faith — visitors and seekers always welcome too.",
        "keywords": "join pleasant springs church, church membership henderson tn, christian community tennessee",
        "image": "https://ps-church.com/files/og-default.png",
        "og:type": "website",
        "og:title": "Become a Member — Pleasant Springs Church",
        "og:description": "Join our community of faith in Henderson, Tennessee.",
        "og:image": "https://ps-church.com/files/og-default.png",
        "og:url": "https://ps-church.com/membership-signup",
        "twitter:card": "summary_large_image",
    }
    return context


@frappe.whitelist(allow_guest=True)
def submit_signup(first_name, last_name, email, phone=None):
    member = frappe.new_doc("Church Member")
    member.first_name = first_name
    member.last_name = last_name
    member.email_address = email
    member.phone = phone
    member.membership_status = "New"
    member.member_since = frappe.utils.today()
    member.insert(ignore_permissions=True)
    return {"status": "success", "member": member.name}
