import logging
import requests
from AbstractAction import AbstractAction
from Helpers import Helpers
from InitializationPackage import app


class MakeGuess(AbstractAction):
    def __init__(self):
        super(MakeGuess, self).__init__()
        logging.debug("MakeGuess: In __init__ for make guess fulfillment")

    def do_action(self, context=None, parameters=None):
        logging.debug("MakeGuess: In do_action for make guess fulfillment")
        logging.debug("MakeGuess: Context: {}. Parameters: {}.".format(context, parameters))

        # Step 1 - Get a helper
        helper = Helpers()

        # Step 1 - Get the digits entered by the user and get the game key
        try:
            digits_required = self._get_digits_required(context)
            user_data = {
                "key": [n["parameters"]["key"] for n in context if n["name"] == "key"][0],
                "digits": self._get_digits_entered(parameters)
            }
        except ValueError as ve:
            return {
                "contextOut": [],
                "speech": str(ve),
                "displayText": str(ve)
            }

        # Step 2 - Send the request to the game server
        game_url = app.config.get("COWBULL_URL", None)
        if not game_url:
            raise ValueError("COWBULL_URL is not defined, so the game cannot be played")

        game_object = helper.execute_post_request(url=game_url, data=user_data)
        logging.debug("Game object returned: {}".format(game_object))

        return {
            "status": 200,
            "message": "",
            "contextOut": [],
            "speech": "Coming soon! Sorry, it's not ready yet.",
            "displayText": "Coming soon! Sorry, it's not ready yet."
        }

    def do_slot(self, context, parameters):
        pass

    @staticmethod
    def _get_digits_entered(parameters):
        digits_entered = [int(i) for i in parameters["digitlist"]]
        logging.debug("The digits input were: {}".format(digits_entered))
        return digits_entered

    @staticmethod
    def _get_digits_required(context):
        digits_required = int([i["parameters"]["digits"] for i in context if i["name"] == "digits"][0])
        logging.debug("{} digits are required.".format(digits_required))
        return digits_required

