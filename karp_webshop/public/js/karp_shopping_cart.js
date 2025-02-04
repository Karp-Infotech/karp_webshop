// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// shopping cart
frappe.provide("webshop.webshop.shopping_cart");
var shopping_cart = webshop.webshop.shopping_cart;


$.extend(shopping_cart, {

	update_cart: function(opts) {

		if (frappe.session.user==="Guest") {
			if (localStorage) {
				localStorage.setItem("last_visited", window.location.pathname);
			}
			frappe.call('webshop.webshop.api.get_guest_redirect_on_action').then((res) => {
				window.location.href = res.message || "/login";
			});
		} else {
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
		}
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

	bind_add_to_cart_action() {
		$('.page_content').on('click', '.btn-add-to-cart-list', (e) => {

			const $btn = $(e.currentTarget);
			//$btn.prop('disabled', true);

			if (frappe.session.user==="Guest") {
				if (localStorage) {
					localStorage.setItem("last_visited", window.location.pathname);
				}
				frappe.call('webshop.webshop.api.get_guest_redirect_on_action').then((res) => {
					window.location.href = res.message || "/login";
				});
				return;
			}

			//$btn.addClass('hidden');
			//$btn.closest('.cart-action-container').addClass('d-flex');
			//$btn.parent().find('.go-to-cart').removeClass('hidden');
			//$btn.parent().find('.go-to-cart-grid').removeClass('hidden');
			$btn.parent().find('.cart-indicator').removeClass('hidden');

			const item_code = $btn.data('item-code');
			webshop.webshop.shopping_cart.add_item({
				item_code,
				qty: 1,
				with_items: 0
			});

		});
	}

});
