import frappe

def apply_reward_points_multipler(doc, method):

    if not doc:
        return 0.0
    
    tp_settings = frappe.get_single("Tiered Promotion Settings")
    if not tp_settings.enabled:
        return

    reward_point_multiplier = 1
    if tp_settings.promo_tiers:
        for tier in sorted(tp_settings.promo_tiers, key=lambda x: x.min_total, reverse=True):
            if doc.grand_total >= tier.min_total and doc.grand_total <=tier.max_total:
                reward_point_multiplier = tier.reward_points_multiplier
                break

    # 1. Retrieve the loyalty point entry created by ERPNext
    lpe = frappe.get_all(
        "Loyalty Point Entry",
        filters={"invoice": doc.name, "invoice_type": "Sales Invoice"},
        fields=["name", "loyalty_points"]
    )

    if not lpe:
        # No entry created (maybe program not applied)
        frappe.logger().info(f"No LPE found for invoice {doc.name}")
        return

    lpe_name = lpe[0].name
    current_points = lpe[0].loyalty_points

    # 3. Apply multiplier
    updated_points = int(current_points * reward_point_multiplier)

    # 4. Update the Loyalty Point Entry
    lpe_doc = frappe.get_doc("Loyalty Point Entry", lpe_name)
    lpe_doc.loyalty_points = updated_points
    lpe_doc.save()
    frappe.db.commit()