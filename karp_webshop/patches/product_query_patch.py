import frappe

# import the core module
from webshop.webshop.product_data_engine import query as _qmod

# create a subclass that only changes __init__ (or other methods you need)
class PatchedProductQuery(_qmod.ProductQuery):
    def __init__(self):
        print("Patching Init from Prouct Query")
        # call original init
        super().__init__()
        # ensure custom_mrp and formatted_mrp are present
        if "custom_single_discount" not in self.fields:
            self.fields.append("custom_single_discount")

        if "custom_vto_enabled" not in self.fields:
            self.fields.append("custom_vto_enabled")

        if "custom_vsp_eligible" not in self.fields:
            self.fields.append("custom_vsp_eligible")
			

# Replace the original class reference with our patched class
_qmod.ProductQuery = PatchedProductQuery