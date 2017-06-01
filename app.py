from __future__ import print_function

import logging
from InitializationPackage import app
from Controller.Webhook import Webhook


logging.basicConfig(
    format=app.config["LOGGING_FORMAT"],
    level=app.config["LOGGING_LEVEL"]
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
