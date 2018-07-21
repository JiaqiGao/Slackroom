import os
from slackclient import SlackClient

slack_token = os.environ["TOKEN"]
sc = SlackClient(slack_token)

# plan: random grouping...
#
#

# my own channel
sc.api_call(
  "chat.postMessage",
  channel="DBTNNDCHW",
  text="Test from Jiaqi! :tada:"
)
