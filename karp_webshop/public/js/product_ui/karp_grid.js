class KarpProductGrid extends webshop.ProductGrid {

	get_primary_button(item, settings) {
		if (item.has_variants) {
			return `
				<a href="/${ item.route || '#' }">
					<div class="btn btn-sm btn-explore-variants w-100 mt-4">
						${ __('Explore') }
					</div>
				</a>
			`;
		} else if (settings.enabled && (settings.allow_items_not_in_stock || item.in_stock)) {
			return `
				<div id="${ item.name }" class="btn
					btn-sm btn-primary btn-add-to-cart-list
					w-100 mt-2 "
					data-item-code="${ item.item_code }" style="visibility: visible;">
					<span class="mr-2">
						<svg class="icon icon-md">
							<use href="#icon-assets"></use>
						</svg>
					</span>
					${ settings.enable_checkout ? __('Add to Cart') :  __('Add to Quote') }
				</div>

				
			`;
		} else {
			return ``;
		}
	}

	get_price_html(item) {

		let price_html = `
			<div class="product-price" itemprop="offers" itemscope itemtype="https://schema.org/AggregateOffer">
				${ item.formatted_price || '' }
		`;

		if (item.custom_mrp) {
			price_html += `
				<small class="striked-price">
					<s>${ item.custom_mrp ? "₹" + item.custom_mrp : "" }</s>
				</small>
				<!-- <small class="ml-1 product-info-green">
					${ item.discount } OFF
				</small>-->
			`;
		}
		price_html += `</div>`;
		return price_html;
	}
};

// Assign the new class to webshop
webshop.ProductGrid = KarpProductGrid;