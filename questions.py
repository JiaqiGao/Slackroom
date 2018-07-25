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

questionElements = [{"type": "text", "label": "Question", "name": "question"}]

questionElements.append({"type": "text", "label": "Class Name", "name": 'class_room'})
questionElements.append({"type": "select", "label": "", "name": 'class_room', "options": [
    {
        "label": "Monday",
        "value": "monday"
    },
    {
        "label": "Tuesday",
        "value": "tuesday"
    },
    {
        "label": "Wednesday",
        "value": "wednesday"
    },
    {
        "label": "Thursday",
        "value": "thursday"
    },
    {
        "label": "Friday",
        "value": "friday"
    }
]})

questionElements.append({"type": "text", "label": "Start Time", "name": 'start_time'})
questionElements.append({"type": "text", "label": "End Time", "name": 'end_time'})

questions_dialog = {"callback_id": "scheduled", "title": "Schedule Question Form", "elements": questionElements}

# EB looks for an 'application' callable by default.
application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
def schedule_command():
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

