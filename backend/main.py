from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

# dev imports Utils
from utils.devUtils import readThis

# functions imports
from functions.openai_requests import convert_audio_to_text, get_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import text_to_speech

# initializing App
app = FastAPI ()

# CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4174",
    "http://localhost:4174",
    "http://localhost:3000",
]

# CORS - Middleware
app.add_middleware (
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.get ("/health")
async def check_health ():
    return {"msg": "healthy"}

# get_audio
@app.post ("/post-audio")
async def post_audio (file: UploadFile = File(...)):
    # get saved audio
    # audio_input = open ("voiceover.mp3", "rb")

    # save file from front end
    with open (file.filename, 'wb') as buffer:
        buffer.write (file.file.read ())
    audio_input = open (file.filename, 'rb')

    msg_decoded = convert_audio_to_text (audio_input)
    # readThis (msg_decoded)

    # guard insure that the message decoded

    if not msg_decoded:
        return HTTPException (status_code=400, detail="Failed to decode Audio")
    
    chat_response = get_response (msg_decoded)

    if not chat_response:
        return HTTPException (status_code=400, detail="Failed to get Chat response")
    
    # readThis (chat_response)
    store_messages (msg_decoded, chat_response)

    # convert chat response to audio
    audio_output = text_to_speech (chat_response) 

    if not audio_output:
        readThis (audio_output)
        return HTTPException (status_code=400, detail="Failed to get Eleven Labs Audio")
    

    # yield chunks of data
    def iterfile (): 
        yield audio_output

    return StreamingResponse (iterfile (), media_type="application/octet-stream")


@app.get ("/reset-chats")
def reset_chats ():
    reset_messages ()
    return {"message": "reset of Conversation was successful"}
