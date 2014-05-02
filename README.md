notify-the-msc
==============

Team Long Beach's in-progress app for connecting emergency responders and follow-up outreach in Long Beach, California.

Testing
------
To test using a local browser, run `python functional_tests.py`.

To test using a remote browser and Sauce Labs, make sure the `SAUCE_USERNAME` and `SAUCE_ACCESS_KEY` environment variables are set, then run `NOTIFY_TEST_REMOTE_BROWSER=YES python functional_tests.py`.

[![Build Status](https://travis-ci.org/codeforamerica/notify-the-msc.svg?branch=master)](https://travis-ci.org/codeforamerica/notify-the-msc)
