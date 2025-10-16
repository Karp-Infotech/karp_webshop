# karp_webshop/karp_webshop/www/api/customer_flags.py
import frappe
from urllib.parse import urlparse, parse_qs
from karp_webshop.karp_webshop.util.customer_util import get_session_customer

@frappe.whitelist(allow_guest=True)
def is_home_service_eligible():

    hse = frappe.request.cookies.get("hse")
    if(hse):
        return {"show": True}
    

    customer = get_session_customer()

    if(customer) :
        if(customer.custom_home_service_eligible):
            return {"show": True}
        else:
            return {"show": False}
        
    # default
    return {"show": False}


@frappe.whitelist(allow_guest=True)
def is_home_service_not_eligible():
    print("In is_home_service_not_eligible")

    hse = frappe.request.cookies.get("hse")
    if(hse):
        return {"show": False}
    
    customer = get_session_customer()

    print(customer)

    if(customer) :
        if(customer.custom_home_service_eligible):
            return {"show": False}
        else:
            return {"show": True}
        
    # default
    return {"show": True}

