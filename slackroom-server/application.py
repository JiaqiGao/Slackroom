import os
import json
import random
import configparser

from slackclient import SlackClient
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from flask import request, Flask

config = configparser.ConfigParser()
config.read('config.ini')
slack_token = config['TEST']['TOKEN']
slack_token_grouping = config['TEST']['TOKEN_GROUPING']

sc = SlackClient(slack_token)

elements = [{"type": "text", "label": "Question", "name": "question"}]
for i in range(1, 5):
    element_name = "option" + str(i)
    elements.append({"type": "text", "label": "Option", "name": element_name})
    if i > 2:
        elements[i]["optional"] = True

question_dialog = {"callback_id": "asked", "title": "Ask a Question!", "elements": elements}


class Question:

    question = ""
    options = []
    answers = {}
    respondable = True

    def __init__(self, question, options):
        self.question = question
        self.options = options

    def __str__(self):
        return self.question

    def build_json(self):
        buttons = {"text": self.question, "fallback": "Sorry, can't display the question right now.",
                   "callback_id": self.question, "color": "#3AA3E3", "attachment_type": "default"}

        actions = []
        for option in self.options:
            single_button = {"name": "answer", "text": option, "type": "button", "value": option}
            actions.append(single_button)
        buttons["actions"] = actions

        return buttons

    def add_response(self, user, response):
        self.answers[response] += [user]

    def name(self):
        return self.question

    def respondable(self):
        return self.respondable

    def set_respondable(self, accepting):
        self.respondable = accepting

    def display_stats(self):
        response_numbers = {}
        for response in self.answers:
            response_numbers[response] = len(self.answers.get(response))

        plt.rcdefaults()
        fig, ax = plt.subplots()

        # Example data
        responses = list(response_numbers)
        y_pos = np.arange(len(responses))
        values = [response_numbers.get(val) for val in responses]

        ax.barh(y_pos, values, align='center',
                color='blue', ecolor='black')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(responses)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Responses')
        ax.set_title(self.question)

        plt.savefig("pies.png")

        response_string = ""

        for response in response_numbers:
            response_string += response + ": " + str(response_numbers.get(response)) + "\n"

        image = {
            "fallback": "Here are the values for each response:\n" + response_string,
            "title": "Response statistics:",
            "text": "Here are the values!",
            "image_url": "pies.png",
            "color": "#764FA5"}

        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text="Here are the statistics!",
            attachments=[image]
        )

        return response_string



###################################################################################################

questionElements = [{"type": "text", "label": "Question", "name": "question"}]

