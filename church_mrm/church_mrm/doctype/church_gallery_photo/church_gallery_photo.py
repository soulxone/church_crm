import frappe
from frappe.model.document import Document


class ChurchGalleryPhoto(Document):
    def before_insert(self):
        if not self.uploaded_by:
            self.uploaded_by = frappe.session.user

    def on_update(self):
        # Apply watermark when image is set or changed
        if self.image and self.has_value_changed("image"):
            try:
                from church_mrm.api.watermark import apply_watermark
                new_url = apply_watermark(self.image, self.doctype, self.name)
                if new_url and new_url != self.image:
                    frappe.db.set_value(self.doctype, self.name, "image", new_url,
                                        update_modified=False)
                    self.image = new_url
            except Exception:
                frappe.log_error("Watermark failed for {}".format(self.name))
