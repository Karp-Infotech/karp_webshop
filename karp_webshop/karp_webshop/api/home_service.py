# karp_webshop/karp_webshop/www/api/customer_flags.py
import frappe
from urllib.parse import urlparse, parse_qs
import json
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

@frappe.whitelist(allow_guest=True)
def book_home_service(data):
    print("In book_home_service, raw data: ", data)
    if isinstance(data, str):
        data = json.loads(data)

    data = frappe._dict(data)

    doc = frappe.new_doc("Home Service Booking")
    doc.full_name = data.full_name
    doc.mobile_number = data.mobile_no
    doc.email = data.email
    doc.address = data.address
    doc.notes = data.notes
    doc.insert(ignore_permissions=True)

    frappe.db.commit()
    return {"status": "success"}


