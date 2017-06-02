from __future__ import print_function

from InitializationPackage import app
from Controller.Webhook import Webhook


# Create a view based on Controller.Webhook that
# will be added to the route /. NOTE: The only
# method supported is POST.
webhook_handler = Webhook.as_view('webhook')
app.add_url_rule(
    rule='/',
    view_func=webhook_handler,
    methods=["POST"]
)


# If the application is being run standalone, i.e.
# python app.py, then this section of code runs
# Flask's built-in server.
if __name__ == "__main__":
    app.run(
        host=app.config["AGENT_HOST"],
        port=int(app.config["AGENT_PORT"]),
        debug=app.config["AGENT_DEBUG"]
    )
