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
        app.config["LOGGING_FORMAT"] = os.getenv("LOGGING_FORMAT", "%(asctime)s %(levelname)s: %(message)s")
        app.config["LOGGING_LEVEL"] = int(os.getenv("LOGGING_LEVEL", 10))
        logging.basicConfig(
            level=app.config["LOGGING_LEVEL"],
            format=app.config["LOGGING_FORMAT"]
        )

        app.config["AGENT_HOST"] = os.getenv("AGENT_HOST", "0.0.0.0")
        agent_port = os.getenv("AGENT_PORT", -1)
        if agent_port == -1:
            agent_port = 5000
        else:
            logging.debug("** AGENT PORT SET ** Docker will ignore this value.")
        app.config["AGENT_PORT"] = agent_port

        agent_debug = os.getenv("AGENT_DEBUG", -1)
        if agent_debug == -1:
            agent_debug = True
        else:
            logging.debug("** AGENT DEBUG SET ** Docker will ignore this value.")
        app.config["AGENT_DEBUG"] = agent_debug

        app.config["COWBULL_URL"] = os.getenv("COWBULL_URL", None)
        if not app.config["COWBULL_URL"]:
            raise ValueError("The game server (environment variable COWBULL_URL) is not set! "
                             "The agent cannot start.")
    else:
        pass

    return
