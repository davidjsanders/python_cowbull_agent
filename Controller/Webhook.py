import json
import logging
import importlib
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

        try:
            # Step 2: Get and validate the JSON in the request
            request_object = helper.validate_json(request_data=request)
            if request_object == {}:
                raise ValueError("The request object returned is None!")

            slot_filling = request_object["actionIncomplete"]
            action_text = request_object["action"]

            logging.debug("Webhook: Processing action '{}' for {}".format(
                action_text,
                'slot filling' if slot_filling else 'fulfillment'
            ))

            action_class = helper.get_action_class(action=action_text)
            logging.debug("Webhook: Loaded action module")

            action = action_class()
            logging.debug("Webhook: Instantiated action class")

            if slot_filling:
                response_object["data"] = action.do_slot()
            else:
                response_object["data"] = action.do_action(
                    context=request_object["contexts"],
                    parameters=request_object["parameters"]
                )
        except KeyError as ke:
            response_object = self._handle_error(
                400,
                "The json is badly formed. Missing key {}".format(str(ke))
            )
        except Exception as e:
            response_object = self._handle_error(400, str(e))

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
