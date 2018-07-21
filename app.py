import os
from slackclient import SlackClient
import requests

msg = "https://slack.com/api/chat.postMessage"
info = "https://slack.com/api/channels.info"
invite_to_channel = "https://slack.com/api/channels.invite"


slack_token = os.environ["TOKEN"]
channel="CBVSC5QDC"
text="Welcome to Slackroom!"

# create channel and returns id
def create_channel(channel_name):
  create_channel = "https://slack.com/api/channels.create"
  create_channel_params = {'token': slack_token, 'name': channel_name}
  channel_post = requests.post(url=create_channel, params=create_channel_params)
  result = channel_post.json()
  return result

# add user to channel
def add_to_channel(userID, channelID):
  channel_invite_params = {'token': slack_token, 'channel': channelID, user: userID}
  channel_invite_post = requests.post(url=create_channel, params=channel_invite_params)
  result = channel_invite_post.json()
  return True



##################################################################

PARAMS = {'token':slack_token, 'channel':channel}

info_result = requests.get(url = info, params = PARAMS)

data = info_result.json()

members = data['channel']['members']

channel_name = create_channel("team_1")

print (channel_name)

#for member in members:
 # add_to_channel(member, channel_name)


#print (members)
#mem_info = []

#for i in members:
 # mem_param = {'token': slack_token, 'user': i}
  #mem_result = requests.get(url = "https://slack.com/api/users.info", params = mem_param).json()

  #print(mem_result['user']['name'])
  #mem_info.append(mem_result['user']['name'])

#print (mem_info)







