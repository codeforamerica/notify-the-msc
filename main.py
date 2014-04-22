from flask import Flask
from flask import render_template, jsonify, request
import sendgrid
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

try:
    sg_username = os.environ['SENDGRID_USERNAME']
    sg_password = os.environ['SENDGRID_PASSWORD']
    sg = sendgrid.SendGridClient(sg_username, sg_password, raise_errors=True)
except Exception as e:
    print "Missing SendGrid Config"
    raise e

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/incidents", methods=["POST"])
def submit_incident():
    errors = []  # list of all errors

    # verify pickup address not empty
    pickup_address = request.form.get('pickup_address', '')
    if len(request.form.get('pickup_address')) == 0:
        errors.append("empty_address")

    # verify hospital given
    if "hospital" not in request.form:
        errors.append("missing_hospital")

    if "interested" not in request.form:
        errors.append("missing_interested")

    if "homeless" not in request.form:
        errors.append("missing_homeless")

    if not errors:
        send_email_for_incident(request.form)
        return jsonify(status="ok")
    else:
        return jsonify(status="error", errors=errors), 400

def build_email_from_incident(incident):
    text_email_template = app.jinja_env.get_template('text_email')
    text_email = text_email_template.render(incident=incident)

    html_email_template = app.jinja_env.get_template('html_email')
    html_email = html_email_template.render(incident=incident)
    return {"html": html_email, "text": text_email}

def send_email_for_incident(incident):
    if app.config['TESTING']:
        return

    email_body = build_email_from_incident(incident)
    message = sendgrid.Mail()
    message.add_to(app.config['EMAIL_RECIPIENT'])
    message.set_subject('*ER Alert*')
    message.set_html(email_body['html'])
    message.set_text(email_body['text'])
    message.set_from('ER Alert <longbeach@codeforamerica.org>')

    try:
        sg.send(message)
    except sendgrid.SendGridClientError as e:
        print e  # @TODO: setup proper Python error logging
    except sendgrid.SendGridServerError as e:
        print e  # @TODO: setup proper Python error logging

if __name__ == "__main__":
    app.run()
