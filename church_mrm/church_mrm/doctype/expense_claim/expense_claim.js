// Copyright (c) 2026, PS Church and contributors
// For license information, please see license.txt

frappe.ui.form.on('Expense Claim', {
	setup(frm) {
		// Set company from Expense Settings if not set
		if (!frm.doc.company) {
			frappe.db.get_single_value('Expense Settings', 'default_company').then(company => {
				if (company) {
					frm.set_value('company', company);
				}
			});
		}
	},

	refresh(frm) {
		// Add Scan Receipt button for draft claims
		if (frm.doc.docstatus === 0) {
			frm.add_custom_button(__('Scan Receipt'), function() {
				let url = '/expense-scanner';
				if (frm.doc.name && !frm.doc.__islocal) {
					url += '?claim=' + frm.doc.name;
				}
				window.open(url, '_blank');
			}, __('Tools'));
		}

		// Add Approve/Reject buttons for Expense Manager when pending
		if (frm.doc.docstatus === 0 && frm.doc.approval_status === 'Pending'
			&& frappe.user_roles.includes('Expense Manager')) {
			frm.add_custom_button(__('Approve'), function() {
				frm.set_value('approval_status', 'Approved');
				frm.set_value('approved_by', frappe.session.user);
				frm.set_value('approval_date', frappe.datetime.nowdate());
				frm.save();
			}, __('Actions'));

			frm.add_custom_button(__('Reject'), function() {
				frappe.prompt({
					fieldname: 'reason',
					fieldtype: 'Small Text',
					label: 'Reason for Rejection',
					reqd: 1
				}, function(values) {
					frm.set_value('approval_status', 'Rejected');
					frm.set_value('approved_by', frappe.session.user);
					frm.set_value('approval_date', frappe.datetime.nowdate());
					frm.set_value('approver_remarks', values.reason);
					frm.save();
				}, __('Reject Expense Claim'));
			}, __('Actions'));
		}
	},

	church_member(frm) {
		// Auto-fill claimant name from Church Member
		if (frm.doc.church_member) {
			frappe.db.get_value('Church Member', frm.doc.church_member, 'full_name', (r) => {
				if (r && r.full_name) {
					frm.set_value('claimant_name', r.full_name);
				}
			});
		}
	}
});

frappe.ui.form.on('Expense Claim Item', {
	amount(frm) {
		calculate_total(frm);
	},

	items_remove(frm) {
		calculate_total(frm);
	}
});

function calculate_total(frm) {
	let total = 0;
	(frm.doc.items || []).forEach(item => {
		total += flt(item.amount);
	});
	frm.set_value('total_amount', total);
}
