$(() => {
	class ProductListing {
		constructor() {
			let me = this;
			let is_item_group_page = $(".item-group-content").data("item-group");
			this.item_group = is_item_group_page || null;

			//let view_type = localStorage.getItem("product_view") || "Grid View";

			// Render Product Views, Filters & Search
			window.karp_product_view = new webshop.ProductView({
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

	/**
     * Accepts an object { field_filters: {...}, attribute_filters: {...}, start: 0 }
     * and applies them (updates internal state and refreshes)
     */
    applyFiltersFromObject(filterObject = {}) {
      // normalize
      this.field_filters = filterObject.field_filters || {};
      this.attribute_filters = filterObject.attribute_filters || {};
      // reset start so results show from first page
      const start = (typeof filterObject.start !== 'undefined') ? filterObject.start : 0;

      // mark that filters came from user action
      this.from_filters = true;

      // call existing workflow to update route, push history and fetch
      this.change_route_with_filters(); // this uses this.field_filters and this.attribute_filters internally
      // note: change_route_with_filters() will call make(true) to fetch new items
    }

    /**
     *This method makes one server request for all the filters selected. It is used in mobile filters.
     */
    getResultFromFilters() {
      	// Reset previous filter state
		this.field_filters = {};
		this.attribute_filters = {};
		this.from_filters = true; // so pagination resets to first page

		// Prefer selecting filters from the desktop filters container to avoid clones
		// Ensure desktopFiltersSelector is available in your scope. If not, fallback to document.
		const desktopFiltersContainer = (typeof desktopFiltersSelector !== 'undefined')
			? document.querySelector("##product-filters") 
			: document;

		if (!desktopFiltersContainer) {
			console.warn('Desktop filters container not found; falling back to document.');
		}

		// Helper to push values into map (array) safely
		const pushTo = (obj, key, val) => {
			obj[key] = obj[key] || [];
			if (!obj[key].includes(val)) obj[key].push(val);
		};

		// 1) Process checkbox / radio / inputs with data-filter-name / data-filter-value
		const inputs = (desktopFiltersContainer || document).querySelectorAll('.product-filter');

		inputs.forEach(inp => {
			// ensure we are reading actual desktop controls (not inside mobile drawer)
			// if your drawer has class '.mobile-filter-panel', exclude elements inside it
			if (inp.closest && inp.closest('.mobile-filter-panel')) return;

			const $inp = $(inp); // using jQuery since ProductView uses it
			const isChecked = $inp.is(':checked');

			// Attribute filters (class .attribute-filter)
			if ($inp.is('.attribute-filter')) {
			const { attributeName, attributeValue } = $inp.data() || {};
			if (!attributeName) return;

			if (isChecked) {
				pushTo(this.attribute_filters, attributeName, attributeValue);
			} else {
				// nothing to do — we only push checked values; we'll clean up below
			}
			}
			// Field filters (class .field-filter) and discount filter
			else if ($inp.is('.field-filter') || $inp.is('.discount-filter')) {
			const { filterName, filterValue } = $inp.data() || {};
			if (!filterName) return;

			// If this is a discount filter, ensure we clear previous discount key so only one discount is applied
			if ($inp.is('.discount-filter')) {
				// ensure we clear previous discount value so only selected discount is present
				delete this.field_filters["discount"];
				if (isChecked) pushTo(this.field_filters, filterName, filterValue);
			} else {
				if (isChecked) {
				pushTo(this.field_filters, filterName, filterValue);
				}
			}
			}
		});

		// 2) Process select boxes inside filters (support multi & single-selects)
		// selects may not have .product-filter class; they usually have data-filter-name attribute
		const selects = (desktopFiltersContainer || document).querySelectorAll('select[data-filter-name]');
		selects.forEach(sel => {
			if (sel.closest && sel.closest('.mobile-filter-panel')) return;
			const name = sel.getAttribute('data-filter-name');
			if (!name) return;

			if (sel.multiple) {
			Array.from(sel.selectedOptions).forEach(opt => {
				const val = opt.value || opt.text;
				if (val) pushTo(this.field_filters, name, val);
			});
			} else {
			const v = sel.value;
			if (v) pushTo(this.field_filters, name, v);
			}
		});

		// 3) Clean up empty arrays (remove keys whose arrays ended up empty)
		Object.keys(this.field_filters).forEach(k => {
			if (!this.field_filters[k] || this.field_filters[k].length === 0) {
			delete this.field_filters[k];
			}
		});
		Object.keys(this.attribute_filters).forEach(k => {
			if (!this.attribute_filters[k] || this.attribute_filters[k].length === 0) {
			delete this.attribute_filters[k];
			}
		});

		// 4) Finally, call the existing method that builds the query string & triggers the ajax fetch.
		// change_route_with_filters() will set the history, set start to 0 (because from_filters=true) and call make(true)
		this.change_route_with_filters();
    }

	add_paging_section(settings) {
		$(".product-paging-area").remove();

		if (this.products) {
			let paging_html = `
				<div class="row product-paging-area mt-5">
					<div class="col-3">
					</div>
					<div class="col-9 text-right">
			`;
			let query_params = frappe.utils.get_query_params();
			let start = query_params.start ? cint(JSON.parse(query_params.start)) : 0;
			let page_length = settings.products_per_page || 0;

			let prev_disable = start > 0 ? "" : "disabled";
			let next_disable = (this.product_count > page_length) ? "" : "disabled";

			paging_html += `
				<button class="plp-nav-btn plp-prev-btn btn-prev" 
					data-start="${ start - page_length }"
					${prev_disable}>
					← Prev
				</button>`;
				

			paging_html += `
				<button class="plp-nav-btn plp-next-btn btn-next"
					data-start="${ start + page_length }"
					${next_disable}>
					Next →
				</button>
			`;

			paging_html += `</div></div>`;

			$(".page_content").append(paging_html);
			this.bind_paging_action();
		}
	}
  
}

// Override the default ProductView with CustomProductView
webshop.ProductView = KarpProductView;


//Mobile Filter Logic
frappe.ready(function() {
  const desktopFiltersSelector = '#product-filters';   // your filters wrapper
  const mobileBtn = document.getElementById('mobile-filter-btn');
  const drawer = document.getElementById('mobile-filter-drawer');
  const drawerBody = drawer && drawer.querySelector('.mobile-filter-body');
  const closeBtn = document.getElementById('mobile-filter-close');
  const applyBtn = document.getElementById('mobile-filter-apply');
  const clearBtn = document.getElementById('mobile-filter-clear');
  const backdrop = drawer && drawer.querySelector('.mobile-filter-backdrop');

  if (!mobileBtn || !drawer || !drawerBody) return;

  // Utility: remove id attributes from cloned subtree
  function removeIds(node) {
    if (!node || !node.querySelectorAll) return;
    node.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
	node.removeAttribute('id')
  }

  // copy checked state from desktop -> clone
  function syncDesktopToClone(clone) {
	
    // For each checkbox in clone, find corresponding desktop checkbox by data-filter-name & data-filter-value
    const cloneInputs = clone.querySelectorAll('input[type="checkbox"], input[type="radio"], select');
	
    cloneInputs.forEach(ci => {
      const name = ci.getAttribute('data-filter-name');
      const value = ci.getAttribute('data-filter-value');
      if (!name) return;

      // find desktop input(s)
      // desktop inputs use same attributes in your macro: data-filter-name & data-filter-value
      const desktopSelector = `[data-filter-name="${name}"][data-filter-value="${value}"]`;
      const desktopInput = document.querySelector(desktopSelector);
      if (desktopInput) {
        // set checked / value according to desktop
        if (desktopInput.type === 'checkbox' || desktopInput.type === 'radio') {
          ci.checked = desktopInput.checked;
        } else {
          ci.value = desktopInput.value;
        }
      }
    });

  }

  // Remove unwanted elements
  function cleanClone(clone) {
	if (clone && window.innerWidth < 768) {
		clone.classList.remove('collapse');
		// optionally ensure it's visible on mobile
		clone.classList.remove('d-none');
	}
	const desktopFilterTitle = clone.querySelector('.filters-title');
	if (desktopFilterTitle) desktopFilterTitle.remove();
	const desktopClearFilter = clone.querySelector('.clear-filters');
	if (desktopClearFilter) desktopClearFilter.remove();
  }

  // copy checked state from clone -> desktop and trigger change events so site's filter logic runs
  function syncCloneToDesktop(clone) {
    const cloneInputs = clone.querySelectorAll('input[type="checkbox"], input[type="radio"], select');
	const desktopFilters = document.querySelector(desktopFiltersSelector);
    cloneInputs.forEach(ci => {
      const name = ci.getAttribute('data-filter-name');
      const value = ci.getAttribute('data-filter-value');
      if (!name) return;

      const desktopSelector = `[data-filter-name="${name}"][data-filter-value="${value}"]`;
      const desktopInput = desktopFilters.querySelector(desktopSelector);
      if (desktopInput) {
        if (desktopInput.type === 'checkbox' || desktopInput.type === 'radio') {
          if (desktopInput.checked !== ci.checked) {
            desktopInput.checked = ci.checked;
          }
        } else {
          if (desktopInput.value !== ci.value) {
            desktopInput.value = ci.value;
          }
        }
      }
    });
  }

  function openDrawer() {
    // find desktop filters
    const desktopFilters = document.querySelector(desktopFiltersSelector);
    if (!desktopFilters) {
      console.warn('No desktop filters found for selector:', desktopFiltersSelector);
      return;
    }

    // deep clone to avoid moving DOM (keeps desktop intact)
    const clone = desktopFilters.cloneNode(true);

	clone.classList.add('mobile-clone');

    // strip ids to avoid duplicates and invalid HTML
    removeIds(clone);

    // sync checked states from desktop -> clone
    syncDesktopToClone(clone);

	cleanClone(clone);

    // inject clone
    drawerBody.innerHTML = '';
    drawerBody.appendChild(clone);
	


    // show drawer
    drawer.style.display = 'block';
    drawer.setAttribute('aria-hidden', 'false');
    document.documentElement.classList.add('no-scroll');

    // re-enable any interactive widgets inside clone if needed (e.g. search inputs)
    // For example: attach any live-search handlers if present
  }

  function closeDrawer() {
    drawer.style.display = 'none';
    drawer.setAttribute('aria-hidden', 'true');
    drawerBody.innerHTML = '';
    document.documentElement.classList.remove('no-scroll');
  }

  function applyFilters() {
    const clone = drawerBody.querySelector(desktopFiltersSelector) || drawerBody.firstElementChild;
    if (!drawerBody) {
      closeDrawer();
      return;
    }

    // copy state back to desktop and trigger change events so existing handlers run
    syncCloneToDesktop(drawerBody);

	const productView = window.karp_product_view;
	if (productView) {
		productView.getResultFromFilters();
	}

    // If your site has a function that applies filters (e.g., refresh via AJAX), call it:
    // if (typeof applyFilters === 'function') { applyFilters(); }
    // Otherwise, the change events should have triggered the site's filter logic.
    closeDrawer();
  }

  function clearFilters() {
    // Uncheck/clear all inputs inside clone and desktop
    // Desktop
    document.querySelectorAll(desktopFiltersSelector + ' input[type="checkbox"], ' + desktopFiltersSelector + ' input[type="radio"]').forEach(el => {
      if (el.checked) {
        el.checked = false;
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
    });
    document.querySelectorAll(desktopFiltersSelector + ' select').forEach(el => {
      el.value = '';
      el.dispatchEvent(new Event('change', { bubbles: true }));
    });

    // Clone (if present)
    drawerBody.querySelectorAll('input[type="checkbox"], input[type="radio"], select').forEach(el => {
      if (el.type === 'checkbox' || el.type === 'radio') el.checked = false;
      else el.value = '';
    });
  }

  // event wiring
  mobileBtn.addEventListener('click', openDrawer);
  closeBtn.addEventListener('click', closeDrawer);
  backdrop.addEventListener('click', closeDrawer);
  applyBtn.addEventListener('click', function(e) { e.preventDefault(); applyFilters(); });
  clearBtn.addEventListener('click', function(e) { e.preventDefault(); clearFilters(); });

  // Esc closes drawer
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && drawer.style.display === 'block') closeDrawer();
  });
});