import frappe

no_cache = 1


def get_context(context):
    context.page_title = "Photo Gallery | Pleasant Springs Church, Pinson TN"
    context.title = context.page_title
    context.metatags = {
        "title": context.page_title,
        "description": "Pictures from worship, fellowship, and life together at Pleasant Springs Church in Pinson, Tennessee.",
        "keywords": "pleasant springs church photos, church gallery pinson tn, church life pictures, pinson tn church",
        "image": "https://ps-church.com/files/og-default.png",
        "og:type": "website",
        "og:title": "Photo Gallery — Pleasant Springs Church",
        "og:description": "Worship, fellowship, and life together in Pinson, Tennessee.",
        "og:image": "https://ps-church.com/files/og-default.png",
        "og:url": "https://ps-church.com/gallery",
        "twitter:card": "summary_large_image",
    }
    context.photos = frappe.get_all(
        "Church Gallery Photo",
        filters={"is_published": 1},
        fields=["name", "image", "caption", "category"],
        order_by="display_order asc, creation desc",
    )
    context.categories = frappe.get_all(
        "Gallery Category",
        fields=["category_name"],
        order_by="display_order asc",
    )
    return context
