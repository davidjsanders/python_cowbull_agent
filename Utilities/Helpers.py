############################################################################
# Module: Helpers.py                                                       #
# Author: D Sanders                                                        #
############################################################################
# Purpose: #
#                                                                          #
#                                                                          #
############################################################################

import importlib
import json
import logging
import requests


class Helpers(object):
    def __init__(self):
        pass

    def get_action_class(self, action=None):
        if not action:
            raise ValueError("Helpers:get_package: Action was set to None!")

        package_name = "{}".format(action)
        mod = importlib.import_module(
            "Controller.{}".format(package_name),
            package=package_name
        )
        return getattr(mod, package_name)

    @staticmethod
    def execute_post_request(url=None, data=None, headers=None):
        if headers is not None and not isinstance(headers, dict):
            raise TypeError("Headers supplied as a {}; it must be a dict".format(type(headers)))
        if data is not None and not isinstance(data, dict):
            raise TypeError("Data supplied as a {}; it must be a dict".format(type(data)))

        if not headers:
            headers = {"Content-Type": "application/json"}

        if not (headers.get("content-type") or headers.get("Content-Type")):
            headers["Content-Type"] = "application/json"

        r = None
        try:
            #
            logging.debug("Helper: Connecting to {}".format(url))
            r = requests.post(url=url, data=json.dumps(data), headers=headers)
        except Exception as e:
            raise IOError("Game reported an exception: {}".format(repr(e)))

        if r is not None:
            if r.status_code != 200:
                err_text = "Game reported an error: HTML Status Code = {}".format(r.status_code)
                if r.status_code == 404:
                    err_text = "The game engine reported a 404 (not found) error. The service may " \
                               "be temporarily unavailable"
                if r.status_code == 400:
                    json_output = r.json()
                    err_text = "{} -- {}".format(json_output["message"], json_output["exception"])
                raise IOError(err_text)
            else:
                return r.json()
        else:
            err_text = "Game reported an error: HTML Status Code = {}".format(r.status_code)
            raise IOError(err_text)


    @staticmethod
    def execute_get_request(url=None):
        r = None
        try:
            logging.debug("Helper: Connecting to {}".format(url))
            r = requests.get(url=url)
            #        except exceptions.ConnectionError as re:
            #            raise IOError("Game reported an error: {}".format(str(re)))
        except Exception as e:
            raise IOError("Game reported an exception: {}".format(repr(e)))

        logging.debug("_fetch_game: Game response --> {}".format(r.text))
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

    def validate_json(self, request_data=None):
        return_object = {}

        if not request_data:
            raise TypeError("Request data must be a Flask request object")

# TODO Class Check request_data
#        if not issubclass(request_data, request) or not isinstance(request_data, request):
#            raise TypeError("Request data is not a Flask request object")

        json_dictionary = request_data.get_json(force=True, silent=True, cache=False)
        if not json_dictionary:
            raise ValueError("There is no JSON data in the request")

        if not isinstance(json_dictionary["result"], dict):
            raise TypeError("The JSON is badly formed and is not a dictionary!")

        return_object = {
            "parameters": json_dictionary["result"]["parameters"],
            "contexts": json_dictionary["result"]["contexts"],
            "actionIncomplete": json_dictionary["result"]["actionIncomplete"],
            "action": json_dictionary["result"]["action"]
        }

        return return_object
