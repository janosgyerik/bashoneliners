See Trello for a more up to date near-term todo list!
https://trello.com/board/main/4e7da3cf5a94680b35000893

social auth
-----------
+ poc: twitter
- poc: google
+ poc: yahoo
+ poc: launchpad
- poc: generic openid url
- poc: all relevant providers
    - make a list of providers used by users
    - verify each
- rework login page // simplify, replace dedicated boxes with single box
    - ok to add tooltip-like info box (bootstrap style) with example urls
- poc: verify smooth transition from old account to new
    - or else, plan migration


complete django 1.9 migration
-----------------------------
- upgrade to python 3
- sort out all reported false errors in pycharm
- unit tests working


cleaning
--------
- fix robots, verify google webmaster
- upgrade to latest django
- verify it works on server
- verify backups
- review and clean old todos
- review and clean trello
- review and clean all texts
- delete maintenance_urls


kick-ass REST API
-----------------
- incremental, continue supporting old endpoints
- use django-rest
- new API tab


collaborative editing
---------------------
- TODO
- differentiate (and distance) from stack overflow


gamification
------------
- TODO


OLD next
--------
- change RSS in navbar to Follow, and update the feeds page
    - mailing list
    - twitter
    - feature requests
    - bug reports
    - feeds
- bug: 500 error on /profile/ page when not logged in
- Implement favoriting
- Show number of starred questions
    - update first upstream in jquery-upvote
    - also better init examples
    - push new release of jquery-upvote
- what is bind_question_answered for?
- replace ugly static methods with more ergonomic ones:
    - oneliner.vote_up(user)
    - ...
- centralize the score counting (all annotate(..) magic in one place)
- switch to using social-auth
    - make sure existing accounts remain unaffected
- format everything with markdown
    - comments
- phase out AUTH_PROFILE_MODULE (deprecated in Django 1.5)


OLD future releases
-------------------
- See all own votes on profile page
- TOP 50
- mark as favourite
- ajax controls to change one-liner or question status from public to private
- the user who asked the question can mark the best answer
- api with different query options and output format options
- logo, better design


OLD minor
---------
- replace bashoneliners.com references using Sites
- add twitter user variable, useful in dev
- get SERVER* info in tweet admin command from settings
