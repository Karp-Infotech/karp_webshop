(function(){
  try {
    var params = new URLSearchParams(window.location.search);
    var hse = params.get('hse');
    if (hse) {
       document.cookie = "hse=" + hse + "; path=/; SameSite=Lax";
    }
  } catch(e) { console && console.log(e); }
})();