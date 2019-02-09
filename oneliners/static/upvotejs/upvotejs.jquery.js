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
 * @version         2.1.0
 * @since           2013.06.19
 * @author          Janos Gyerik
 * @homepage        https://janosgyerik.github.io/upvotejs
 * @twitter         twitter.com/janosgyerik
 *
 * ------------------------------------------------------------------
 *
 *  <div id="topic" class="upvotejs">
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
  const namespace = 'upvotejs';
  const enabledClass = 'upvotejs-enabled';

  function init(dom, options) {
    var total = 0;
    var failed = 0;
    var ret = dom.each(function() {
      const jqdom = $(this);
      methods.destroy(jqdom);

      const id = jqdom.attr('id');
      try {
        total++;
        const obj = Upvote.create(id, options);
        jqdom.data(namespace, obj);
      } catch {
        failed++;
      }
    });
    if (failed > 0) {
      throw 'error: failed to create ' + failed + '/' + total + ' controllers';
    }
    return ret;
  }

  function upvote(jqdom) {
    jqdom.data(namespace).upvote();
    return jqdom;
  }

  function downvote(jqdom) {
    jqdom.data(namespace).downvote();
    return jqdom;
  }

  function star(jqdom) {
    jqdom.data(namespace).star();
    return jqdom;
  }

  function count(jqdom) {
    return jqdom.data(namespace).count();
  }

  function upvoted(jqdom) {
    return jqdom.data(namespace).upvoted();
  }

  function downvoted(jqdom) {
    return jqdom.data(namespace).downvoted();
  }

  function starred(jqdom) {
    return jqdom.data(namespace).starred();
  }

  const methods = {
    init: init,
    count: count,
    upvote: upvote,
    upvoted: upvoted,
    downvote: downvote,
    downvoted: downvoted,
    starred: starred,
    star: star,
    destroy: destroy
  };

  function destroy(jqdom) {
    return jqdom.each(function() {
      const obj = jqdom.data(namespace);
      if (obj) {
        obj.destroy();
      }
      $(this).removeClass(enabledClass);
      $(this).removeData(namespace);
    });
  }

  $.fn.upvote = function(method) {  
    var args;
    if (methods[method]) {
      args = Array.prototype.slice.call(arguments, 1);
      args.unshift(this);
      return methods[method].apply(this, args);
    }
    if (typeof method === 'object' || ! method) {
      args = Array.prototype.slice.call(arguments);
      args.unshift(this);
      return methods.init.apply(this, args);
    }
    $.error('Method ' + method + ' does not exist on jQuery.upvote');
  };  
})(jQuery);
