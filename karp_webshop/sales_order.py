import frappe
from datetime import date

def calculate_sales_dist(doc, method):
    
    # Get the customer linked to the sales order
    customer = frappe.get_doc("Customer", doc.customer)
    kk_sales_portion = 0
    sales_dist_plan = get_sale_dist_plan()
    for item in doc.items:
        item_doc = frappe.get_doc("Item", item.item_code)
        for sd_item in sales_dist_plan.sales_distribution_items:
                if(sd_item.brand == item_doc.brand and sd_item.item_group == item_doc.item_group
                    and sd_item.sales_channel == doc.custom_sales_channel 
                    and sd_item.customer_relationship == customer.custom_customer_relationship) :
                    kk_sales_portion += item.net_amount * sd_item.kk_share_ / 100
                    break
        doc.custom_klear_kut_payment_amount = kk_sales_portion
        doc.save
        frappe.db.commit()
    
    




def get_sale_dist_plan():
	
    # Get the logged-in user
    user_email = frappe.session.user

    # Fetch the customer linked to this user
    customer = frappe.get_value("Customer", {"custom_linked_user": user_email}, ["name","custom_sales_distribution_plan"], as_dict=True)

    sales_dis_plan = frappe.get_doc("Sales Distribution Plan", customer.custom_sales_distribution_plan)

    return sales_dis_plan

   


