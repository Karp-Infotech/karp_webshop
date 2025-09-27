import frappe

def update_guest_customer_info(doc, method):
    """
    Update guest customer info (Contact) from shipping address
    when the Sales Order is saved (on_update hook).
    Only runs for guest customers (Contact with empty user_id and email_id="Guest").
    """

    if not doc.customer:
        return

    customer = frappe.get_doc("Customer", doc.customer)

    # Step 1: Find contacts linked to this customer via Dynamic Link
    linked_contacts = frappe.get_all(
        "Dynamic Link",
        filters={
            "link_doctype": "Customer",
            "link_name": customer.name,
            "parenttype": "Contact"
        },
        fields=["parent as contact_name"]
    )

    if not linked_contacts:
        print("Not Contact Found")
        return  # no contacts linked, skip

    # Step 2: Find guest contact (user_id empty and email_id="Guest")
    guest_contact = None
    for lc in linked_contacts:
        contact = frappe.get_doc("Contact", lc.contact_name)
        if not contact.user:
            print ("Found Guest Contact")
            guest_contact = contact
            break

    if not guest_contact:
        print("No Guest Contact")
  
        return  # no guest contact found

    # Step 3: Update guest contact info from shipping address
    if doc.shipping_address_name:
        address = frappe.get_doc("Address", doc.shipping_address_name)

        # Update name
        if getattr(address, "address_title", None):
            guest_contact.first_name = address.address_title
            customer.customer_name = address.address_title

        guest_contact.phone_nos = []   # Clear Contact Phone table
        guest_contact.email_ids = []    
        # Update phone
        if getattr(address, "phone", None):
            guest_contact.append("phone_nos", {
                "phone": address.phone,
                "is_primary_phone": 1
            })

        # Update email
        if getattr(address, "email_id", None):
            guest_contact.append("email_ids", {
                "email_id": address.email_id,
                "is_primary_email": 1
            })

    assign_loyalty_program(customer)
    # Save contact
    guest_contact.save(ignore_permissions=True)
    customer.save(ignore_permissions=True)




def assign_loyalty_program(customer): 
    if(not customer.loyalty_program) : 
        k_ws_settings = frappe.get_single("Karp Webshop Settings") 
        customer.loyalty_program = k_ws_settings.b2c_loyalty_program