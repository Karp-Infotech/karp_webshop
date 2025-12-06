(function () {
  try {


    // ---- 1. Check URL param first ----
    var params = new URLSearchParams(window.location.search);
    var hse = params.get('hse');

    if (hse) {
      // Store cookie from URL param
      document.cookie = "hse=" + hse + "; path=/; SameSite=Lax";
      return;
    }

    // ---- 2. If cookie exists, stop ----
    var existing = (document.cookie.match(/(?:^|;\s*)hse=([^;]+)/) || [])[1];
    if (existing !== undefined) {
      return; // Home service eligibility already evaluated
    }


    // ---- 3. No cookie + no param => Check server eligibility ----
    fetch("/api/method/karp_webshop.karp_webshop.api.home_service.is_customer_home_service_eligible", {
      method: "GET",
      credentials: "same-origin",
      headers: {
        "Accept": "application/json"
      }
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        // Expected: data.message = null, 0, 1
        if (data && data.message !== null && data.message !== undefined) {
          document.cookie = "hse=" + data.message + "; path=/; SameSite=Lax";
        }
      })
      .catch(function (err) {
        console && console.log("Home Service API Error:", err);
      });

  } catch (e) {
    console && console.log("Home Service Init Error:", e);
  }
})();
