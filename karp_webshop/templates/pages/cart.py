# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

no_cache = 1

from webshop.webshop.shopping_cart.cart import get_cart_quotation


def get_context(context):
	# Get the logged-in user
    user = frappe.session.user

    # Fetch the customer linked to this user
    customer = frappe.db.get_value("Customer", {"customer_name": user}, ["customer_type"], as_dict=True)

    # Pass customer data to context
    context.customer_type = customer.customer_type if customer.customer_type else ""

    context.body_class = "product-page"
    context.update(get_cart_quotation())
    
	