/*!
 * Bash One-Liners JavaScript Library v0.1
 * http://bashoneliners.com/
 *
 * Copyright 2011, Janos Gyerik
 * http://bashoneliners.com/license
 *
 * Date: Sat Oct  8 06:38:28 CEST 2011
 */

function popup_error() {
    alert('Oops! Whatever you were trying to do, it\'s not working now... Please try again later!\n\nIf the problem doesn\'t go away soon, send an email to info@bashoneliners.com');
}

function bind_help_markdown() {
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
}

function bind_question_answered() {
    $('.question-answered').click(function(e) {
	e.preventDefault();
	var me = $(this);
	var remove_buttons = function() {
	    me
	    .parent().parent().parent() // TODO
	    .find('.question-answered')
	    .remove();
	};
	$.ajax({
	    url: $(this).attr('href'),
	    success: remove_buttons,
	    error: popup_error
	});
    });
}

$(document).ready(function() {
    bind_help_markdown();
    bind_question_answered();
});

// eof
