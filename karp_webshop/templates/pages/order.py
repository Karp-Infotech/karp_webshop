# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe import _

from webshop.webshop.doctype.webshop_settings.webshop_settings import show_attachments


def get_context(context):
	
	context.no_cache = 1
	context.show_sidebar = True
	context.doc = frappe.get_doc(frappe.form_dict.doctype, frappe.form_dict.name)
	
	context.user_msg = create_user_msg(context.doc)

	context.enable_payment = context.doc.custom_payment_ready or is_direct_purchase(context.doc)

	if hasattr(context.doc, "set_indicator"):
		context.doc.set_indicator()

	if show_attachments():
		context.attachments = get_attachments(frappe.form_dict.doctype, frappe.form_dict.name)

	context.parents = frappe.form_dict.parents
	context.title = frappe.form_dict.name
	context.payment_ref = frappe.db.get_value(
		"Payment Request", {"reference_name": frappe.form_dict.name}, "name"
	)

	context.enabled_checkout = frappe.get_doc("Webshop Settings").enable_checkout

	default_print_format = frappe.db.get_value(
		"Property Setter",
		dict(property="default_print_format", doc_type=frappe.form_dict.doctype),
		"value",
	)
	if default_print_format:
		context.print_format = default_print_format
	else:
		context.print_format = "Standard"

	# check for the loyalty program of the customer
	customer_loyalty_program = frappe.db.get_value(
		"Customer", context.doc.customer_name, "loyalty_program"
	)
	if customer_loyalty_program:
		from erpnext.accounts.doctype.loyalty_program.loyalty_program import (
			get_loyalty_program_details_with_points,
		)

		loyalty_program_details = get_loyalty_program_details_with_points(
			context.doc.customer_name, customer_loyalty_program
		)
		context.available_loyalty_points = int(loyalty_program_details.get("loyalty_points"))

	# show Make Purchase Invoice button based on permission
	context.show_make_pi_button = frappe.has_permission("Purchase Invoice", "create")


def get_attachments(dt, dn):
	return frappe.get_all(
		"File",
		fields=["name", "file_name", "file_url", "is_private"],
		filters={"attached_to_name": dn, "attached_to_doctype": dt, "is_private": 0},
	)

def create_user_msg(sales_order):
	if is_direct_purchase(sales_order) or sales_order.custom_payment_ready:
		return "Your order is successfully placed. Please pay balance amount."
	else:
		return "Your order is successfully placed. Our expert will reach out for further procesing."
	
def is_direct_purchase(sales_order):
	is_direct_purchase = True
	for item in sales_order.items:
		if "Eyeglasses" in item.item_group:
			is_direct_purchase = False
			break
	return is_direct_purchase