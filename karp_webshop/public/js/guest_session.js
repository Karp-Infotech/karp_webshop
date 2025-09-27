

(function() {
    let sid = localStorage.getItem("guest_session_id");
    if (!sid) {
        sid = "GS-" + Math.random().toString(36).substr(2, 8);
        localStorage.setItem("guest_session_id", sid);
    }

    // 🚨 Make sure cookie is set for the whole domain
    document.cookie = "guest_session_id=" + sid + "; path=/; SameSite=Lax";
    console.log("guest_session_id set:", sid);

})();
