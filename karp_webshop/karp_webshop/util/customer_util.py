
import frappe

def get_session_customer():

    	# Get the logged-in user
    email = frappe.session.user
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