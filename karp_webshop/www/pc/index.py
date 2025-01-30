import frappe
from frappe.utils import cint

from webshop.webshop.product_data_engine.filters import ProductFiltersBuilder

sitemap = 1


def get_context(context):

	pc_doc = frappe.get_doc('Product Collection', get_pc_name())
      
	context.title = pc_doc.title  
	context.field_filter = pc_doc.field_filters

	# Add homepage as parent
	context.body_class = "product-page"
	context.parents = [{"name": frappe._("Home"), "route": "/"}]

	filter_engine = ProductFiltersBuilder()
	context.field_filters = filter_engine.get_field_filters()
	context.attribute_filters = filter_engine.get_attribute_filters()

	context.page_length = (
		cint(frappe.db.get_single_value("Webshop Settings", "products_per_page")) or 20
	)
            
	context.no_cache = 1


def get_pc_name():
    path = frappe.request.path  # Example: "/col/women"
    collection_name = path.split("/")[-1]  # Extracts "women"

    print("Collection Name: " + collection_name) 

    return collection_name