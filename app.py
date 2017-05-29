from __future__ import print_function

import logging
from InitializationPackage import app
from OldWebhookController.WebhookHandler import WebhookHandler
from Controller.Webhook import Webhook


logging.basicConfig(
    format=app.config["LOGGING_FORMAT"],
    level=app.config["LOGGING_LEVEL"]
)

old_webhook_handler = WebhookHandler.as_view('oldWebhook')
app.add_url_rule(
    rule='/old',
    view_func=old_webhook_handler,
    methods=["POST"]
)

webhook_handler = Webhook.as_view('webhook')
app.add_url_rule(
    rule='/',
    view_func=webhook_handler,
    methods=["POST"]
)


if __name__ == "__main__":
    app.run(
        host=app.config["AGENT_HOST"],
        port=int(app.config["AGENT_PORT"]),
        debug=app.config["AGENT_DEBUG"]
    )
