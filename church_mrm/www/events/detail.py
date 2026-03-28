import frappe
from frappe.utils import get_url

no_cache = 1


def get_context(context):
    name = frappe.form_dict.get("name")

    if not name:
        frappe.throw("Event not found", frappe.DoesNotExistError)

    event = frappe.get_all(
        "Church Event",
        filters={"event_name": name, "is_public": 1},
        fields=[
            "event_name", "event_type", "start_date", "end_date",
            "venue", "summary", "description", "image",
            "is_online", "online_meeting_url", "status"
        ],
        limit=1,
    )

    if not event:
        frappe.throw("Event not found", frappe.DoesNotExistError)

    ev = event[0]

    context.event = ev
    context.page_title = ev.event_name + " — Pleasant Springs Church"

    # OG / social meta
    site_url = get_url()
    context.og_title = ev.event_name
    context.og_description = ev.summary or "Join us at Pleasant Springs Church for " + ev.event_name
    context.og_image = (
        site_url + ev.image
        if ev.image and ev.image.startswith("/")
        else site_url + "/assets/church_mrm/images/og-banner.png"
    )
    context.og_url = site_url + "/events/detail?name=" + frappe.utils.quote(name)

    return context
