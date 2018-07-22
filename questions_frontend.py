import requests

import configparser
import os
import json
from flask import Flask
from flask import request
from slackclient import SlackClient

# config = configparser.ConfigParser()
# config.read('config.ini')
# slack_token = config['TEST']['TOKEN']
#
# sc = SlackClient(slack_token)
#
# elements = [{"type": "text", "label": "Question", "name": "question"}]
#
# elements.append({"type": "text", "label": "Class Name", "name": 'class_room'})
# elements.append({"type": "select", "label": "", "name": 'class_room', "options": [
#     {
#         "label": "Monday",
#         "value": "monday"
#     },
#     {
#         "label": "Tuesday",
#         "value": "tuesday"
#     },
#     {
#         "label": "Wednesday",
#         "value": "wednesday"
#     },
#     {
#         "label": "Thursday",
#         "value": "thursday"
#     },
#     {
#         "label": "Friday",
#         "value": "friday"
#     }
# ]})
#
# elements.append({"type": "text", "label": "Start Time", "name": 'start_time'})
# elements.append({"type": "text", "label": "End Time", "name": 'end_time'})
#
# question_dialog = {"callback_id": "scheduled", "title": "Schedule Question Form", "elements": elements}
#
# # EB looks for an 'application' callable by default.
# application = Flask(__name__)
#
# msg = "https://slack.com/api/chat.postMessage"
# info = "https://slack.com/api/channels.info"
#
# slack_token = os.environ["TOKEN"]
#
# @application.route('/schedule', methods=['GET', 'POST'])
# def schedule_command():
#     dictionary = {
#         'text': 'Hello from Slackroom!'
#     }
#     sc.api_call(
#         "dialog.open",
#         trigger_id=request.form.get('trigger_id'),
#         dialog=question_dialog
#     )
#     response = application.response_class(
#         response=json.dumps(dictionary),
#         status=200,
#         mimetype='application/json',
#     )
#     return response


def generate_question_summary(num_questions, lecture_date, class_name, num_top):
    return "There were {} questions asked for the {} lecture of {}.  " \
           "The top {} results are:".format(num_questions, lecture_date, class_name, num_top)


def generate_top_questions(list_questions):
    question_statement = generate_question_summary(len(list_questions), "09-14-2018", "CMSC412: Algorithms", 5)
    for x in range(0, 5):
        question_statement = question_statement + "\n" + list_questions[x].question +" "\
                             +str(list_questions[x].num_reactions)+" "+":thumbsup:"

    send_message(channel, question_statement)

class ListQ():

    def __init__(self, question, num_reactions):
        self.question=question
        self.num_reactions=num_reactions

testList = []
testList.append(ListQ("How do you solve a polynomial function?", 43))
testList.append(ListQ("What is the most difficult field of mathematics?", 7))
testList.append(ListQ("What is 3 * 7?", 6))
testList.append(ListQ("How do you find the asymptote of a parabola?", 5))
testList.append(ListQ("How do you find the inflection points of a graph?", 4))
testList.append(ListQ("What is 4 + 9?", 3))
print generate_top_questions(testList)
#
#
# channel = "CBVSC5QDC"
#
# PARAMS = {'token': slack_token, 'channel': channel}
#
# info_result = requests.get(url=info, params=PARAMS)
#
# data = info_result.json()
#
# members = data['channel']['members']
