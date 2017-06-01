import logging
import os
import sys


if sys.version_info[0] == 2:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


class Config(object):
    app = None

    def __init__(self, app=None):
        if not app:
            raise ValueError("A flask app must be passed to the configuration object.")
        self.app = app
        self.app.config["LOGGING_FORMAT"] = os.getenv(
            "LOGGING_FORMAT",
            "[%(asctime)s] [%(levelname)s]: %(message)s"
        )
        self.app.config["LOGGING_LEVEL"] = int(os.getenv("LOGGING_LEVEL", 10))
        logging.basicConfig(
            level=self.app.config["LOGGING_LEVEL"],
            format=self.app.config["LOGGING_FORMAT"]
        )

        self.app.config["AGENT_HOST"] = os.getenv("AGENT_HOST", None)
        self.app.config["AGENT_PORT"] = os.getenv("AGENT_PORT", None)
        self.app.config["AGENT_DEBUG"] = os.getenv("AGENT_DEBUG", None)
        self.app.config["COWBULL_URL"] = os.getenv("COWBULL_URL", None)

    def validate(self):
        self._check_app_set()

        logging_level = self.app.config["LOGGING_LEVEL"] or None
        if not logging_level:
            self.app.config["LOGGING_LEVEL"] = logging.DEBUG

        logging_format = self.app.config["LOGGING_FORMAT"] or None
        if not logging_format:
            self.app.config["LOGGING_FORMAT"] = "[%(asctime)s] [%(levelname)s]: %(message)s"

        agent_host = self.app.config["AGENT_HOST"] or None
        if not agent_host:
            self.app.config["AGENT_HOST"] = "0.0.0.0"

        agent_port = self.app.config["AGENT_PORT"] or None
        if not agent_port:
            self.app.config["AGENT_PORT"] = 5000

        agent_debug = self.app.config["AGENT_DEBUG"] or None
        if not agent_debug:
            self.app.config["AGENT_DEBUG"] = True

        cowbull_url = self.app.config["COWBULL_URL"] or None
        if not cowbull_url:
            raise ValueError("The game server (COWBULL_URL) is not set in "
                             "environment variables or configuration files "
                             "and cannot be defaulted! The agent cannot "
                             "start.")

    def load(self, filename=None):
        self._check_app_set()

        if not filename or filename == "":
            raise ValueError("The configuration filename cannot be empty")
        if not isinstance(filename, str):
            raise TypeError(
                "The configuration file can only be passed as a string (i.e. the filename and path)"
            )

        try:
            logging.debug("Opening configuration file '{}'.".format(filename))
            f = open(filename, 'r')
        except IOError:
            logging.debug("** Configuration Filename {} was not found!".format(filename))
            raise

        cp = ConfigParser()

        logging.debug("Loading configuration from file.")
        cp.readfp(f)
        f.close()

        if not cp.sections():
            logging.error("Empty configuration found. Nothing loaded.")
            return

        logging.debug("Config sections: {}".format(cp.sections()))

        for section in cp.sections():
            logging.debug("Processing configuration section '{}'".format(section))
            for parameter in cp.items(section):
                key = parameter[0].upper()
                value = parameter[1]
                logging.debug("Setting {} = {}".format(key, value))
                self.app.config[parameter[0].upper()] = parameter[1]

    def dump(self):
        self._check_app_set()

        logging.debug("Agent Host is {}".format(self.app.config["AGENT_HOST"]))
        logging.debug("Agent Port is {} (NB: value ignored by Docker and Kubernetes)".format(self.app.config["AGENT_PORT"]))
        logging.debug("Agent Debug is {} (NB: value ignored by Docker and Kubernetes)".format(self.app.config["AGENT_DEBUG"]))
        logging.debug("Logging format is {}".format(self.app.config["LOGGING_FORMAT"]))
        logging.debug("Logging level is {}".format(self.app.config["LOGGING_LEVEL"]))
        logging.debug("Cowbull URL is {}".format(self.app.config["COWBULL_URL"]))

    def _check_app_set(self):
        if not self.app:
            raise ValueError("APP is undefined!!")
