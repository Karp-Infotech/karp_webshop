// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt


// shopping cart
frappe.provide("webshop.webshop.shopping_cart");
var shopping_cart = webshop.webshop.shopping_cart;


$.extend(shopping_cart, {

	update_cart: function(opts) {

		
		shopping_cart.freeze();

		return frappe.call({
			type: "POST",
			method: "karp_webshop.karp_webshop.shopping_cart.karp_cart.update_cart",
			args: {
				item_code: opts.item_code,
				qty: opts.qty,
				additional_notes: opts.additional_notes !== undefined ? opts.additional_notes : undefined,
				with_items: opts.with_items || 0,
			},
			btn: opts.btn,
			callback: function(r) {
				shopping_cart.unfreeze();
				shopping_cart.set_cart_count(true);
				if(opts.callback)
					opts.callback(r);
			}
		});
		
	},

	remove_item: function({q_item_name}) {

		shopping_cart.freeze();
		return frappe.call({
			type: "POST",
			method: "karp_webshop.karp_webshop.shopping_cart.karp_cart.remove_item",
			args: {
				q_item_name: q_item_name,
				with_items: 1
			},
			callback: function(r) {
				shopping_cart.unfreeze();
				if(!r.exc) {
					$(".cart-items").html(r.message.items);
					$(".cart-tax-items").html(r.message.total);
					$(".payment-summary").html(r.message.taxes_and_totals);
					shopping_cart.set_cart_count();
				}
			},
		});
	},

	add_item: function({item_code, qty, with_items}) {

		shopping_cart.freeze();
		return frappe.call({
			type: "POST",
			method: "karp_webshop.karp_webshop.shopping_cart.karp_cart.add_item",
			args: {
				item_code: item_code,
				qty: qty,
				with_items: with_items
			},
			callback: function(r) {
				shopping_cart.unfreeze();
				shopping_cart.set_cart_count(true);
				if(!r.exc) {
					$(".cart-items").html(r.message.items);
					$(".cart-tax-items").html(r.message.total);
					$(".payment-summary").html(r.message.taxes_and_totals);
					shopping_cart.set_cart_count();
				}
			},
		});
	},

	shopping_cart_update: function({item_code, qty, cart_dropdown, additional_notes}) {
		shopping_cart.update_cart({
			item_code,
			qty,
			additional_notes,
			with_items: 1,
			btn: this,
			callback: function(r) {
				if(!r.exc) {
					$(".cart-items").html(r.message.items);
					$(".cart-tax-items").html(r.message.total);
					$(".payment-summary").html(r.message.taxes_and_totals);
					shopping_cart.set_cart_count();

					if (cart_dropdown != true) {
						$(".cart-icon").hide();
					}
				}
			},
		});
	},
	
	set_cart_count: function(animate=false) {
		$(".intermediate-empty-cart").remove();

		var cart_count = frappe.get_cookie("cart_count");


		if(cart_count) {
			$(".shopping-cart").toggleClass('hidden', false);
		}

		var $cart = $('.cart-icon');
		var $badge = $cart.find("#cart-count");

		if(parseInt(cart_count) === 0 || cart_count === undefined) {

			$(".cart-tax-items").hide();
			$(".btn-place-order").hide();
			$(".cart-payment-addresses").hide();

			let intermediate_empty_cart_msg = `
				<div class="text-center w-100 intermediate-empty-cart mt-4 mb-4 text-muted">
					${ __("Cart is Empty") }
				</div>
			`;
			$(".cart-table").after(intermediate_empty_cart_msg);
		}
		else {
			$cart.css("display", "inline");
			$("#cart-count").text(cart_count);
		}

		if(cart_count) {
			$badge.html(cart_count);

			if (animate) {
				$cart.addClass("cart-animate");
				setTimeout(() => {
					$cart.removeClass("cart-animate");
				}, 500);
			}
		} else {
			$badge.remove();
		}
	},

	bind_add_to_cart_action() {
		$('.page_content').on('click', '.btn-add-to-cart-list', (e) => {

			const $btn = $(e.currentTarget);

			$btn.parent().find('.cart-indicator').removeClass('hidden');

			const item_code = $btn.data('item-code');
			const item_name = $btn.data('item-name') || '';
			const item_price = Number($btn.data('price')) || 0;
			const item_brand = $btn.data('brand') || '';
			const item_category = $btn.data('category') || '';

			// GA4 Add-to-cart (PLP)
			window.dataLayer = window.dataLayer || [];
			window.dataLayer.push({
				event: "add_to_cart",
				ecommerce: {
					currency: "INR",
					value: item_price,
					items: [
						{
							item_id: item_code,
							item_name: item_name,
							price: item_price,
							quantity: 1,
							item_brand: item_brand,
							item_category: item_category
						}
					]
				}
			});

			console.log("GA4 add_to_cart PLP fired:", item_code);

			// Add to ERPNext cart
			webshop.webshop.shopping_cart.add_item({
				item_code,
				qty: 1,
				with_items: 0
			});
		});
	}

});
