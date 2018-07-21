import os
from slackclient import SlackClient
import requests
import random

msg = "https://slack.com/api/chat.postMessage"
info = "https://slack.com/api/channels.info"


slack_token = os.environ["TOKEN"]
channel="CBVSC5QDC"
text="Welcome to Slackroom!"

# create channel and returns id
def create_channel(channel_name):
    create_channel = "https://slack.com/api/channels.create"
    params = {'token': slack_token, 'name': channel_name}
    channel_post = requests.post(url=create_channel, params=params)
    result = channel_post.json()
    return result["channel"]["id"]

# add user to channel
def add_to_channel(userID, channelID):
    invite_to_channel = "https://slack.com/api/channels.invite"
    params = {'token': slack_token, 'channel': channelID, 'user': userID}
    channel_invite_post = requests.post(url=invite_to_channel, params=params)
    result = channel_invite_post.json()
    return True

# send a message to channel
def send_message(channelID, text):
    send_message = "https://slack.com/api/chat.postMessage"
    params = {'token': slack_token, 'channel': channelID, 'text': text}
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
    mem_param = {'token': slack_token, 'user': userID}
    mem_result = requests.get(url="https://slack.com/api/users.info", params=mem_param).json()
    return mem_result['user']['name']




##################################################################

PARAMS = {'token':slack_token, 'channel':channel}

info_result = requests.get(url = info, params = PARAMS)

data = info_result.json()

members = data['channel']['members']

grouped = random_grouping(members, 3) #"".join(map(str, random_grouping(members, 2)))

msg = "Here are " + str(len(grouped)) + " groups of " + str(len(grouped[0])) + " students: "
for group in range(len(grouped)):
    for student in range(len(grouped[group])):
        if (student < len(grouped[0])-1):
            msg += get_name(grouped[group][student]) + " + "
        else:
            msg += get_name(grouped[group][student])
    msg += ", "

send_message("CBTUY2DUY", msg)

counter = 5
for group in grouped:
    channel_id = create_channel("team_"+str(counter))
    for student in group:
        add_to_channel(student, channel_id)
    counter += 1








