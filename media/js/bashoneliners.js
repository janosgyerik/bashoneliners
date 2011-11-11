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

    obj.find('.expand-all').prepend('<div class="expand-all-trigger">Expand all</div>');
    obj.find('.expand-all').prepend('<div class="collapse-all-trigger">Collapse all</div>');

    obj.find('.expand-all-trigger').click(function() {;
	obj.find('.details-trigger').addClass('details-trigger-active');
	obj.find('.details').show('slow');
    });

    obj.find('.collapse-all-trigger').click(function() {;
	obj.find('.details-trigger').removeClass('details-trigger-active');
	obj.find('.details').hide('slow');
    });
}

$(document).ready(function() {
    bind_details_trigger($('div.oneliners'));
});

// eof
