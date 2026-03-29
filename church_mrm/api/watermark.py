import frappe
import os
import time
from PIL import Image


LOGO_SIZE = (100, 100)
PADDING = 10  # pixels from edge


def apply_watermark(file_url, doctype=None, docname=None):
    """Apply PS-Church logo watermark to the lower-right corner of an image.

    Returns the new file_url with watermark applied, or None on failure.
    """
    if not file_url:
        return None

    # Resolve image path
    file_path = _resolve_path(file_url)
    if not file_path or not os.path.exists(file_path):
        return None

    # Find logo file
    logo_path = _find_logo()
    if not logo_path:
        frappe.log_error("Watermark logo not found: PSC-logo-hires.png")
        return None

    try:
        img = Image.open(file_path)
        if img.mode == "P":
            img = img.convert("RGBA")

        logo = Image.open(logo_path)
        logo = logo.convert("RGBA")
        logo = logo.resize(LOGO_SIZE, Image.LANCZOS)

        # Calculate position (lower-right with padding)
        img_w, img_h = img.size
        logo_w, logo_h = logo.size
        x = img_w - logo_w - PADDING
        y = img_h - logo_h - PADDING

        # Don't watermark if image is too small
        if x < 0 or y < 0:
            return None

        # Composite with transparency
        if img.mode == "RGBA":
            img.paste(logo, (x, y), logo)
        else:
            # Convert to RGBA for paste, then back
            img = img.convert("RGBA")
            img.paste(logo, (x, y), logo)

        # Save as new file
        ext = os.path.splitext(file_path)[1].lower()
        if ext in (".heic", ".heif"):
            ext = ".jpg"

        original_stem = os.path.splitext(os.path.basename(file_path))[0]
        timestamp = int(time.time())
        new_filename = "{}_wm_{}{}".format(original_stem, timestamp, ext)

        site_path = frappe.get_site_path("public", "files")
        new_file_path = os.path.join(site_path, new_filename)

        # Convert RGBA to RGB for JPEG
        if ext in (".jpg", ".jpeg") and img.mode == "RGBA":
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            img = bg

        save_kwargs = {}
        if ext in (".jpg", ".jpeg"):
            save_kwargs = {"quality": 90, "optimize": True}
        elif ext == ".png":
            save_kwargs = {"optimize": True}

        img.save(new_file_path, **save_kwargs)

        new_file_url = "/files/{}".format(new_filename)

        # Create Frappe File doc
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_url": new_file_url,
            "file_name": new_filename,
            "is_private": 0,
            "attached_to_doctype": doctype,
            "attached_to_name": docname,
        })
        file_doc.insert(ignore_permissions=True)

        return new_file_url

    except Exception as e:
        frappe.log_error("Watermark error: {}".format(str(e)))
        return None


def _resolve_path(file_url):
    """Resolve a Frappe file URL to absolute disk path."""
    if file_url.startswith("/private/files/"):
        return frappe.get_site_path("private", "files",
                                     file_url.replace("/private/files/", ""))
    elif file_url.startswith("/files/"):
        return frappe.get_site_path("public", "files",
                                     file_url.replace("/files/", ""))
    return None


def _find_logo():
    """Find the PSC-logo-hires.png file on disk."""
    # Check public files first
    public_path = frappe.get_site_path("public", "files", "PSC-logo-hires.png")
    if os.path.exists(public_path):
        return public_path

    # Check private files
    private_path = frappe.get_site_path("private", "files", "PSC-logo-hires.png")
    if os.path.exists(private_path):
        return private_path

    # Check app assets
    import church_mrm
    app_path = os.path.join(os.path.dirname(church_mrm.__file__),
                            "public", "images", "PSC-logo-hires.png")
    if os.path.exists(app_path):
        return app_path

    return None
