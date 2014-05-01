notify-the-msc
==============

Testing
------
To view on your local machine:
1. Type this to activate the virtual environment:
        source ENV/bin/activate
2. Type this to activate the framework:
        python main.py
3. Open your browser to http://localhost:5000

To test using a local browser, run `python functional_tests.py`.

To test using a remote browser and Sauce Labs, make sure the `SAUCE_USERNAME` and `SAUCE_ACCESS_KEY` environment variables are set, then run `NOTIFY_TEST_REMOTE_BROWSER=YES python functional_tests.py`.

[![Build Status](https://travis-ci.org/codeforamerica/notify-the-msc.svg?branch=master)](https://travis-ci.org/codeforamerica/notify-the-msc)
