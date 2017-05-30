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

        try:
            digits_required = self._get_digits_required(context)
            digits_entered = self._get_digits_entered(parameters)
            self._check_digit_lengths(digits_entered=digits_entered, digits_required=digits_required)
        except ValueError as ve:
            return {
                "contextOut": [],
                "speech": str(ve),
                "displayText": str(ve)
            }

        return {
            "status": 200,
            "message": "",
            "contextOut": [],
            "speech": "Coming soon! Sorry, it's not ready yet.",
            "displayText": "Coming soon! Sorry, it's not ready yet."
        }

    def do_slot(self, context, parameters):
        pass

    def _get_digits_entered(self, parameters):
        digits_entered = [int(i) for i in parameters["digitlist"]]
        logging.debug("The digits input were: {}".format(digits_entered))
        return digits_entered

    def _get_digits_required(self, context):
        digits_required = int([i["parameters"]["digits"] for i in context if i["name"] == "digits"][0])
        logging.debug("{} digits are required.".format(digits_required))
        return digits_required

    def _check_digit_lengths(self, digits_entered, digits_required):
        if len(digits_entered) != digits_required:
            raise ValueError("You must enter {0} and only {0} digits".format(digits_required))

