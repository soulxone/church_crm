import frappe

no_cache = 1


def get_context(context):
    context.page_title = "Upcoming Events | Pleasant Springs Church, Henderson TN"
    context.title = context.page_title
    context.metatags = {
        "title": context.page_title,
        "description": "Upcoming worship services, Bible studies, fellowship meals, and the annual Faith Walk pilgrimage at Pleasant Springs Church in Henderson, Tennessee.",
        "keywords": "pleasant springs church events, church calendar henderson tn, christian events west tennessee, faith walk event",
        "image": "https://ps-church.com/files/og-default.png",
        "og:type": "website",
        "og:title": "Upcoming Events — Pleasant Springs Church",
        "og:description": "Worship, study, and fellowship events in Henderson, Tennessee.",
        "og:image": "https://ps-church.com/files/og-default.png",
        "og:url": "https://ps-church.com/church-events",
        "twitter:card": "summary_large_image",
    }
    context.events = frappe.get_all(
        "Church Event",
        filters={"is_public": 1, "status": ["in", ["Planned", "Active"]]},
        fields=["event_name", "event_type", "start_date", "end_date", "venue", "summary", "image", "is_online", "online_meeting_url"],
        order_by="start_date asc",
    )
    return context
