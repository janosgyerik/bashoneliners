See Trello for a more up to date near-term todo list!
https://trello.com/board/main/4e7da3cf5a94680b35000893


release
-------
- make front page work again
- re-enable django openid auth, for easy review and matching of accounts
- merge branch to master
- make a backup on the server
- upgrade on server
- review all existing data and clean up any garbage


complete django 1.9 migration
-----------------------------
- upgrade to python 3
- sort out all reported false errors in pycharm
- unit tests working
- fix urls in templates


cleaning up
-----------
- fix robots, verify google webmaster
- upgrade to latest django
- verify it works on server
- verify backups
- review and clean old todos
- review and clean trello
- review and clean all texts
- delete maintenance_urls
- delete dreamhost views


post migration features
-----------------------
- command to merge users
    - change association from id_source to id_target
    - change id of all content having id_source to id_target


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
