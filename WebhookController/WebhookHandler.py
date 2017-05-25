import json
import logging
import requests
from InitializationPackage import app
from flask import render_template, request, Response
from flask.views import MethodView
from requests import exceptions
from werkzeug.exceptions import BadRequest


class WebhookHandler(MethodView):
    webhook_response = {
        "speech": None,
        "displayText": None,
        "data": {},
        "source": "cowbull-agent",
        "followupEvent": {},
        "contextOut": [],
        "result": None,             # Shouldn't be here - for testing only
        "parameters": None          # Shouldn't be here - for testing only
    }

    def post(self):
        cowbull_url = app.config.get("COWBULL_URL", None)

        logging.debug("Processing webhook")
        logging.debug("Game server is {}".format(cowbull_url))

        request_mimetype = request.headers.get('Content-Type', None)
        logging.debug("Content type of request is: {}".format(request_mimetype))

        if request_mimetype is None\
        or request_mimetype.lower() != "application/json":
            self.webhook_response = {
                "status": 400,
                "message": "content-type must be explicitly specified "
                           "as application/json"
            }
            return self._build_error_response(response=self.webhook_response)

        json_string = request.get_json(silent=True, force=True)

        if json_string is None:
            self.webhook_response = {
                "status": 400,
                "message": "No JSON data was provided"
            }
            return self._build_error_response(response=self.webhook_response)

        webhook_result = json_string.get('result', None)
        if webhook_result is not None:
            self.webhook_response["parameters"] = webhook_result.get('parameters', None)
            self.webhook_response["action"] = webhook_result.get('action', None)
        else:
            self.webhook_response = {
                "status": 400,
                "message": "No result data. The request from api.ai was badly formed!"
            }
            return self._build_error_response(response=self.webhook_response)

        self.webhook_response["speech"] = self.webhook_response["displayText"] = "Hello!"
        #webhook_response["payload"] = json_string

        return Response(
            status=200,
            mimetype="application/json",
            response=json.dumps(self.webhook_response)
        )

    def _build_error_response(
            self,
            status_code=400,
            response=None
    ):
        logging.error(
            "HTML Status: {}; Response: {}".format(status_code, response)
        )
        return Response(
            status=status_code,
            mimetype="application/json",
            response=json.dumps(response)
        )
