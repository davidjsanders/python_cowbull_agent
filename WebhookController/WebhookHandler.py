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

        if not self._check_mimetype(request=request):
            return self._build_error_response(
                response="content-type must be explicitly specified as application/json"
            )

        json_string = request.get_json(silent=True, force=True)

        if json_string is None:
            return self._build_error_response(
                response="No JSON was provided in the request!"
            )

        webhook_result = json_string.get('result', None)
        if webhook_result is None:
            return self._build_error_response(
                response="No result data. The request was badly formed!"
            )

        action = webhook_result.get('action', None)
        logging.debug("Processing action: {}".format(action))

        parameters = webhook_result.get('parameters', None)
        logging.debug("Parameters are: {}".format(parameters))

        self.webhook_response["parameters"] = parameters
        self.webhook_response["action"] = action

        self.webhook_response["speech"] = self.webhook_response["displayText"] = "Hello!"
        #webhook_response["payload"] = json_string

        return Response(
            status=200,
            mimetype="application/json",
            response=json.dumps(self.webhook_response)
        )

    def _check_mimetype(self, request):
        request_mimetype = request.headers.get('Content-Type', None)
        logging.debug("Content type of request is: {}".format(request_mimetype))

        if request_mimetype is None\
        or request_mimetype.lower() != "application/json":
            return False

        return True

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
            response=json.dumps({
                "status": status_code,
                "message": response
            })
        )
