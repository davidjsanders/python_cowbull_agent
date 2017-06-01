import logging
import os


def set_config(app=None):
    if not app:
        raise ValueError("APP is undefined!!")

    #
    # Expected OS Env Vars:
    # CONFIG_FILE    --> Optional configuration file
    # AGENT_HOST     --> 0.0.0.0                !! Only if using Flask to serve
    # AGENT_PORT     --> 5000                   !! "    "    "    "    "    "
    # LOGGING_FORMAT --> Python logging fmt     !! Default: "%(asctime)s %(levelname)s: %(message)s"
    # LOGGING_LEVEL  --> Python logging level   !! Default: 10 (logging.DEBUG)
    # COWBULL_URL    --> http://server:port/{}  !! Note NO TRAILING / and parameter for path IS required

    config_file = os.getenv("CONFIG_FILE", None)
    if not config_file:
        app.config["AGENT_HOST"] = os.getenv("AGENT_HOST", "0.0.0.0")
        app.config["AGENT_PORT"] = os.getenv("AGENT_PORT", 5000)
        app.config["AGENT_DEBUG"] = os.getenv("AGENT_DEBUG", True)
        app.config["LOGGING_FORMAT"] = os.getenv("LOGGING_FORMAT", "%(asctime)s %(levelname)s: %(message)s")
        app.config["LOGGING_LEVEL"] = os.getenv("LOGGING_LEVEL", 10)
        app.config["COWBULL_URL"] = os.getenv("COWBULL_URL", None)
        if not app.config["COWBULL_URL"]:
            raise ValueError("The game server (environment variable COWBULL_URL) is not set! "
                             "The agent cannot start.")
        logging.basicConfig(
            level=app.config["LOGGING_LEVEL"],
            format=app.config["LOGGING_FORMAT"]
        )
    else:
        pass

    return
