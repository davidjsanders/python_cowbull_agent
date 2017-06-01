from InitializationPackage.set_config import set_config
from InitializationPackage.log_config import log_config
from flask import Flask


# Step 1 - Get Configuration data
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static/',
    static_path='/static/'
)

set_config(app=app)
log_config(app=app)
#if config_file:
#    set_config(config_file=config_file, app=app)
#else:
#    app.config["AGENT_HOST"] = "0.0.0.0"
#    app.config["AGENT_PORT"] = 5000
#    app.config["AGENT_DEBUG"] = True
#    app.config["LOGGING_FORMAT"] = "%(asctime)s %(levelname)s: %(message)s"
#    app.config["LOGGING_LEVEL"] = 10
#    app.config["COWBULL_URL"] = "https://cowbull-test-project.appspot.com/v0_1/{}"
