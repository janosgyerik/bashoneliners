/*!
 * Bash One-Liners JavaScript Library v0.1
 * http://bashoneliners.com/
 *
 * Copyright 2012, Janos Gyerik
 * http://bashoneliners.com/LICENSE
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
	var question = $('.' + $(this).attr('data-parent'));
	var remove_buttons = function() {
	    question.find('.question-answered').remove();
	};
	$.ajax({
	    url: $(this).attr('href'),
	    success: remove_buttons,
	    error: popup_error
	});
    });
}

function bind_preview_markdown() {
    $('.preview-markdown').click(function(e) {
	e.preventDefault();
	var source = $('#' + $(this).attr('data-source'));
	var preview = $('#' + $(this).attr('data-source') + '-preview');
	var update_preview = function(html) {
	    preview.html(html);
	    preview.addClass('well');
	};
	$.ajax({
	    url: $(this).attr('href'),
	    type: 'post',
	    data: { text: source.val() },
	    success: update_preview,
	    error: popup_error
	});
    });
}

function bind_comments_toggle() {
    $('.comments-toggle').click(function(e) {
	$(this).toggleClass('expanded').next().toggle(0);
    });
}

$(document).ready(function() {
    bind_help_markdown();
    bind_question_answered();
    bind_preview_markdown();
    bind_comments_toggle();
});

// eof
