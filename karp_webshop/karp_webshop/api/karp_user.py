# my_app/api/signup.py
import frappe 
from frappe import _

from frappe.website.utils import is_signup_disabled
from frappe.utils import (
	escape_html,
)

@frappe.whitelist(allow_guest=True)
def karp_sign_up(email, full_name, password, redirect_to=None, **kwargs):

  
    core_result = sign_up(email=email, full_name=full_name, redirect_to=redirect_to, password=password)


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


def sign_up(email: str, full_name: str, redirect_to: str, password: str) -> tuple[int, str]:
	if is_signup_disabled():
		frappe.throw(_("Sign Up is disabled"), title=_("Not Allowed"))
	print("Password :")
	print(password)	

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, _("Already Registered")
		else:
			return 0, _("Registered but disabled")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_(
					"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
				),
				http_status_code=429,
			)

		from frappe.utils import random_string

		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": escape_html(full_name),
				"enabled": 1,
				"new_password": password,
				"user_type": "Website User",
			}
		)
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert()

		# set default signup role as per Portal Settings
		default_role = frappe.db.get_single_value("Portal Settings", "default_role")
		if default_role:
			user.add_roles(default_role)

		if redirect_to:
			frappe.cache.hset("redirect_after_login", user.name, redirect_to)
		return 1, _("Registration successful. You can now log in.")
