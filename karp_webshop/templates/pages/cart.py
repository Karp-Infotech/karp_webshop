# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

no_cache = 1

from webshop.webshop.shopping_cart.cart import get_cart_quotation


def get_context(context):

	# Get the logged-in user
    user_email = frappe.session.user
    customer = frappe.get_value("Customer", {"custom_linked_user": user_email}, ["name", "customer_type"], as_dict=True)

    print(customer)

    # Pass customer data to context
    context.customer_type = customer.customer_type if customer.customer_type else ""

    context.body_class = "product-page"
    context.update(get_cart_quotation())
    
	