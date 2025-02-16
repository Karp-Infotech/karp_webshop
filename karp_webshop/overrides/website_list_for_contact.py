# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import json

import frappe
from frappe import _
from frappe.modules.utils import get_module_app
from frappe.utils import flt, has_common
from frappe.utils.user import is_website_user
import erpnext.controllers.website_list_for_contact as website_list_for_contact


def karp_get_transaction_list(
	doctype,
	txt=None,
	filters=None,
	limit_start=0,
	limit_page_length=20,
	order_by="creation",
	custom=False,
):
	user = frappe.session.user
	ignore_permissions = False

	if not filters:
		filters = {}

	filters["docstatus"] = ["<", "2"] if doctype in ["Supplier Quotation", "Purchase Invoice"] else ["<=", "1"]
	print("This is from Karp")

	if (user != "Guest" and is_website_user()) or doctype == "Request for Quotation":
		parties_doctype = "Request for Quotation Supplier" if doctype == "Request for Quotation" else doctype
		# find party for this contact
		customers, suppliers = get_customers_suppliers(parties_doctype, user)

		if customers:
			if doctype == "Quotation":
				filters["quotation_to"] = "Customer"
				filters["party_name"] = ["in", customers]
			else:
				filters["customer"] = ["in", customers]
		elif suppliers:
			filters["supplier"] = ["in", suppliers]
		elif not custom:
			return []

		if doctype == "Request for Quotation":
			parties = customers or suppliers
			return rfq_transaction_list(parties_doctype, doctype, parties, limit_start, limit_page_length)

		# Since customers and supplier do not have direct access to internal doctypes
		ignore_permissions = True

		if not customers and not suppliers and custom:
			ignore_permissions = False
			filters = {}

	transactions = website_list_for_contact.get_list_for_transactions(
		doctype,
		txt,
		filters,
		limit_start,
		limit_page_length,
		fields="name",
		ignore_permissions=ignore_permissions,
		order_by="creation desc",
	)

	if custom:
		return transactions

	return website_list_for_contact.post_process(doctype, transactions)