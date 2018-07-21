import configparser
import os
import json
from flask import Flask
from flask import request
from slackclient import SlackClient

config = configparser.ConfigParser()
config.read('config.ini')
slack_token = config['TEST']['TOKEN']

sc = SlackClient(slack_token)

elements = [{"type":"text", "label":"Question", "name":"question"}]
for i in range(1, 5):
	element_name = "option" + str(i)
	elements.append({"type":"text", "label":"Option", "name":element_name})
	if i > 2:
		elements[i]["optional"] = True

question_dialog = {"callback_id":"asked", "title":"Ask a Question!", "elements":elements}


# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def hello_world():
    dictionary = {
            'text': 'Hello from Slackroom!'
    }
    sc.api_call(
            "dialog.open",
            trigger_id=request.form.get('trigger_id'),
            dialog=question_dialog
    )
    response = application.response_class(
        response=json.dumps(dictionary),
        status=200,
        mimetype='application/json',
    )
    return response



# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