questionElements.append({"type": "text", "label": "Class Name", "name": "class_room"})
questionElements.append({"type": "select", "label": "", "name": "class_room", "options": [
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

questionElements.append({"type": "text", "label": "Start Time", "name": "start_time"})
questionElements.append({"type": "text", "label": "End Time", "name": "end_time"})

questions_dialog = {"callback_id": "scheduled", "title": "Schedule Question Form", "elements": questionElements}
questions_dialog = {"callback_id": "scheduled", "title": "Schedule Question Form", "elements": questionElements}

# EB looks for an 'application' callable by default.
application = Flask(__name__)

msg = "https://slack.com/api/chat.postMessage"
info = "https://slack.com/api/channels.info"


# create channel and returns id
def create_channel(channel_name):
    create_channel = "https://slack.com/api/channels.create"
    params = {'token': slack_token_grouping, 'name': channel_name}
    channel_post = requests.post(url=create_channel, params=params)
    result = channel_post.json()
    return result["channel"]["id"]


# add user to channel
def add_to_channel(userID, channelID):
    invite_to_channel = "https://slack.com/api/channels.invite"
    params = {'token': slack_token_grouping, 'channel': channelID, 'user': userID}
    channel_invite_post = requests.post(url=invite_to_channel, params=params)
    result = channel_invite_post.json()
    return True


# send a message to channel
def send_message(channelID, text):
    send_message = "https://slack.com/api/chat.postMessage"
    params = {'token': slack_token_grouping, 'channel': channelID, 'text': text}
    send_message_post = requests.post(url=send_message, params=params)
    return True


# returns a list of lists, randoming grouping the members given a group size
def random_grouping(members, size):
    groups = []
    while len(members) > 0:
        group = []
        for i in range(size):
            mem = random.choice(members)
            group.append(mem)
            members.remove(mem)
        groups.append(group)
    return groups


# return name of user from user ID
def get_name(userID):
    mem_param = {'token': slack_token_grouping, 'user': userID}
    mem_result = requests.get(url="https://slack.com/api/users.info", params=mem_param).json()
    return mem_result['user']['name']


##################################################################


def form_group(members, size):
    grouped = random_grouping(members, size)  # "".join(map(str, random_grouping(members, 2)))

    msg = "Here are " + str(len(grouped)) + " groups of " + str(len(grouped[0])) + " students: "
    for group in range(len(grouped)):
        for student in range(len(grouped[group])):
            if (student < len(grouped[0]) - 1):
                msg += get_name(grouped[group][student]) + " + "
            else:
                msg += get_name(grouped[group][student])
        msg += ", "

    send_message("CBTUY2DUY", msg)

    channels = {}  # dict of channel ids: [memberids]
    counter = random.randint(0, 100000)
    for group in grouped:
        channel_id = create_channel("team" + str(counter))
        new_channel = []
        for student in group:
            add_to_channel(student, channel_id)
            new_channel.append(student)
        counter += 1
        send_message(channel_id, "Your new team consists of " + ", ".join([get_name(x) for x in group]))
        send_message(channel_id, "Create a team name!")
        channels["channel_id"] = new_channel

    # print(channels)


def init():
    channel = "CBVSC5QDC"

    PARAMS = {'token': slack_token_grouping, 'channel': channel}

    info_result = requests.get(url=info, params=PARAMS)

    data = info_result.json()

    members = data['channel']['members']
    form_group(members, 3)


active_q = None


@application.route('/', methods=['GET', 'POST'])
def hello_world():
    toReturn = 'huh?'
    global active_q
    print(request.form)
    channel = "slackroom"
    responder = "@shaynak"
    print(active_q)
    if 'payload' in request.form:
        toReturn = 'payloadz'
        payload = request.form.get('payload')
        payload = json.loads(payload)
        print(payload)
        channel = payload.get("channel").get("id")
        responder = payload.get("user").get("id")

        questions = {}

        if (payload.get('callback_id')) == 'asked':
            submission = payload.get("submission")
            question = submission.get("question")
            options = []

            for i in range(1, 5):
                option = submission.get("option" + str(i))
                if option is not None:
                    options.append(option)

            q = Question(question, options)

            active_q = q

            # questions.add("question":Question)

            buttons = q.build_json()

            print(buttons)

            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text="Please respond to this question!",
                attachments=[buttons])

        elif active_q is not None and payload.get("callback_id") == active_q.name() and active_q.respondable():
            action = payload.get("actions")
            # q = questions.get(response.get("callback_id"))

            if action.get("name") == "answer":
                active_q.add_response(responder, action.get("value"))

    elif request.form.get('command') == "/stop" and active_q is not None:
        toReturn = "Stopped!"
        active_q.set_respondable(False)

    elif request.form.get('command') == "/stats" and active_q is not None:
        toReturn = active_q.display_stats()

    elif request.form.get('command') == '/schedule':
        sc.api_call(
            "dialog.open",
            trigger_id=request.form.get('trigger_id'),
            dialog=questions_dialog
        )
        toReturn = 'Done Scheduling!'
    elif (request.form.get('command')) == '/ask':
        toReturn = 'Asking!'
        sc.api_call(
            "dialog.open",
            trigger_id=request.form.get('trigger_id'),
            dialog=question_dialog
        )
    elif (request.form.get('command')) == '/random-groups':
        toReturn = 'Forming groups!'
        init()
    dictionary = {
        "text": toReturn
    }
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
