/*!
 * jQuery Upvote - a voting plugin
 * ------------------------------------------------------------------
 *
 * jQuery Upvote is a plugin that generates a voting widget like
 * the one used on Stack Exchange sites.
 *
 * Licensed under Creative Commons Attribution 3.0 Unported
 * http://creativecommons.org/licenses/by/3.0/
 *
 * @version         1.0.2
 * @since           2013.06.19
 * @author          Janos Gyerik
 * @homepage        https://janosgyerik.github.io/jquery-upvote
 * @twitter         twitter.com/janosgyerik
 *
 * ------------------------------------------------------------------
 *
 *  <div id="topic" class="upvote">
 *    <a class="upvote"></a>
 *    <span class="count"></span>
 *    <a class="downvote"></a>
 *    <a class="star"></a>
 *  </div>
 *
 *  $('#topic').upvote();
 *  $('#topic').upvote({count: 5, upvoted: true});
 *
 */

;(function($) {
    "use strict";
    var namespace = 'upvote';

    function init(options) {
        return this.each(function() {
            methods.destroy.call(this);

            var count = parseInt($(this).find('.count').text());
            count = isNaN(count) ? 0 : count;
            var initial = {
                id: $(this).attr('data-id'),
                count: count,
                upvoted: $(this).find('.upvoted').size(),
                downvoted: $(this).find('.downvoted').size(),
                starred: $(this).find('.starred').size(),
                callback: function() {}
            };

            var data = $.extend(initial, options);
            if (data.upvoted && data.downvoted) {
                data.downvoted = false;
            }

            var that = $(this);
            that.data(namespace, data);
            render(that);
            setupUI(that);
        });
    }

    function setupUI(that) {
        that.find('.upvote').addClass('upvote-enabled');
        that.find('.downvote').addClass('upvote-enabled');
        that.find('.star').addClass('upvote-enabled');
        that.find('.upvote').on('click.' + namespace, function() {
            that.upvote('upvote');
        });
        that.find('.downvote').on('click.' + namespace, function() {
            that.upvote('downvote');
        });
        that.find('.star').on('click.' + namespace, function() {
            that.upvote('star');
        });
    }

    function _click_upvote() {
        this.find('.upvote').click();
    }

    function _click_downvote() {
        this.find('.downvote').click();
    }

    function _click_star() {
        this.find('.star').click();
    }

    function render(that) {
        var data = that.data(namespace);
        that.find('.count').text(data.count);
        if (data.upvoted) {
            that.find('.upvote').addClass('upvoted');
            that.find('.downvote').removeClass('downvoted');
        }
        else if (data.downvoted) {
            that.find('.upvote').removeClass('upvoted');
            that.find('.downvote').addClass('downvoted');
        }
        else {
            that.find('.upvote').removeClass('upvoted');
            that.find('.downvote').removeClass('downvoted');
        }
        if (data.starred) {
            that.find('.star').addClass('starred');
        }
        else {
            that.find('.star').removeClass('starred');
        }
    }

    function callback(that) {
        var data = that.data(namespace);
        data.callback(data);
    }

    function upvote() {
        var data = this.data(namespace);
        if (data.upvoted) {
            data.upvoted = false;
            --data.count;
        }
        else {
            data.upvoted = true;
            ++data.count;
            if (data.downvoted) {
                data.downvoted = false;
                ++data.count;
            }
        }
        render(this);
        callback(this);
        return this;
    }

    function downvote() {
        var data = this.data(namespace);
        if (data.downvoted) {
            data.downvoted = false;
            ++data.count;
        }
        else {
            data.downvoted = true;
            --data.count;
            if (data.upvoted) {
                data.upvoted = false;
                --data.count;
            }
        }
        render(this);
        callback(this);
        return this;
    }

    function star() {
        var data = this.data(namespace);
        data.starred = ! data.starred;
        render(this);
        callback(this);
        return this;
    }

    function count() {
        return this.data(namespace).count;
    }

    function upvoted() {
        return this.data(namespace).upvoted;
    }

    function downvoted() {
        return this.data(namespace).downvoted;
    }

    function starred() {
        return this.data(namespace).starred;
    }

    var methods = {
        init: init,
        count: count,
        upvote: upvote,
        upvoted: upvoted,
        downvote: downvote,
        downvoted: downvoted,
        starred: starred,
        star: star,
        _click_upvote: _click_upvote,
        _click_downvote: _click_downvote,
        _click_star: _click_star,
        destroy: destroy
    };

    function destroy() {
        return $(this).each(function() {
            $(window).unbind('.' + namespace);
            $(this).removeClass('upvote-enabled');
            $(this).removeData(namespace);
        });
    }

    $.fn.upvote = function(method) {  
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        }
        else if (typeof method === 'object' || ! method) {
            return methods.init.apply(this, arguments);
        }
        else {
            $.error('Method ' + method + ' does not exist on jQuery.upvote');
        }
    };  
})(jQuery);
