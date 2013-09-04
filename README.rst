sentry-lighthouse
===========

A rudimentary extension for Sentry which allows you to create issues in
Lighthouse based on sentry events. Based originally on the much more
complete sentry-jira_.

.. _sentry-jira: https://github.com/thurloat/sentry-jira

Installation
------------

Install via pip (from repos because these packages are not yet in PyPI):

::

    pip install -e git+https://github.com/gthb/python-lighthouse-api#egg=lighthouse
    pip install -e git+https://github.com/gthb/sentry-lighthouse#egg=sentry_lighthouse


Configuration
-------------

Go to your project's configuration page (Projects -> [Project]) and select the
Lighthouse tab. Enter the Lighthouse credentials and Project configuration and save changes.


License
-------

sentry-lighthouse is licensed under the terms of the 3-clause BSD license.


Contributing
------------

All contributions are welcome, including but not limited to:

 - Documentation fixes / updates
 - New features (requests as well as implementations)
 - Bug fixes (see issues list)
