import frappe

no_cache = 1


def get_context(context):
    context.page_title = "Videos - PS Church"
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
