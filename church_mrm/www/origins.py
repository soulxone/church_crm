import frappe

no_cache = 1


def get_context(context):
    context.page_title = "Origins of Ideas | Pleasant Springs Church"
    context.title = context.page_title
    context.metatags = {
        "title": context.page_title,
        "description": "Tracing the roots of doctrines, traditions, and ideas across Church history — from the Apostolic Fathers to the present. A teaching project of Pleasant Springs Church.",
        "keywords": "origins of christian ideas, history of doctrine, church history project, theological origins",
        "image": "https://ps-church.com/files/og-default.png",
        "og:type": "website",
        "og:title": "Origins of Ideas — Pleasant Springs",
        "og:description": "Tracing the roots of Christian doctrines and traditions across history.",
        "og:image": "https://ps-church.com/files/og-default.png",
        "og:url": "https://ps-church.com/origins",
        "twitter:card": "summary_large_image",
    }
    context.no_breadcrumbs = True
    context.is_logged_in = frappe.session.user != "Guest"
    context.user_fullname = (
        frappe.utils.get_fullname(frappe.session.user)
        if context.is_logged_in
        else ""
    )
