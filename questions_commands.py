import os
from slackclient import SlackClient
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')
slack_token = config['TEST']['TOKEN']

DAY_SECONDS = 24 * 60 * 60
sc = SlackClient(slack_token)

last_get_ts = ""

def get_top_questions(amount):
    # read messages for a thread
    # create question objects
    # return top amount
    channel_id = "CBUMNC8HG"

    # gets the question thread
    conversation_history = sc.api_call(
                                "conversations.history",
                                channel=channel_id,
                                inclusive="true",
                                latest=str(time.time()),
                                oldest=str(time.time() - DAY_SECONDS))

    # finds the question thread id
    messages = conversation_history["messages"]
    for msg in messages:
        if (msg["user"] == bot_id):
            thread_indicator = msg["ts"]
            break

    # gets all questions asked since last get
    latest_time = str(time.time())
    thread = sc.api_call(
                    "conversations.replies",
                    channel=channel_id,
                    ts=thread_indicator,
                    inclusive="true",
                    latest=latest_time,
                    oldest=last_get_ts)
    last_get_ts = latest_time

    # sorts all questions and gets top n questions based on reactions
    replies = thread[1:]
    question_processor = QuestionProcessor()
    for reply in replies:
        question_processor.add_question(reply)
    question_processor.sort_questions()
    return question_processor.top(amount)

