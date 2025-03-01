import frappe
from frappe.utils import cint
import json
import pprint

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
	all_field_filters = filter_engine.get_field_filters()
	context.field_filters = remove_pc_filters(all_field_filters,pc_doc.field_filters)
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

def remove_pc_filters(all_field_filters, pc_field_filters):

	#pc_field_names = pc_field_filters.keys()
	pc_field_filters_dict = json.loads(pc_field_filters)
	cleaned_field_filters = all_field_filters
	for field_filter in all_field_filters:
		#pprint.pprint(vars(field_filter[0]))
		for pc_field_name in pc_field_filters_dict.keys():
			position = field_filter[0].fieldname.find(pc_field_name)
			if (position > -1):
				cleaned_field_filters.remove(field_filter)
				break
	return cleaned_field_filters