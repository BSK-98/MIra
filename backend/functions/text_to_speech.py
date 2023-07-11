import requests

from decouple import config

# dev utils 
from utils.devUtils import readThis

ELEVEN_LABS = config ("ELEVEN_LABS")

# convert text to speech
def text_to_speech (message):
    # print (message)
    body = {
        "text": message,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0.5,
            "use_speaker_boost": False
        }
    }

    voice_id = "21m00Tcm4TlvDq8ikWAM"
    headers = {
        "xi-api-key": ELEVEN_LABS,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }

    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    try:
        response = requests.post (endpoint, json=body, headers=headers)
        # readThis ({"response Main": response.content})
    except Exception as e:
        readThis ({"response": e})
        return
    
    if response.status_code == 200:
        return response.content
    else:
        return