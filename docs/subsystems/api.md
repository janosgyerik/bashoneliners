RESTful API Urls and actions
============================

Common query parameters
-----------------------

That is, parameters that you can use in the query string,
appended at the end of the URL after `?` mark.

- `limit`: limit the objects in the output
  + There is a built-in global limit which cannot be exceeded
  + Default: the build-in global limit, or specific limit depending on the URL

- `fields`: limit the fields of objects in the output
  + Comma separated list
  + Example: `id,title`
  + Default: no limit, or specific fields depending on the URL

- `page`: used for pagination purposes, must be an integer value, otherwise fall back to the default
  + Default: 1

- `sort`: fields to sort by
  + Comma separated list
  + Field names can be prefixed by `-` sign to indicate sorting in descending order
  + Example: `id,-title`
  + Default: specific sorting order depending on the URL

Common URL prefix
-----------------

All URLs listed on this page have a common prefix:

    /api/v1

The `/api` part is to isolate from the rest of the web interface.

The `/v1` part is for versioning.

OneLiners
---------

| URL           | Method | Action  | 
| ------------- |:------:|---------|
| | GET | |

References
----------

- http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api
- http://www.commandlinefu.com/site/api
