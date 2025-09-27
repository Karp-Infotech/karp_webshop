# Copyright (c) 2021, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

import frappe

no_cache = 1

from karp_webshop.karp_webshop.shopping_cart.karp_cart import get_cart_quotation


def get_context(context):

	# Get the logged-in user
    user_email = frappe.session.user

    customer = get_customer_by_email(user_email)


    # Pass customer data to context
    context.customer_type = customer.customer_type if customer.customer_type else ""

    context.body_class = "product-page"
    context.update(get_cart_quotation(None))
    
	
def get_customer_by_email(email):
    # Find Contact with given email
    contact = frappe.db.get_value(
        "Contact Email",
        {"email_id": email},
        "parent"
    )
    if not contact:
        return None

    # Find linked Customer from Contact
    customer = frappe.db.get_value(
        "Dynamic Link",
        {
            "parent": contact,
            "parenttype": "Contact",
            "link_doctype": "Customer"
        },
        "link_name"
    )
    # Load full Customer document
    customer_doc = frappe.get_doc("Customer", customer)
    return customer_doc