$(() => {
	class ProductListing {
		constructor() {
			let me = this;
			let is_item_group_page = $(".item-group-content").data("item-group");
			this.item_group = is_item_group_page || null;

			//let view_type = localStorage.getItem("product_view") || "Grid View";

			// Render Product Views, Filters & Search
			new webshop.ProductView({
				view_type: "Grid View",
				products_section: $('#product-listing'),
				item_group: me.item_group
			});

			this.bind_card_actions();
		}

		bind_card_actions() {
			webshop.webshop.shopping_cart.bind_add_to_cart_action();
			webshop.webshop.wishlist.bind_wishlist_action();
		}
	}

	new ProductListing();
});


class KarpProductView extends webshop.ProductView {
    
    get_item_filter_data(from_filters = false) {

		let me = this;
		this.from_filters = from_filters;
		let args = this.get_query_filters();

		let fieldFilters = args?.field_filters || {};

		args.field_filters = Object.assign({}, fieldFilters, this.get_pc_field_filters());

		this.disable_view_toggler(true);

		frappe.call({
			method: "webshop.webshop.api.get_product_filter_data",
			args: {
				query_args: args
			},
			callback: function(result) {
				if (!result || result.exc || !result.message || result.message.exc) {
					me.render_no_products_section(true);
				} else {
					// Sub Category results are independent of Items
					if (me.item_group && result.message["sub_categories"].length) {
						me.render_item_sub_categories(result.message["sub_categories"]);
					}

					if (!result.message["items"].length) {
						// if result has no items or result is empty
						me.render_no_products_section();
					} else {
						// Add discount filters
						me.re_render_discount_filters(result.message["filters"].discount_filters);

						// Render views
						me.render_list_view(result.message["items"], result.message["settings"]);
						me.render_grid_view(result.message["items"], result.message["settings"]);

						me.products = result.message["items"];
						me.product_count = result.message["items_count"];
					}

					// Bind filter actions
					if (!from_filters) {
						// If `get_product_filter_data` was triggered after checking a filter,
						// don't touch filters unnecessarily, only data must change
						// filter persistence is handle on filter change event
						me.bind_filters();
						me.restore_filters_state();
					}

					// Bottom paging
					me.add_paging_section(result.message["settings"]);
				}

				me.disable_view_toggler(false);
			}
		});
    }

	get_pc_field_filters() {

		let pc_field_filters = new String(document.getElementById("pc_field_filters").value.toString().slice(1, -1)); //Remove leading and traling " char

		pc_field_filters = pc_field_filters.replace(/(\r\n|\n|\r|\\n|\\)/g, '').trim(); //Remove unwanted chars	

		return JSON.parse(pc_field_filters)
	}
}

// Override the default ProductView with CustomProductView
webshop.ProductView = KarpProductView;
