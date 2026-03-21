# Copyright (c) 2026, PS Church and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class ExpenseClaim(Document):
	def validate(self):
		self.calculate_totals()

	def calculate_totals(self):
		total = 0
		for item in self.items:
			total += flt(item.amount)
		self.total_amount = total

	def on_submit(self):
		self.create_journal_entry()

	def on_cancel(self):
		if self.journal_entry:
			je = frappe.get_doc("Journal Entry", self.journal_entry)
			if je.docstatus == 1:
				je.cancel()
			self.db_set("journal_entry", "")

	def create_journal_entry(self):
		if self.journal_entry:
			return

		je = frappe.new_doc("Journal Entry")
		je.posting_date = self.claim_date
		je.company = self.company
		je.voucher_type = "Journal Entry"

		# Group items by category to minimize JE rows
		category_totals = {}
		for item in self.items:
			if not item.amount:
				continue
			category_totals.setdefault(item.expense_category, 0)
			category_totals[item.expense_category] += flt(item.amount)

		for cat_name, amount in category_totals.items():
			category = frappe.get_doc("Expense Category", cat_name)

			# Debit the expense account
			je.append("accounts", {
				"account": category.expense_account,
				"debit_in_account_currency": flt(amount),
			})

			# Credit the payable account
			je.append("accounts", {
				"account": category.payable_account,
				"credit_in_account_currency": flt(amount),
			})

		je.user_remark = f"Expense Claim {self.name} - {self.claimant_name}"
		je.insert(ignore_permissions=True)
		je.submit()

		self.db_set("journal_entry", je.name)
