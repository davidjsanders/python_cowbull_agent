from flask import request


class Helpers(object):
    def __init__(self):
        pass

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
