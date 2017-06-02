############################################################################
# Module: __init__.py                                                      #
############################################################################
# Purpose: Initializes the application, creates an instance of a Flask     #
#          object (app), and sets the configuration of the app. app is     #
#          created in an initialization package so it can be imported in   #
#          any package or module within the app.                           #
############################################################################

import os
from flask import Flask
from Utilities.Config import Config


# Initialize the Flask app and set the location of templates and statics
# folders, even though they aren't used in this app - they may be needed
# in future.

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static/',
    static_path='/static/'
)

# Get a configuration helper that will be used to set configuration values
# such as the URL of the game server.
config = Config(app=app)

# For logging purposes, dump the configuration.
config.dump()
