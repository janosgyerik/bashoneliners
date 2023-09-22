function bind_preview_markdown() {
    const converter = new showdown.Converter();
    $('.markdown').each(function () {
        var inputPane = $(this).find('textarea').eq(0);
        var previewPane = $('<div class="preview form-control col-md-6"/>');
        previewPane.height(inputPane.height());
        previewPane.width(inputPane.width());
        previewPane.insertAfter($(this));
        inputPane.keyup(function () {
            previewPane.html(converter.makeHtml(inputPane.val()));
        }).trigger('keyup');
        inputPane.scroll(function () {
            previewPane.scrollTop(inputPane.scrollTop());
            previewPane.scrollLeft(inputPane.scrollLeft());
        });
    });
}

function bind_dblclick_to_select_oneliner() {
    if (window.getSelection) {
        $('.oneliner .line').dblclick(function (e) {
            var element = $(this)[0];
            var selection = window.getSelection();
            var range = document.createRange();
            range.selectNodeContents(element);
            selection.removeAllRanges();
            selection.addRange(range);
        });
    }
}

function bind_upvote() {
    if (App.user_id == 'None') return;

    var callback = function (data) {
        if (!data) return;

        $.ajax({
            url: '/oneliners/ajax/oneliner/' + data.id + '/vote/',
            type: 'POST',
            data: {
                upvoted: data.newState.upvoted,
                downvoted: data.newState.downvoted,
                id: data.id,
                csrfmiddlewaretoken: App.csrftoken
            }
        });
    };

    $('div.upvotejs').each(function (i, item) {
        const $item = $(item);
        if ($item.attr('data-voting-disabled') === 'true') {
            return;
        }
        const oneliner_user_id = $item.attr('data-user-id');
        if (oneliner_user_id != App.user_id) {
            Upvote.create($item.attr('id'), { callback: callback });
        }
    });
}

$(document).ready(function () {
    bind_preview_markdown();
    bind_upvote();
    bind_dblclick_to_select_oneliner();
});
