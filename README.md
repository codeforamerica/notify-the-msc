notify-the-msc
==============

Installation
------

Notify the MSC is a Python Flask application. To install Python in your local development environment, follow the dirctions for [Python & Virtualenv](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). The file `Procfile` contains the command for running the app; you can run it directly:

    $ python main.py
    
...or ask [Honcho](http://honcho.readthedocs.org/) to run it for you:

    $ pip install honcho
    $ honcho start

Testing
------
To test using a local browser, run `python functional_tests.py`.

To test using a remote browser and Sauce Labs, make sure the `SAUCE_USERNAME` and `SAUCE_ACCESS_KEY` environment variables are set, then run `NOTIFY_TEST_REMOTE_BROWSER=YES python functional_tests.py`.

[![Build Status](https://travis-ci.org/codeforamerica/notify-the-msc.svg?branch=master)](https://travis-ci.org/codeforamerica/notify-the-msc)
