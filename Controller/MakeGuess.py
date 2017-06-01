import logging
from Controller.AbstractAction import AbstractAction
from Controller.Helpers import Helpers
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
        game_url = app.config.get("COWBULL_URL", None).format("game")
        if not game_url:
            raise ValueError("COWBULL_URL is not defined, so the game cannot be played")

        guess_analysis = helper.execute_post_request(url=game_url, data=user_data)
        logging.debug("Game object returned: {}".format(guess_analysis))

        # Step 3 - Analyze the guess
        response_text = self._analyze_result(guess_analysis=guess_analysis)

        # Step 4 - Return the results
        output = {
            "contextOut": context,
            "speech": response_text,
            "displayText": response_text
        }

        return output

    def do_slot(self, context, parameters):
        pass

    @staticmethod
    def _analyze_result(guess_analysis):
        game = guess_analysis.get('game', None)
        status = game.get('status', None)
        guesses_remaining = int(game.get('guesses_remaining', 0))

        outcome = guess_analysis.get('outcome', None)
        message = outcome.get('message', None)
        analysis = outcome.get('analysis', None)
        cows = outcome.get('cows', 0)
        bulls = outcome.get('bulls', 0)

        if status.lower() in ["won", "lost"]:
            response_text = message
        else:
            message_text = ""
            for a in analysis:
                if a["match"]:
                    message_text += "{} is a bull".format(a["digit"])
                elif a["in_word"]:
                    message_text += "{} is a cow".format(a["digit"])
                else:
                    message_text += "{} is a miss".format(a["digit"])

                if a["multiple"]:
                    message_text += " and occurs more than once. "
                else:
                    message_text += ". "

            message_text += "You have {} goes remaining!".format(guesses_remaining)
            response_text = "You have {} cows and {} bulls. {}".format(cows, bulls, message_text)

        return response_text

    @staticmethod
    def _get_digits_entered(parameters):
        digits_entered = [int(i) for i in parameters["digitlist"]]
        logging.debug("The digits input were: {}".format(digits_entered))
        return digits_entered
