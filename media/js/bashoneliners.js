/*!
 * Bash One-Liners JavaScript Library v0.1
 * http://bashoneliners.com/
 *
 * Copyright 2011, Janos Gyerik
 * http://bashoneliners.com/license
 *
 * Date: Sat Oct  8 06:38:28 CEST 2011
 */

$(document).ready(function() {
    $('.help-markdown').click(function() {
	var url = this.href;
	var dialog = $('<div class="loading"></div>').appendTo('body');
	dialog.dialog({
	    close: function(event, ui) { dialog.remove(); },
	    height: 400,
	    width: 500,
	    title: 'Markdown Syntax Quick Reference'
	});
	dialog.load(
	    url,
	    '',
	    function(responseText, textStatus, XMLHttpRequest) {
		dialog.removeClass('loading');
	    }
	);
	return false;
    });
});

// eof
