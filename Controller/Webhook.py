import json
import logging
from flask import request, Response
from Controller.Helpers import Helpers
from flask.views import MethodView


class Webhook(MethodView):
    def post(self):
        logging.debug("Webhook: Processing POST request")

        response_object = {
            "status": 200,
            "message": "success"
        }
        request_object = {}

        # Step 1: Instantiate a helper
        helper = Helpers()

        # Step 2: Get and validate the JSON in the request
        try:
            request_object = helper.validate_json(request_data=request)
        except KeyError as ke:
            response_object = self._handle_error(
                400,
                "The json is badly formed. Missing key {}".format(str(ke))
            )
        except (ValueError, TypeError) as e:
            response_object = self._handle_error(400, str(e))
        except Exception as e:
            response_object = self._handle_error(400, "Exception: {}".format(str(e)))

        # Step 3: Decide on the type of request
        try:
            slot_filling = request_object["actionIncomplete"]
            logging.debug("Slot filling? {}".format(slot_filling))
        except KeyError as ke:
            response_object = self._handle_error(
                400,
                "The json is badly formed. Missing key {}".format(str(ke))
            )

        # Step n: Return the response to the user.
        return Response(
            status=response_object["status"],
            response=json.dumps(response_object),
            mimetype="application/json"
        )

    def _handle_error(self, error_code, error_msg):
        logging.debug("Error Raised: {} {}".format(error_code, error_msg))
        return {
            "status": error_code,
            "message": error_msg
        }
