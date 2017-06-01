import os
from flask import Flask
from Utilities.Config import Config


# Initialize the Flask app
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static/',
    static_path='/static/'
)

# Get a configuration helper
config = Config(app=app)
config.dump()

# Get any OS Env Var set for CONFIG_FILE
config_file = os.getenv("CONFIG_FILE", None)

# If a configuration file was specified, then use values from there.
if config_file:
    config.load(filename=config_file)

# Validate the configuration
config.validate()

# Dump the configuration that's been set.
config.dump()
