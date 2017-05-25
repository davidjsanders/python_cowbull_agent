import requests
from requests import exceptions


class WebhookHelpers(object):
    game_modes = []
    cowbull_url = None

    def __init__(self, cowbull_url=None):
        if cowbull_url is None or not isinstance(cowbull_url, str):
            raise TypeError("The Cowbull game URL is incorrectly configured!")
        self.cowbull_url = cowbull_url

    def validate_mode(self, mode=None):
        #TODO Add caching for the game modes to avoid unwanted round trips

        _mode = mode or "normal"

        url = self.cowbull_url.format("modes")
        r = None

        try:
            r = requests.get(url=url)
        except exceptions.ConnectionError as re:
            error_message = "Game is unavailable: {}.".format(str(re))

        if r is not None:
            if r.status_code != 200:
                table = [{
                    "mode": "Game is unavailable. Status code {}".format(r.status_code),
                    "digits": "n/a", "guesses": "n/a"
                }]
            else:
                table = r.json()
                self.game_modes = str([str(mode["mode"]) for mode in table])\
                    .replace('[', '').replace(']', '').replace("'", "")
                if _mode in self.game_modes:
                    return True
                else:
                    return False
        else:
            return []
