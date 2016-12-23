============================
Global logging with flask
============================
:date: 2016-12-22
:category: programming
:tags: python, flask
:author: Yusuke Tsutsumi

As of December 2016, `Flask <http://flask.pocoo.org/>`_ has a built-in
logger that it instantiates for you. Unfortunately, this misses the
errors and other log messages in other libraries that may also be
valuable.

It would be nice to have a single logger, one that captures BOTH
library AND app logs. For those that want a global logger, this may
take a few concept to get right. You have to:

1. undo flask's logging
2. set up your own logging
3. set log levels, as the default may not suit you.

Combined, this ends up looking like:

.. code-block:: python

    import logging
    import sys
    from flask import Flask, current_app

    LOG = logging.getLogger("my_log")
    LOG2 = logging.getLogger(__name__ + ".toheunateh")
    app = Flask(__name__)


    @app.route("/")
    def route():
        current_app.logger.info("flask logger: foo")
        LOG.info("log: foo")
        LOG2.info("log2: foo")
        return "hello!"


    # create your own custom handler and formatter.
    # you can also use logging.basicConfig() to get
    # the python default.
    out_hdlr = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    out_hdlr.setFormatter(fmt)
    out_hdlr.setLevel(logging.INFO)
    # append to the global logger.
    logging.getLogger().addHandler(out_hdlr)
    logging.getLogger().setLevel(logging.INFO)
    # removing the handler and
    # re-adding propagation ensures that
    # the root handler gets the messages again.
    app.logger.handlers = []
    app.logger.propagate = True
    app.run()


And you get the right messages. Voila!
