import frappe
from frappe.utils import flt

def apply_tiered_discount(doc, method=None):
    """Apply tiered discount based on Promotion Settings"""

    tp_settings = frappe.get_single("Tiered Promotion Settings")
    if not tp_settings.enabled:
        return

    # Determine if rule applies on this doctype
   # if settings.apply_on_doctype == "Quotation" and doc.doctype != "Quotation":
    #    return
    #if settings.apply_on_doctype == "Sales Order" and doc.doctype != "Sales Order":
    #    return

    included_brands = [d.brand for d in tp_settings.included_brands]

    # Calculate eligible total
    eligible_total = 0.0
    for item in doc.items:
        brand = frappe.db.get_value("Item", item.item_code, "brand")
        if brand in included_brands:
            eligible_total += flt(item.amount or 0.0)    

    # Find applicable tier
    applicable_discount = 0.0
    if tp_settings.promo_tiers:
        for tier in sorted(tp_settings.promo_tiers, key=lambda x: x.min_total, reverse=True):
            if eligible_total >= tier.min_total and eligible_total <=tier.max_total:
                applicable_discount = flt(tier.discount_percent)
                break

    # Apply discount
    if applicable_discount > 0:
        #doc.discount_type = "Percent"
        doc.apply_discount_on = "Net Total"
        #doc.additional_discount_percentage = applicable_discount
         # Compute the actual discount amount for clarity
        discount_amount = flt(eligible_total * applicable_discount / 100.0)
        doc.discount_amount = discount_amount
    else:
       # Reset if not applicable
        doc.discount_type = "Percent"
        doc.additional_discount_percentage = 0
        doc.discount_amount = 0
        frappe.logger().info("ℹ️ No tier met. Discount cleared.")
    
    # 5️⃣ Trigger recalculation of totals
    doc.calculate_taxes_and_totals()


def calculate_savings(doc, method=None):
    """Compute total savings for the given Quotation/Sales Order."""
    if not doc:
        return 0.0
    
    calculate_total_base_item_price(doc)
    calculate_total_item_discount(doc)
    calculate_total_savings(doc)

    

def calculate_total_savings(doc,method=None):
    # Step 1: Item-level savings
    total_item_savings = sum(flt(item.discount_amount or 0.0) for item in (doc.items or []))

    # Step 2: Order-level discount
    # ERPNext automatically sets `doc.discount_amount` for order-level discounts
    order_discount = flt(getattr(doc, "discount_amount", 0.0))

    # Step 3: Any other promotions (future extension)
    # e.g., coupon-based discount, free item equivalent value, etc.

    total_savings = total_item_savings + order_discount

    # Optional: assign to doc for display or export
    doc.custom_total_savings = total_savings

    frappe.logger().info(f"💰 Calculated total savings for {doc.name}: ₹{total_savings}")

def calculate_total_item_discount(doc):
    # Step 1: Item-level savings
    total_item_savings = sum(flt(item.discount_amount or 0.0) for item in (doc.items or []))
    doc.custom_total_item_discount = total_item_savings


def calculate_total_base_item_price(doc):

    base_total = 0.0
    for item in doc.items:
        base_rate = get_item_base_price(item.item_code, doc.selling_price_list)
        base_total += base_rate * item.qty
    doc.custom_total_item_price = base_total
    


def get_item_base_price(item_code, price_list, customer=None):
    """Fetch base rate (without any discounts) for a given item and price list."""

    rate = frappe.db.get_value(
        "Item Price",
        {"item_code": item_code, "price_list": price_list},
        "price_list_rate"
    )
    return rate or 0.0