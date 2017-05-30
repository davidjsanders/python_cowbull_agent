import logging
import requests
from InitializationPackage import app


class NewGame(object):
    def __init__(self):
        logging.debug("NewGame: In __init__ for new game fulfillment")

    def do_action(self, context=None, parameters=None):
        logging.debug("NewGame: Context: {}. Parameters: {}.".format(context, parameters))

        if context is None or parameters is None:
            raise ValueError("Context and/or Parameters must be set")

        mode = parameters["mode"]
        mode_valid = self._validate_mode(mode=mode)
        if not mode_valid:
            raise ValueError("The mode you entered ({}) isn't supported".format(mode))

        return self._fetch_game(mode=mode)

    def do_slot(self, context=None, parameters=None):
        logging.debug("NewGame: Context: {}. Parameters: {}.".format(context, parameters))

        if context is None or parameters is None:
            raise ValueError("Context and/or Parameters must be set")

        return {"modes": self._fetch_modes()}

    def _fetch_game(self, mode=None):
        output = {}

        game_url = app.config.get("COWBULL_URL", None)
        if not game_url:
            raise ValueError("COWBULL_URL is not defined, so the game cannot be played")

        url = game_url.format("game") + "?mode={}".format(mode)

        game_object = self._execute_request(url=url)

        output["contextOut"] = [
            {"name": "digits", "lifespan": 15, "parameters": {"digits": game_object["digits"]}},
            {"name": "guesses", "lifespan": 15, "parameters": {"guesses_remaining": game_object["guesses"]}},
            {"name": "key", "lifespan": 15, "parameters": {"key": game_object["key"]}},
            {"name": "served-by", "lifespan": 15, "parameters": {"served-by": game_object["served-by"]}}
        ]
        output["speech"] = output["displayText"] = \
            "Okay, I've started a new game. You have {} guesses to guess {} numbers." \
            .format(
                game_object["guesses"],
                game_object["digits"]
            )

        return output

    def _validate_mode(self, mode):
        # TODO Add caching for the game modes to avoid unwanted round trips

        _mode = mode or "normal"

        game_modes = self._fetch_modes()
        if _mode in game_modes:
            return True
        else:
            return False

    def _fetch_modes(self):
        game_url = app.config.get("COWBULL_URL", None)
        if not game_url:
            raise ValueError("COWBULL_URL is not defined, so the game cannot be played")

        url = game_url.format("modes")

        game_mode_query = self._execute_request(url=url)
        return str([str(mode["mode"]) for mode in game_mode_query]) \
            .replace('[', '').replace(']', '').replace("'", "")

    @staticmethod
    def _execute_request(url=None):
        try:
            logging.debug("fetch_new_game: Connecting to {}".format(url))
            r = requests.get(url=url)
#        except exceptions.ConnectionError as re:
#            raise IOError("Game reported an error: {}".format(str(re)))
        except Exception as e:
            raise IOError("Game reported an exception: {}".format(repr(e)))

        if r is not None:
            if r.status_code != 200:
                err_text = "Game reported an error: HTML Status Code = {}".format(r.status_code)
                if r.status_code == 404:
                    err_text = "The game engine reported a 404 (not found) error. The service may " \
                               "be temporarily unavailable"
                raise IOError(err_text)
            else:
                return r.json()
        else:
            err_text = "Game reported an error: HTML Status Code = {}".format(r.status_code)
            raise IOError(err_text)
