import logging  # Use Python's standard logging
import os       # For getting OS environment variables
import sys      # For getting the Python version number
from flask import Flask

# ConfigParser differs between Python major versions 2 and 3; therefore, check
# the version being used and import from the correct package.
if sys.version_info[0] == 2:
    from ConfigParser import ConfigParser
else:
    from configparser import ConfigParser


class Config(object):
    """
    Configuration helper for the python_cowbull_agent app. When initialized, the object
    must be passed a Flask app and then stores the required settings in the object's
    config dictionary. They can then be referenced anywhere the object is used; for example,
    app.config["COWBULL_URL"] would return the setting for COWBULL_URL.
    """
    app = None
    """the representation of the Flask object"""

    def __init__(self, app=None):
        """
        Initializes the Config object and loads configuration from environment variables. The caller
        may then load additional settings from file(s) by calling Config.load(filename=). The object
        also includes a validate method, which allows
        :param app: Flask - A Flask object, typically initiated as...  app = Flask(...)
        """
        if not app:
            raise ValueError("A flask app must be passed to the configuration object.")
        if not isinstance(app, Flask):
            raise TypeError("Config must be passed an instance of a Flask object (i.e. app)")

        # Store the Flask object passed to the instantiation
        self.app = app

        # Set any values from env vars. NOTE: Logging format and level are THE ONLY values
        # to be defaulted. This is to enable Config itself to issue debug statements.
        #
        self.app.config["LOGGING_FORMAT"] = os.getenv(
            "LOGGING_FORMAT",
            "[%(asctime)s] [%(levelname)s]: %(message)s"
        )
        self.app.config["LOGGING_LEVEL"] = int(os.getenv("LOGGING_LEVEL", 10))
        logging.basicConfig(
            level=self.app.config["LOGGING_LEVEL"],
            format=self.app.config["LOGGING_FORMAT"]
        )

        # Get any env vars for config. NOTE, defaults are None.
        self.app.config["AGENT_HOST"] = os.getenv("AGENT_HOST", None)
        self.app.config["AGENT_PORT"] = os.getenv("AGENT_PORT", None)
        self.app.config["AGENT_DEBUG"] = os.getenv("AGENT_DEBUG", None)
        self.app.config["COWBULL_URL"] = os.getenv("COWBULL_URL", None)

    def validate(self):
        """
        Validate ensures that all settings have been configured or defaults them where
        possible. The only exception which will be raised is if the COWBULL_URL (the URL
        for the game server) has not been set, as the agent cannot run without it and
        cannot guess it.
        """
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
        """
        Load settings from a configuration file. The settings are loaded using ConfigParser.ConfigParser (
        Python 2) and configparser.ConfigParser (Python 3). Follow the documentation at
        https://docs.python.org/2/library/configparser.html (2+) and
        https://docs.python.org/3.3/library/configparser.html (3+).
        :param filename: a string representation of filename (and path), e.g. /path/to/config.ini. The file
        may be called anything.

        Important Notes:
        1. Although sections are supported, they are ignored. For example a section [foo] with
        a setting bar will be imported into the app.config dictionary but is never used.
        2. When the setting is called from app.config, it is up to the caller to cast the setting
        to the correct type.

        """
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
        """
        dump logs the values of all expected settings from the Flask app.config dictionary to
        the standard console out using debug statements. NOTE: If the logging level is set to
        INFO or higher, these statements will NOT show.
        """
        self._check_app_set()

        logging.debug("Agent Host is {}".format(self.app.config["AGENT_HOST"]))
        logging.debug("Agent Port is {} (NB: value ignored by Docker and Kubernetes)".format(self.app.config["AGENT_PORT"]))
        logging.debug("Agent Debug is {} (NB: value ignored by Docker and Kubernetes)".format(self.app.config["AGENT_DEBUG"]))
        logging.debug("Logging format is {}".format(self.app.config["LOGGING_FORMAT"]))
        logging.debug("Logging level is {}".format(self.app.config["LOGGING_LEVEL"]))
        logging.debug("Cowbull URL is {}".format(self.app.config["COWBULL_URL"]))

    def _check_app_set(self):
        """
        'Private' method which checks that the app is defined and that it is an instance of a Flask
        object.
        :return:
        """
        if not self.app:
            raise ValueError("APP is undefined!!")
        if not isinstance(self.app, Flask):
            raise TypeError("Config APP is not an instance of a Flask object (i.e. app)")
