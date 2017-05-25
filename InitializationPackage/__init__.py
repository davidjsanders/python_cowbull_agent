from flask import Flask


app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static/',
    static_path='/static/'
)

app.config["AGENT_HOST"] = "0.0.0.0"
app.config["AGENT_PORT"] = 5000
app.config["AGENT_DEBUG"] = True
app.config["LOGGING_FORMAT"] = "%(asctime)s %(levelname)s: %(message)s"
app.config["LOGGING_LEVEL"] = 10
app.config["COWBULL_URL"] = "https://cowbull-test-project.appspot.com/v0_1/{}"