from flask import Flask
from flask import render_template, jsonify, request
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
    errors = [] # list of all errors

    # verify pickup address not empty
    pickup_address = request.form.get('pickup_address', '')
    if len(request.form.get('pickup_address')) == 0:
        errors.append("empty_address")

    # verify hospital given
    if "hospital" not in request.form:
        errors.append("missing_hospital")

    if not errors:
        return jsonify(status="ok")
    else:
        return jsonify(status="error", errors=errors), 400

if __name__ == "__main__":
    app.run()
