frappe.ui.form.on("Church Gallery Photo", {
    refresh(frm) {
        if (frm.doc.image && !frm.is_new()) {
            frm.add_custom_button(__("Edit Photo"), function() {
                church_mrm.photo_editor.open(frm);
            });
        }
    }
});
