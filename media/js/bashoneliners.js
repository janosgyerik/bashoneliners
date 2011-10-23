/*!
 * Bash One-Liners JavaScript Library v0.1
 * http://bashoneliners.com/
 *
 * Copyright 2011, Janos Gyerik
 * http://bashoneliners.com/license
 *
 * Date: Sat Oct  8 06:38:28 CEST 2011
 */

function bind_details_trigger(obj) {
    $('<div class="details-trigger">Details...</div>').insertBefore(obj.find('.details')).click(function() {;
	$(this).toggleClass('details-trigger-active').next().toggle('slow');
    });
}

$(document).ready(function() {
    bind_details_trigger($('div.oneliners'));
});

// eof
