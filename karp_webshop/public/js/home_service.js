(function(){
  try {
    var params = new URLSearchParams(window.location.search);
    var hse = params.get('hse');
    if (hse) {
      localStorage.setItem("hse", encodeURIComponent(hse));
    }
  } catch(e) { console && console.log(e); }
})();