/*
 * UpvoteJS - a Stack Exchange look-alike voting widget
 * ----------------------------------------------------
 *
 * UpvoteJS is a widget that generates a voting widget like
 * the one used on Stack Exchange sites.
 *
 * Licensed under Creative Commons Attribution 3.0 Unported
 * http://creativecommons.org/licenses/by/3.0/
 *
 * @version         2.1.0
 * @since           2018.12.05
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
 *  Upvote.create('id');
 *  Upvote.create('id', {count: 5, upvoted: true});
 *
 */

const Upvote = function() {
  const upvoteClass = 'upvote';
  const enabledClass = 'upvotejs-enabled';
  const upvoteOnClass = 'upvote-on';
  const downvoteClass = 'downvote';
  const downvoteOnClass = 'downvote-on';
  const starClass = 'star';
  const starOnClass = 'star-on';
  const countClass = 'count';

  const Utils = {
    combine: function() {
      const combined = {};
      for (let i = 0; i < arguments.length; i++) {
        Object.entries(arguments[i])
          .filter(e => e[1] !== undefined)
          .forEach(e => combined[e[0]] = e[1]);
      }

      return combined;
    },
    isBoolean: v => typeof v === "boolean",
    isFunction: v => typeof v === "function",
    classes: dom => dom.className.split(/ +/).filter(x => x),
    removeClass: (dom, className) => {
      dom.className = dom.className.split(/ +/)
        .filter(x => x)
        .filter(c => c !== className)
        .join(' ');
    },
    noop: () => {}
  };

  const Model = function() {
    const validate = params => {
      if (!Number.isInteger(params.count)) {
        throw 'error: parameter "count" must be a valid integer';
      }
      if (!Utils.isBoolean(params.upvoted)) {
        throw 'error: parameter "upvoted" must be a boolean';
      }
      if (!Utils.isBoolean(params.downvoted)) {
        throw 'error: parameter "downvoted" must be a boolean';
      }
      if (!Utils.isBoolean(params.starred)) {
        throw 'error: parameter "starred" must be a boolean';
      }
      if (params.callback && !Utils.isFunction(params.callback)) {
        throw 'error: parameter "callback" must be a function';
      }
      if (params.upvoted && params.downvoted) {
        throw 'error: parameters "upvoted" and "downvoted" must not be true at the same time';
      }
    };

    const create = params => {
      validate(params);

      const data = Utils.combine(params);

      const upvote = () => {
        if (data.upvoted) {
          data.count--;
        } else {
          data.count++;
          if (data.downvoted) {
            data.downvoted = false;
            data.count++;
          }
        }
        data.upvoted = !data.upvoted;
      };

      const downvote = () => {
        if (data.downvoted) {
          data.count++;
        } else {
          data.count--;
          if (data.upvoted) {
            data.upvoted = false;
            data.count--;
          }
        }
        data.downvoted = !data.downvoted;
      };

      return {
        count: () => data.count,
        upvote: upvote,
        upvoted: () => data.upvoted,
        downvote: downvote,
        downvoted: () => data.downvoted,
        star: () => data.starred = !data.starred,
        starred: () => data.starred,
        data: () => Utils.combine(data)
      };
    };

    return {
      create: create
    };
  }();

  const View = function() {
    const create = id => {
      const dom = document.getElementById(id);
      if (dom === null) {
        throw 'error: could not find element with ID ' + id + ' in the DOM';
      }

      if (Utils.classes(dom).includes(enabledClass)) {
        throw 'error: element with ID ' + id + ' is already in use by another upvote controller';
      }
      dom.className += ' ' + enabledClass;

      const firstElementByClass = className => {
        const list = dom.getElementsByClassName(className);
        if (list === null) {
          throw 'error: could not find element with class ' + className + ' within element with ID ' + id + ' in the DOM';
        }
        return list[0];
      };

      const createCounter = className => {
        const dom = firstElementByClass(className);

        if (dom === undefined) {
          return {
            count: () => undefined,
            set: Utils.noop
          };
        }

        return {
          count: () => parseInt(dom.innerHTML || 0, 10),
          set: value => dom.innerHTML = value
        };
      };

      const createToggle = (className, activeClassName) => {
        const createClasses = () => {
          const classes = {
            [className]: true,
            [activeClassName]: false,
          };
          item.className.split(/ +/)
            .filter(x => x)
            .forEach(className => classes[className] = true);
          return classes;
        };

        const formatClassName = () => {
          return Object.entries(classes)
            .filter(e => e[1])
            .map(e => e[0])
            .join(' ');
        };

        const item = firstElementByClass(className);
        if (item === undefined) {
          return {
            get: () => false,
            set: Utils.noop,
            onClick: Utils.noop
          };
        }

        const classes = createClasses();

        return {
          get: () => classes[activeClassName],
          set: value => {
            classes[activeClassName] = value;
            item.className = formatClassName();
          },
          onClick: fun => item.onclick = fun
        };
      };

      const render = model => {
        counter.set(model.count());
        upvote.set(model.upvoted());
        downvote.set(model.downvoted());
        star.set(model.starred());
      };

      const parseParamsFromDom = () => {
        return {
          count: counter.count(),
          upvoted: upvote.get(),
          downvoted: downvote.get(),
          starred: star.get()
        };
      };

      const destroy = () => {
        Utils.removeClass(dom, enabledClass);
        upvote.onClick(null);
        downvote.onClick(null);
        star.onClick(null);
      };

      const counter = createCounter(countClass);
      const upvote = createToggle(upvoteClass, upvoteOnClass);
      const downvote = createToggle(downvoteClass, downvoteOnClass);
      const star = createToggle(starClass, starOnClass);

      return {
        render: render,
        parseParamsFromDom: parseParamsFromDom,
        onClickUpvote: fun => upvote.onClick(fun),
        onClickDownvote: fun => downvote.onClick(fun),
        onClickStar: fun => star.onClick(fun),
        destroy: destroy
      };
    };

    return {
      create: create
    };
  }();

  const create = (id, params = {}) => {
    var destroyed = false;
    const view = View.create(id);
    const domParams = view.parseParamsFromDom();
    const defaults = {
      id: id,
      count: 0,
      upvoted: false,
      downvoted: false,
      starred: false,
      callback: () => {}
    };
    const combinedParams = Utils.combine(defaults, domParams, params);
    const model = Model.create(combinedParams);

    const throwIfDestroyed = () => {
      if (destroyed) {
        throw "fatal: unexpected call to destroyed controller";
      }
    };

    const callback = action => {
      const data = model.data();
      combinedParams.callback({
        id: data.id,
        action: action,
        newState: {
          count: data.count,
          upvoted: data.upvoted,
          downvoted: data.downvoted,
          starred: data.starred
        }
      });
    };

    const upvote = () => {
      throwIfDestroyed();
      model.upvote();
      view.render(model);
      callback(model.upvoted() ? 'upvote' : 'unupvote');
    };

    const downvote = () => {
      throwIfDestroyed();
      model.downvote();
      view.render(model);
      callback(model.downvoted() ? 'downvote' : 'undownvote');
    };

    const star = () => {
      throwIfDestroyed();
      model.star();
      view.render(model);
      callback(model.starred() ? 'star' : 'unstar');
    };

    const destroy = () => {
      throwIfDestroyed();
      destroyed = true;
      view.destroy();
    };

    view.render(model);
    view.onClickUpvote(upvote);
    view.onClickDownvote(downvote);
    view.onClickStar(star);

    return {
      id: id,
      count: () => {
        throwIfDestroyed();
        return model.count();
      },
      upvote: upvote,
      upvoted: () => {
        throwIfDestroyed();
        return model.upvoted();
      },
      downvote: downvote,
      downvoted: () => {
        throwIfDestroyed();
        return model.downvoted();
      },
      star: star,
      starred: () => {
        throwIfDestroyed();
        return model.starred();
      },
      destroy: destroy
    };
  };

  return {
    create: create
  };
}();
