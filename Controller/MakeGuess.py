import logging
import requests
from AbstractAction import AbstractAction
from InitializationPackage import app


class MakeGuess(AbstractAction):
    def __init__(self):
        super(MakeGuess, self).__init__()
        logging.debug("MakeGuess: In __init__ for make guess fulfillment")

    def do_action(self, context=None, parameters=None):
        logging.debug("MakeGuess: In do_action for make guess fulfillment")
        logging.debug("MakeGuess: Context: {}. Parameters: {}.".format(context, parameters))

        digits_required = int([i["parameters"]["digits"] for i in context if i["name"] == "digits"][0])
        logging.debug("{} digits are required.".format(digits_required))

        digits_entered = [int(i) for i in parameters["digitlist"]]
        logging.debug("The digits input were: {}".format(digits_entered))

        return {
            "status": 200,
            "message": "",
            "contextOut": [],
            "speech": "Coming soon! Sorry, it's not ready yet.",
            "displayText": "Coming soon! Sorry, it's not ready yet."
        }

    def do_slot(self, context, parameters):
        pass
