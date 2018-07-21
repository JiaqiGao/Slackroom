import os
import configparser
from slackclient import SlackClient

config = configparser.ConfigParser()
config.read('config.ini')
slack_token = config['TEST']['TOKEN']

sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="slackroom",
  text="Hello from Winson! :tada:"
)
