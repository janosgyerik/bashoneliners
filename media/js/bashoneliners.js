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
    if (obj.find('.oneliner').size() > 3) {
	obj.find('.details').each(function() {
	    var trigger = $('<div class="details-trigger"/>').click(function() {
		$(this).toggleClass('details-trigger-active').next().toggle('slow');
	    });
	    var has_explanation = $(this).find('.explanation').size() > 0;
	    var has_limitations = $(this).find('.limitations').size() > 0;
	    if (has_explanation && has_limitations) {
		trigger.text('Show explanation and limitations');
	    }
	    else if (has_explanation) {
		trigger.text('Show explanation');
	    }
	    else if (has_limitations) {
		trigger.text('Show limitations');
	    }
	    $(this).before(trigger);
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
    else {
	obj.find('.details').show();
    }
}

function hide_questionform() {
    if ($('.form-show-hide-trigger').size() > 0) {
	if ($('.questionform .errorlist').size() == 0) {
	    $('.questionform').hide();
	}

	$('.form-show-hide-trigger').click(function() {
	    $(this).toggleClass('details-trigger-active');
	    $('.questionform').toggle('slow');
	});

	$('.questionform .btn.cancel').click(function(e) {
	    e.preventDefault();
	    $('.form-show-hide-trigger').click();
	});
    }
}

$(document).ready(function() {
    bind_details_trigger($('div.oneliners'));
    hide_questionform();
});

// eof
