# karp_webshop/karp_webshop/www/api/customer_flags.py
import frappe
from urllib.parse import urlparse, parse_qs
from karp_webshop.karp_webshop.util.customer_util import get_session_customer

@frappe.whitelist(allow_guest=True)
def is_home_service_eligible():

    customer = get_session_customer()

    if(customer) :
        if(customer.custom_home_service_eligible):
            return {"show": True}
        else:
            return {"show": False}
        
    # default
    return {"show": False}

