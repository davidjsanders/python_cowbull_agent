from __future__ import print_function

import json
import logging
import requests
from requests import exceptions


class WebhookHelpers(object):
    game_modes = []
    selected_mode = None
    cowbull_url = None

    def __init__(self, cowbull_url=None):
        if cowbull_url is None or not isinstance(cowbull_url, str):
            raise TypeError("The Cowbull game URL is incorrectly configured!")
        self.cowbull_url = cowbull_url

    def mkae_guess(self, key=None, digits_required=0, digits=[]):
        if key is None:
            raise ValueError("The key cannot be null (None), so a guess cannot be made.")

        if digits_required == 0:
            raise ValueError("The digits required are zero, so a guess cannot be made.")

        if not isinstance(digits_required, int):
            raise TypeError("digits_required must be an <int>; a {} was provided".format(type(digits_required)))

        if digits == [] or len(digits) != digits_required:
            raise ValueError("There must be {0} and only {0} digits".format(digits_required))

        url = self.cowbull_url.format('game')
        headers = {"Content-Type": "application/json"}
        payload = {
            "key": key,
            "digits": digits
        }
        r = None

        try:
            logging.debug("make_guess: Posting to {}".format(url))
            r = requests.post(url=url, headers=headers, data=json.dumps(payload))
        except exceptions.ConnectionError as re:
            raise IOError("Game reported an error: {}".format(str(re)))
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
                table = r.json()
                logging.debug('JSON returned is: {}'.format(table))
                return table
        else:
            err_text = "Game reported an error: HTML Status Code = {}".format(r.status_code)
            raise IOError(err_text)

    def fetch_new_game(self):
        if self.selected_mode is None:
            raise ValueError('The game mode is null (None), so a game cannot be started.')

        url = "{}?mode={}".format(self.cowbull_url.format('game'), self.selected_mode)
        r = None

        try:
            logging.debug("fetch_new_game: Connecting to {}".format(url))
            r = requests.get(url=url)
        except exceptions.ConnectionError as re:
            raise IOError("Game reported an error: {}".format(str(re)))
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
                table = r.json()
                return table
        else:
            err_text = "Game reported an error: HTML Status Code = {}".format(r.status_code)
            raise IOError(err_text)

    def validate_mode(self, mode=None):
        #TODO Add caching for the game modes to avoid unwanted round trips

        _mode = mode or "normal"

        url = self.cowbull_url.format("modes")
        r = None

        try:
            r = requests.get(url=url)
        except exceptions.ConnectionError as re:
            raise IOError("Game reported an error: {}".format(str(re)))
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
                table = r.json()
                self.game_modes = str([str(mode["mode"]) for mode in table])\
                    .replace('[', '').replace(']', '').replace("'", "")
                if _mode in self.game_modes:
                    self.selected_mode = _mode
                    return True
                else:
                    return False
        else:
            return []
