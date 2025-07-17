import frappe

def create_customer_for_user(doc, method):
    """Create a Customer when a new user signs up on the webshop."""
    if frappe.db.exists("Customer", {"custom_linked_user": doc.name}):
        return  # Customer already exists

    k_ws_settings = frappe.get_single("Karp Webshop Settings") 

    customer_name = doc.full_name or doc.email  # Use full name or fallback to email
    customer_doc = frappe.get_doc({
        "doctype": "Customer",
        "customer_name": customer_name,
        "customer_type": "Individual",
        "customer_group": "Individual",
        "territory": "All Territories",
        "custom_customer_segment": "Regular",
        "email_id": doc.email,
        "custom_linked_user": doc.name,
        "loyalty_program": k_ws_settings.b2c_loyalty_program,
        "gender": doc.gender
    })
    customer_doc.insert(ignore_permissions=True)

    frappe.db.commit()  # Ensure changes are saved
    