import os
from slackclient import SlackClient
import requests
import random
import configparser


msg = "https://slack.com/api/chat.postMessage"
info = "https://slack.com/api/channels.info"

dialog = "https://slack.com/api/dialog.open"


config = configparser.ConfigParser()
config.read('config.ini')
slack_token = config['TEST']['TOKEN']
sc = SlackClient(slack_token)


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
   # sc.api_call(
    #    "chat.postMessage",
     #   channel=channelID,
      #  text=text
    #)
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

def generate_team_name():
    with open('adjectives.txt', "r",encoding='utf-8', errors='ignore') as f:
        adj = f.read().split("\n")
    with open('nouns.txt', "r",encoding='utf-8', errors='ignore') as f:
        noun = f.read().split("\n")
    return random.choice(adj).capitalize() + " " + random.choice(noun).capitalize()



def grouping(members, size):
    grouped = random_grouping(members, size) #"".join(map(str, random_grouping(members, 2)))

    msg = "Here are " + str(len(grouped)) + " groups of " + str(len(grouped[0])) + " students: "
    for group in range(len(grouped)):
        for student in range(len(grouped[group])):
            if (student < len(grouped[0])-1):
                msg += get_name(grouped[group][student]) + " + "
            else:
                msg += get_name(grouped[group][student])
        msg += ", "

    send_message("CBTUY2DUY", msg)

    channels = {} # dict of channel ids: [memberids]
    counter = random.randint(0,1000)
    for group in grouped:
        channel_id = create_channel("team_"+str(counter))
        new_channel = []
        for student in group:
            add_to_channel(student, channel_id)
            new_channel.append(student)
        counter += 1
        send_message(channel_id, "Your new team consists of " + ", ".join([get_name(x) for x in group])+"!")
        send_message(channel_id, "✨ Rename this channel with a new team name ✨ \n "
                                 "_Can't think of one?_ How about `"+generate_team_name()+"`?")
        channels["channel_id"] = new_channel


def form_group(size):
    channel = "CBVSC5QDC"
    PARAMS = {'token': slack_token, 'channel': channel}
    info_result = requests.get(url=info, params=PARAMS)
    data = info_result.json()
    members = data['channel']['members']
    grouping(members, size)


size = 3
###for forming groups
form_group(size)









