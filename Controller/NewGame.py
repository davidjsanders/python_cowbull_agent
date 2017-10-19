import logging

from Controller.AbstractAction import AbstractAction
from InitializationPackage import app
from Utilities.Helpers import Helpers


class NewGame(AbstractAction):
    def __init__(self):
        super(NewGame, self).__init__()

    def do_action(self, context=None, parameters=None):
        logging.debug("NewGame: In do_action for new game fulfillment")
        logging.debug("NewGame: Context: {}. Parameters: {}.".format(context, parameters))

        if context is None or parameters is None:
            raise ValueError("Context and/or Parameters must be set")

        mode = parameters["mode"]
        mode_valid = self._validate_mode(mode=mode)
        if not mode_valid:
            raise ValueError("The mode you entered ({}) isn't supported".format(mode))

        return self._fetch_game(mode=mode)

    def do_slot(self, context=None, parameters=None):
        logging.debug("NewGame: In do_slot for new game fulfillment")
        logging.debug("NewGame: Context: {}. Parameters: {}.".format(context, parameters))

        if context is None or parameters is None:
            raise ValueError("Context and/or Parameters must be set")

        modes = self._fetch_modes()
        text_message = "Choose one of the following modes: {}".format(modes)
        output = {
            "contextOut": [
                {"name": "modes", "lifespan": 15, "parameters": {"digits": modes}}
            ],
            "speech": text_message,
            "displayText": text_message
        }

        return output

    @staticmethod
    def _fetch_game(mode=None):
        logging.debug("_fetch_game: Start")
        output = {}

        game_url = app.config.get("COWBULL_URL", None)
        if not game_url:
            raise ValueError("COWBULL_URL is not defined, so the game cannot be played")

        url = game_url.format("game") + "?mode={}".format(mode)
        logging.debug("_fetch_game: Game URL is {}".format(url))

        helper = Helpers()
        game_object = helper.execute_get_request(url=url)

        output["contextOut"] = [
            {"name": "key", "lifespan": 15, "parameters": {"key": game_object["key"]}}
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

    @staticmethod
    def _fetch_modes():
        game_url = app.config.get("COWBULL_URL", None)
        if not game_url:
            raise ValueError("COWBULL_URL is not defined, so the game cannot be played")

        url = game_url.format("modes")

        helper = Helpers()
        game_mode_query = helper.execute_get_request(url=url)

        modes = game_mode_query["modes"]
        return str([str(mode["mode"]) for mode in modes]) \
            .replace('[', '').replace(']', '').replace("'", "")
