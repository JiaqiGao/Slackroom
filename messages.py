import os
import configparser
from slackclient import SlackClient

config = configparser.ConfigParser()
config.read('config.ini')
slack_token = config['TEST']['TOKEN']

sc = SlackClient(slack_token)

# sc.api_call(
#   "chat.postMessage",
#   channel="slackroom",
#   text="Hello from Shayna! :tada:"
# )

# channels = sc.api_call("channels.list").get("channels")


# for c in channels:
# 	print(c.get("name"))
# 	if (c.get("name") == "slackroom"):
# 		conversation_id = c.get("id")


# channel_members = sc.api_call(
# 	"conversations.members",
# 	channel=conversation_id)


# info = sc.api_call("conversations.info",
# 	channel=conversation_id)

# creator = info.get("channel").get("creator")


# print(creator)
# for member in channel_members.get("members"):
# 	print(member)
# 	sc.api_call(
# 		"chat.meMessage",
# 		channel="slackroom",
# 		text="Hey creator! Only you can see this message!"
# 		# user=member
# 	)

elements = [{"type":"text", "label":"Question", "name":"question"}]

for i in range(1, 5):
	element_name = "option" + str(i)
	elements.append({"type":"text", "label":"Option", "name":element_name})
	if i > 2:
		elements[i]["optional"] = True

question_dialog = {"callback_id":"asked", "title":"Ask a Question!", "elements":elements}

sc.api_call(
	"dialog.open",
	trigger_id="fdsfsdfs",
	dialog=question_dialog
)
