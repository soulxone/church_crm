import frappe

no_cache = 1


def get_context(context):
    context.page_title = "Sermons & Teaching Videos | Pleasant Springs Church"
    context.title = context.page_title
    context.metatags = {
        "title": context.page_title,
        "description": "Watch free sermons, Bible studies, and teaching videos from Pleasant Springs Church. Septuagint study, doctrine, and discipleship from Henderson, Tennessee.",
        "keywords": "church sermons online, free christian video, septuagint sermon, bible teaching video, pleasant springs videos",
        "image": "https://ps-church.com/files/og-default.png",
        "og:type": "website",
        "og:title": "Sermons & Teaching Videos — Pleasant Springs Church",
        "og:description": "Free sermons and Bible teaching videos from a small church in West Tennessee.",
        "og:image": "https://ps-church.com/files/og-default.png",
        "og:url": "https://ps-church.com/videos",
        "twitter:card": "summary_large_image",
    }
    context.videos = frappe.get_all(
        "Church Video",
        filters={"is_published": 1},
        fields=["name", "title", "description", "video_id", "thumbnail_url",
                "category", "published_date"],
        order_by="published_date desc",
    )
    # Extract distinct categories for filter tabs
    context.categories = sorted(list(set(
        v.category for v in context.videos if v.category
    )))
    return context
