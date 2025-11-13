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
		`;

		// If Single Discount is defined (e.g. 30)
		if (item.custom_single_discount && parseFloat(item.custom_single_discount) > 0) {
			const discount_percent = parseFloat(item.custom_single_discount);
			const base_price = parseFloat(item.price_list_rate || 0);
			const discounted_price = base_price * (1 - discount_percent / 100);

			price_html += `
				<span class="discounted-price text-red-600 font-semibold ml-2">
					₹${ discounted_price  }
				</span>
				<small class="striked-price">
					<s>${ item.price_list_rate || '' }</s>
				</small>
				
				<small class="ml-1 product-info-green">
					(${ discount_percent }% OFF)
				</small>
			`;
		} else {
			price_html += `${ item.formatted_price || '' }`;
		}
		
		price_html += `</div>`;
		price_html += `
			<div class="vsp-badge mt-1">
				<span class="vsp-text">VSP Eligible</span>
			</div>
		`;

		return price_html;
	}

	get_image_html(item, title) {
		let image = item.website_image;

		const productUrl = this.get_product_url(item);

		if (image) {
			return `
				<div class="card-img-container">
					<a href="/${ productUrl }" style="text-decoration: none;">
						<img itemprop="image" class="card-img" src="${ image }" alt="${ title }">
					</a>
				</div>
			`;
		} else {
			return `
				<div class="card-img-container">
					<a href="/${ productUrl}" style="text-decoration: none;">
						<div class="card-img-top no-image">
							${ frappe.get_abbr(title) }
						</div>
					</a>
				</div>
			`;
		}
	}

	get_title(item, title) {
		const productUrl = this.get_product_url(item);
		let title_html = `
			<a href="/${ productUrl }">
				<div class="product-title" itemprop="name">
					${ title || '' }
				</div>
			</a>
		`;
		return title_html;
	}

	get_product_url(item) {
		let base = item.route || '#';
		let ref = window.location.pathname; // e.g. /pc/men-eg

		// Remove the '/pc/' prefix if it exists
		if (ref.startsWith('/pc/')) {
			ref = ref.replace('/pc/', '');
		} else {
			// Remove leading slash if any
			ref = ref.replace(/^\//, '');
		}

		let query = `?ref=${encodeURIComponent(ref)}`;
		return `${base}${query}`;
	}

};

// Assign the new class to webshop
webshop.ProductGrid = KarpProductGrid;