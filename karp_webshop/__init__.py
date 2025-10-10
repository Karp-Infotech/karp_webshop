__version__ = "0.0.1"
import frappe
import erpnext.controllers.website_list_for_contact as website_list_for_contact
from karp_webshop.overrides.website_list_for_contact import karp_get_transaction_list
from webshop.webshop.doctype.item_review.item_review import get_customer
from webshop.webshop.shopping_cart.product_info import get_product_info_for_website
from webshop.webshop.utils.product import get_non_stock_item_status

# apps/karp_webshop/karp_webshop/__init__.py
# ensure patch module is loaded at app import time
from .patches import product_query_patch  # noqa: F401

website_list_for_contact.get_transaction_list = karp_get_transaction_list



def _patch_webshop():
    try:
        from webshop.webshop.product_data_engine import query as original_query

        # Overriding get_stock_availability method in webshop/webshop/webshop/product_data_engine/query.py so that stock availiblity is checked for the warehouse assigned to the customer.
        def get_stock_availability(self, item):
		
            """Modify item object and add stock details."""
            from webshop.templates.pages.wishlist import (
                get_stock_availability as get_stock_availability_from_template,
            )
            
            item.in_stock = False

            customer_doc = get_customer_by_email(frappe.session.user)
            warehouse = customer_doc.get("custom_primary_warehouse")

            if(not warehouse) :
                    k_ws_settings = frappe.get_single("Karp Webshop Settings") 
                    warehouse = k_ws_settings.default_web_warehouse

            is_stock_item = frappe.get_cached_value("Item", item.item_code, "is_stock_item")

            if item.get("on_backorder"):
                return
            
            if not is_stock_item:
                if warehouse:
                    # product bundle case
                    item.in_stock = get_non_stock_item_status(item.item_code, "website_warehouse")
                else:
                    item.in_stock = True
            elif warehouse:
                # stock item and has warehouse
                item.in_stock = get_stock_availability_from_template(item.item_code, warehouse)


        # ✅ patch it
        original_query.ProductQuery.get_stock_availability = get_stock_availability
        frappe.logger().info("✅ Patched ProductQuery.get_stock_availability")

    except Exception as e:
        frappe.logger().error(f"❌ Failed to patch: {e}")


def get_customer_by_email(email):

    # first check per-request cache
    if hasattr(frappe.local, "customer_doc"):
        print("Found in Cache")
        return frappe.local.customer_doc
    else:
        print("NOT Found in Cache")

    customer_doc = _get_customer_from_db(email)
    if customer_doc:
        frappe.local.customer_doc = customer_doc
        return customer_doc

    return None
  

def _get_customer_from_db(email):
    print("Getting Customer from DB")
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

# Run patch at app load
_patch_webshop()