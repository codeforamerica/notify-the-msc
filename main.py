from flask import Flask
from flask import render_template, jsonify
import os

app = Flask(__name__)

# Switch between configurations based on MSC_NOTIFIER_ENVIRONMENT env variable
config_to_use = 'config.DevelopmentConfig'
if 'MSC_NOTIFIER_ENVIRONMENT' in os.environ:
    if os.environ['MSC_NOTIFIER_ENVIRONMENT'] == "production":
        config_to_use = 'config.ProductionConfig'
    elif os.environ['MSC_NOTIFIER_ENVIRONMENT'] == "testing":
        config_to_use = 'config.TestingConfig'

app.config.from_object(config_to_use)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/incidents", methods=["POST"])
def submit_incident():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run()
