from slackclient import SlackClient
import os

slack_token = os.environ["TOKEN"]
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="slackroom",
  text="Hello from Python! :tada:"
)