import logging
import os


def log_config(app=None):
    if not app:
        raise ValueError("APP is undefined!!")

    logging.debug("Agent Host is {}".format(app.config["AGENT_HOST"]))
    logging.debug("Agent Port is {}".format(app.config["AGENT_PORT"]))
    logging.debug("Agent Debug is {}".format(app.config["AGENT_DEBUG"]))
    logging.debug("Logging format is {}".format(app.config["LOGGING_FORMAT"]))
    logging.debug("Logging level is {}".format(app.config["LOGGING_LEVEL"]))
    logging.debug("Cowbull URL is {}".format(app.config["COWBULL_URL"]))
