import frappe
import json
from frappe.utils import flt, today

no_cache = 1


def get_context(context):
    # Require login — redirect guests to login page
    if frappe.session.user == "Guest":
        frappe.local.flags.redirect_location = "/login?redirect-to=/expense-scanner"
        raise frappe.Redirect

    context.page_title = "Expense Scanner - PS Church"
    context.no_breadcrumbs = True
    context.categories = frappe.get_all(
        "Expense Category",
        filters={"is_active": 1},
        fields=["name", "category_name"],
        order_by="category_name asc"
    )
    # Pass logged-in user info for auto-fill
    context.user_fullname = frappe.utils.get_fullname(frappe.session.user)
    context.user_email = frappe.session.user
    return context


@frappe.whitelist()
def create_expense_claim(claimant_name, items_json, notes="", receipt_urls_json="[]"):
    items = json.loads(items_json)
    receipt_urls = json.loads(receipt_urls_json)

    settings = frappe.get_single("Expense Settings")
    company = settings.default_company or frappe.db.get_single_value(
        "Global Defaults", "default_company"
    )

    doc = frappe.new_doc("Expense Claim")
    doc.claimant_name = claimant_name
    doc.claimant_email = frappe.session.user
    doc.claim_date = today()
    doc.company = company
    doc.notes = notes

    for idx, item in enumerate(items):
        row = doc.append("items", {})
        row.description = item.get("description", "")
        row.vendor = item.get("vendor", "")
        row.expense_category = item.get("category", "")
        row.expense_date = item.get("date") or today()
        row.amount = flt(item.get("amount", 0))
        row.ocr_raw_text = item.get("ocr_raw_text", "")
        # Attach receipt image if uploaded
        if idx < len(receipt_urls) and receipt_urls[idx]:
            row.receipt_image = receipt_urls[idx]

    doc.insert()
    frappe.db.commit()
    return {"name": doc.name, "route": f"/app/expense-claim/{doc.name}"}
