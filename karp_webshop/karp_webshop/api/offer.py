import frappe
from frappe.utils import nowdate
from frappe.utils import today, add_days

@frappe.whitelist(allow_guest=True)
def claim_welcome_offer(mobile, name=None, utm_source=None, utm_campaign=None):
    """
    Creates/updates customer and credits leaflet reward points once.
    """

    if not mobile or len(mobile) != 10:
        frappe.throw("Invalid mobile number")

    customer = None

    # 1️⃣ Check if customer exists by mobile
    existing_customer = frappe.db.get_value(
        "Customer",
        {"mobile_no": mobile},
        ["name", "custom_welcome_offer_availed"],
        as_dict=True
    )

    # 1️⃣ Fetch Loyalty Program from Karp Webshop Settings
    loyalty_program = frappe.db.get_single_value(
        "Karp Webshop Settings",
        "b2c_loyalty_program"
    )
    welcome_reward_points = frappe.db.get_single_value(
        "Karp Webshop Settings",
        "welcome_reward_points"
    )
    welcome_reward_validity = frappe.db.get_single_value(
        "Karp Webshop Settings",
        "welcome_reward_validity"
    )
    if existing_customer:
        customer = existing_customer.name
    else:
        # 2️⃣ Create new customer
        customer_doc = frappe.get_doc({
            "doctype": "Customer",
            "customer_name": name or mobile,
            "mobile_no": mobile,
            "customer_type": "Individual",
            "lead_source": utm_source or "Leaflet",
            "campaign_code": utm_campaign,
            "loyalty_program": loyalty_program
        })
        customer_doc.insert(ignore_permissions=True)
        customer = customer_doc.name

    # 3️⃣ Check if leaflet reward already given
    reward_given = frappe.db.get_value(
        "Customer",
        customer,
        "custom_welcome_offer_availed"
    )

    if reward_given:
        return {
            "status": "exists",
            "message": "Reward already credited",
            "customer": customer
        }

     

    if not loyalty_program:
        frappe.throw("B2C Loyalty Program not configured")

    # 4️⃣ Credit loyalty points
    loyalty_entry = frappe.get_doc({
        "doctype": "Loyalty Point Entry",
        "customer": customer,
        "loyalty_program": loyalty_program,
        "loyalty_points": welcome_reward_points,
        "posting_date": today(),
        "expiry_date": add_days(today(), welcome_reward_validity),
        "invoice_type": "Sales Invoice",
        "loyalty_program_tier": "Standard"
    })
    loyalty_entry.insert(ignore_permissions=True)

    # 5️⃣ Mark reward as given
    frappe.db.set_value(
        "Customer",
        customer,
        "custom_welcome_offer_availed",
        1
    )

    frappe.db.commit()

    return {
        "status": "success",
        "customer": customer,
        "points": welcome_reward_points
    }