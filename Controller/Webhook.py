import json
import logging
from AbstractAction import AbstractAction
from flask import request, Response
from Controller.Helpers import Helpers
from flask.views import MethodView


class Webhook(MethodView):
    def post(self):
        logging.debug("Webhook: Processing POST request")

        response_object = {
            "status": 200,
            "message": "success",
            "speech": None,
            "displayText": None,
            "data": {},
            "source": "cowbull-agent",
            "followupEvent": {},
            "contextOut": []
        }

        # Step 1: Instantiate a helper
        helper = Helpers()

        action_text = None
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
            if not issubclass(action_class, AbstractAction):
                raise TypeError("The action class is not a concrete implementation of AbstractAction")
            logging.debug("Webhook: Loaded action module")

            action = action_class()
            logging.debug("Webhook: Instantiated action class")

            if slot_filling:
                return_results = action.do_slot(
                    context=request_object["contexts"],
                    parameters=request_object["parameters"]
                )
            else:
                return_results = action.do_action(
                    context=request_object["contexts"],
                    parameters=request_object["parameters"]
                )
                logging.debug("Return results: {}".format(return_results))
            response_object["contextOut"] = return_results["contextOut"]
            response_object["speech"] = return_results["speech"]
            response_object["displayText"] = return_results["displayText"]

        except KeyError as ke:
            response_object = self._handle_error(
                400,
                "The json is badly formed. Missing key {}".format(str(ke))
            )
        except ImportError:
            response_object = self._handle_error(
                400,
                "Sorry, the action you wanted ({}), isn't available yet.".format(action_text)
            )
        except Exception as e:
            response_object = self._handle_error(400, str(e))

        # Step n: Return the response to the user.
        return Response(
            status=response_object["status"],
            response=json.dumps(response_object),
            mimetype="application/json"
        )

    @staticmethod
    def _handle_error(error_code, error_msg):
        logging.debug("Error Raised: {} {}".format(error_code, error_msg))

        error_text = "{} {}".format(error_code, error_msg)
        response_object = {
            "status": 200,
            "message": "success",
            "speech": error_text,
            "displayText": error_text,
            "data": {},
            "source": "cowbull-agent",
            "followupEvent": {},
            "contextOut": []
        }

        return response_object
