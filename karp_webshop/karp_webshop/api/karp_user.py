# my_app/api/signup.py
import frappe
from frappe import _
# import core sign_up BEFORE we override it via hooks
try:
    from frappe.core.doctype.user.user import sign_up as core_sign_up
except Exception:
    core_sign_up = None

@frappe.whitelist(allow_guest=True)
def karp_sign_up(email, full_name, redirect_to=None, **kwargs):
    """
    Wrapper around frappe.core.doctype.user.user.sign_up
    - Calls the core sign_up to create the User (so existing behaviour + email flows remain)
    - If guest_session_id cookie exists, find Customer and Contact and link the new User
    """
    # 1) call core sign_up (if available) so default flow is preserved
    if core_sign_up:
        # core_sign_up returns a message string (e.g. "Registration Details Emailed.")
        core_result = core_sign_up(email=email, full_name=full_name, redirect_to=redirect_to)
    else:
        # fallback: create minimal User (be careful: this will not send welcome email etc)
        frappe.throw(_("Core sign_up not available"))

    # 2) find the just-created user
    user_name = frappe.db.get_value("User", {"email": email}, "name")
    if not user_name:
        return core_result  # nothing else we can do

    # 3) read guest_session_id cookie
    guest_session_id = None
    try:
        guest_session_id = frappe.request.cookies.get("guest_session_id")
    except Exception:
        # request may not be available in some contexts
        guest_session_id = None

    if not guest_session_id:
        return core_result

    # 4) find customer with this guest_session_id
    customer_name = frappe.db.get_value("Customer", {"custom_guest_session_id": guest_session_id}, "name")
    
    if not customer_name:
        return core_result

    # 5) find Contact linked to this customer (Dynamic Link table -> parent is Contact)
    contact_parent = frappe.db.get_value(
        "Dynamic Link",
        {"link_doctype": "Customer", "link_name": customer_name, "parenttype": "Contact"},
        "parent"
    )

    if contact_parent:
        contact = frappe.get_doc("Contact", contact_parent)
        contact.user = user_name
        contact.save(ignore_permissions=True)

    return core_result
