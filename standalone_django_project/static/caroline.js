(function() {
    function createScript(src) {
	var script = document.createElement("script");
	script.type = "text/javascript";
	script.src = src;
	document.appendChild(script);
    };

    createScript("https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js");
    createScript("https://raw.github.com/carhartl/jquery-cookie/master/jquery.cookie.js");

    function viewedLightboxes() {
	var cookie = $.cookie('caroline.seen');
	if( !cookie ) { return {}; }
	return JSON.parse(cookie);
    };

    function addViewedLightbox(key) {
	var seen = viewedLightboxes();
	if( !seen[key] ) {
	    seen[key] = [];
	}
	seen[key].push(new Date());
	$.cookie('caroline.seen', JSON.stringify(seen), {
		expires: 365*3, path: '/'
	    });
    };
})();
