import json
import random

# dev utils
from utils.devUtils import readThis

# get recent messages
def get_recent_messages ():
    file_name = "store_data.json"
    learn_instruction = {
        "role": "system",
        "content": "Your Are a Science and assistant who is every enthusiastic, Curious for Solutions to Solving client change. Finding new sources of Green and renewable energy environmental friendly and beneficial to the environment. Ask relevant question patterning the Environment. Your Name is Mira. The user is Bright. keep your answers to under 100 words",
    }
    messages = []

    # add a random element
    x = random.uniform (0, 1)
    if (x < 0.5):
        learn_instruction['content'] = learn_instruction['content'] + " Your Response will include some dry humour."
    else:
        learn_instruction['content'] = learn_instruction['content'] + " Your Response will include rather challenging and intriguing reasoning"

    # append instruction to message
    messages.append (learn_instruction)

    # get last messages
    try:
        with open (file_name) as user_file:
            data = json.load (user_file)

            # append the last five
            if data: 
                if len (data) < 5:
                    for item in data:
                        messages.append (item)
                else:
                    for item in data[-5:]: 
                        messages.append (item)
    except Exception as e:
        readThis (e)

    return messages


# store messages
def store_messages (request_message, response_message): 
    file_name = "store_data.json"

    messages = get_recent_messages ()[1:]

    # add messages to data
    user_message = {
        "role": "user",
        "content": request_message
    }
    assistant_message = {
        "role": "assistant",
        "content": request_message
    }

    messages.append (user_message)
    messages.append (assistant_message)

    # save data
    with open (file_name, 'w') as file:
        json.dump (messages, file)

def reset_messages ():
    open ("store_data.json", 'w')