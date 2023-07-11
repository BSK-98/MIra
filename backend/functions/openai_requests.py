import openai

from decouple import config

# dev utils
from utils.devUtils import readThis

# retrieve Environment Variables
openai.organization = config ("OPENAI_ORG_KEY")
openai.api_key = config ("OPENAI_API_KEY")

# database imports
from .database import get_recent_messages


# convert Audio To text
# open AI - Whisper
def convert_audio_to_text (audio_file):
    try:
        transcript = openai.Audio.transcribe ("whisper-1", audio_file)
        msg = transcript['text']
        return msg
    except Exception as e:
        readThis (e)
        return

# openAI Chart GPT
def get_response (message_input):
    recent_messages = get_recent_messages ()
    user_msg = {
        "role": "user",
        "content": message_input
    }
    
    recent_messages.append (user_msg)

    # readThis (recent_messages)

    try:
        response = openai.ChatCompletion.create (
            model = "gpt-3.5-turbo",
            messages = recent_messages
        )
        # readThis (response)
        message_text = response['choices'][0]['message']['content']
        return message_text
    except Exception as e:
        readThis (e)
        return