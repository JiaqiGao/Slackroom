import json
import os
import configparser
import numpy as np
import matplotlib.pyplot as plt
from slackclient import SlackClient

config = configparser.ConfigParser()
config.read('config.ini')
slack_token = config['TEST']['TOKEN']

sc = SlackClient(slack_token)

class Question:

	def __init__(self, question, options):
		self.question = question
		self.options = options
		self.answers = {}
		self.respondable = True

	def build_json(self):
		buttons = {"text":question, "fallback":"Sorry, can't display the question right now.",
		"callback_id":question, "color":"#3AA3E3", "attachment_type":"default"}

		actions = []
		for option in options:
			single_button = {"name":"answer", "text":option, "type":"button", "value":option}
			actions.append(single_button)
		buttons["actions"] = actions

		return buttons

	def add_response(self, user, response):
		answers[response] += [user]

	def name(self):
		return self.question

	def respondable(self):
		return self.respondable

	def set_respondable(self, accepting):
		self.respondable = accepting

	def display_stats(self):
		response_numbers = {}
		for response in answers:
			response_numbers[response] = len(answers.get(response))
		
		plt.rcdefaults()
		fig, ax = plt.subplots()

		# Example data
		responses = list(response_numbers)
		y_pos = np.arange(len(responses))
		values = [response_numbers.get(val) for val in responses]

		ax.barh(y_pos, performance, align='center',
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

		sc.api_call (
		  "chat.postMessage",
		  channel=channel,
		  text="Here are the statistics!",
		  attachments=[image]
		)


response = json.loads(payload)

channel = response.get("channel").get("id")

responder = response.get("user").get("id")

questions = {}

active_q = None

# channel = "slackroom"

# response = {"callback_id":"asked", "submission":{"question": "Test question", "option1": "Hey!", "option2": "What", "option3": "yeet"}}

if response.get("callback_id") == "asked":
	submission = response.get("submission")
	question = submission.get("question")
	options = []

	for i in range(1, 5):
		option = submission.get("option" + str(i))
		if option != None:
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
	  attachments=[buttons]
	)

elif response.get("callback_id") == active_q.name() and active_q.respondable():

	action = response.get("actions")
	# q = questions.get(response.get("callback_id"))

	if action.get("name") == "answer":
		active_q.add_response(responder, action.get("value"))

elif command == "/stop":
	active_q.set_respondable(False)

elif command == "/stats":
	active_q.display_stats()

