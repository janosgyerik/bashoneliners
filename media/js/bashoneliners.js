/*!
 * Bash One-Liners JavaScript Library v0.1
 * http://bashoneliners.com/
 *
 * Copyright 2011, Janos Gyerik
 * http://bashoneliners.com/license
 *
 * Date: Sat Oct  8 06:38:28 CEST 2011
 */

function setupSearch() {
    $('#search').click(function(e) {
	e.preventDefault();
	$('#search-query').toggle('fast', function() {
	    if ($('#search-query').is(':visible')) {
		$('#search-query').focus();
	    }
	});
    });
    $('#search-query').keypress(function(e) {
	if (e.which == 13) {
	    e.preventDefault();
	    if ($('.oneliners').size() > 0) {
		// replace items in .oneliners using AJAX
	    }
	    else {
		$('#search-form').submit();
	    }
	}
    });
}

$(document).ready(function() {
    setupSearch();
});

// eof
