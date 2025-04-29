from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import asyncio
import wave
import io
load_dotenv()
import os
from google import genai

from google.genai import types
from google.genai.types import (
    LiveConnectConfig,
    PrebuiltVoiceConfig,
    SpeechConfig,
    VoiceConfig,
)
from conversationClass import *

GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

# credential_path = '/Users/longn/CodeStuffs/podcast-generator/server/podcast-generator-458000-68a07928e1ab.json'
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
client = genai.Client(api_key=GEMINI_API_KEY)
model = "gemini-2.0-flash-live-001"

voice_name = "Aoede"  # @param ["Aoede", "Puck", "Charon", "Kore", "Fenrir", "Leda", "Orus", "Zephyr"]

PROJECT_ID = str(os.environ.get("GOOGLE_CLOUD_PROJECT"))
LOCATION = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
# client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

config1 = LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=SpeechConfig(
        voice_config=VoiceConfig(
            prebuilt_voice_config=PrebuiltVoiceConfig(
                voice_name=voice_name,
            )
        ),
    )
)


config2 = LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=SpeechConfig(
        voice_config=VoiceConfig(
            prebuilt_voice_config=PrebuiltVoiceConfig(
                voice_name="Charon",
            )
        ),
    )
)
# config = {"response_modalities": ["AUDIO"]}

# response = client.models.generate_content(
#     model='gemini-2.0-flash-001', contents='Why is the sky blue?'
# )
# print(response.text)

# with open('test.mp3','w') as f:
    # audio_bytes = f.read()


# for chunk in client.models.generate_content_stream(
#     model='gemini-2.0-flash-001', contents=

#     'Tell me a story in 300 words.'
# ):
#     full_audio_data = b''.join(chunk) # Use io.BytesIO to treat the stream as a file audio_io = io.BytesIO(full_audio_data) 
    
#     # print(chunk.text, end='')

# audio_io = io.BytesIO(full_audio_data)
# app = Flask(__name__)


# # Use pydub to open the audio stream (assuming it's a raw audio stream) 
# audio = pydub.AudioSegment.from_file(audio_io, format="raw") # Adjust format if needed # Export as MP3 
# output_filename = "generated_audio.mp3" 
# audio.export(output_filename, format="mp3") 

# CORS(app)

# @app.route("/api/home", methods=(['Get']))
# def return_home():
#     return jsonify({
#         "message": "He"
#     })


# @app.route("/api/submit", methods=(['POST']))
# def fetch_podcast():
#     return jsonify({
#         "message": "He"
#     })


# async def responseToAudio(session, responseData = None): 
#     async with client.aio.live.connect(model=model, config=config1) as session:
#         # await sessionHandler()

#         # wf = wave.open("audio.wav", "wb")
#         # wf.setnchannels(1)
#         # wf.setsampwidth(2)
#         # wf.setframerate(24000)
#         await session.send_client_content(
#             turns={"role": "user", "parts": [{"text": message}]}, turn_complete=True
#         )

#         async for response in session.receive():
#             if response.data is not None:
#                 # print(response.data)
#                 return response.data
#                 # wf.writeframes(response.data)

#             # Un-comment this code to print audio data info
#             # if response.server_content.model_turn is not None:
#             #     print(response.server_content.output_transcription.text)
#                 # exit()

#         # return None
#         # wf.close()

# async def conversationStarter(message):
#     conversationFlow = []
#     async with client.aio.live.connect(model=model, config=config1) as session:
#         # wf = wave.open("audio.wav", "wb")
#         # wf.setnchannels(1)
#         # wf.setsampwidth(2)
#         # wf.setframerate(24000)

#         message = "Hello? Gemini are you there?"
#         await session.send_client_content(
#             turns={"role": "user", "parts": [{"text": message}]}, turn_complete=True
#         )

#         async for response in session.receive():
#             if response.data is not None:
#                 # print(response.data)
#                 return response.data
#                 # wf.writeframes(response.data)

#             # Un-comment this code to print audio data info
#             # if response.server_content.model_turn is not None:
#             #     print(response.server_content.output_transcription.text)
#                 # exit()

#         # return None
#         # wf.close()


def podcastContent(topic1, time): 
    response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Write a podcast based on this topic " + topic1 + " with two hosts with duration of " + str(time)
    + " in minutes. Label them so we can use later for voice models")
    print(response.text)
    return response.text

async def conversation(podcastScript, configSetting, file):
    async with client.aio.live.connect(model=model, config=configSetting) as session:
        wf = wave.open(file, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)


        if configSetting == config1: 
            hostOrder = "First host"
        else: 
            hostOrder = "Second host"

        await session.send_client_content(
            turns={"role": "user", "parts": [{"text": "(don't ask back question) Read this podcast script: " + str(podcastScript) + " and be the " + hostOrder}]}, turn_complete=False
        )

        async for response in session.receive():
            if response.data is not None:
                # print(response.data)
                # return response.data
                wf.writeframes(response.data)

            # Un-comment this code to print audio data info
            # if response.server_content.model_turn is not None:
            #     print(response.server_content.output_transcription.text)
                # exit()

        # return None
        wf.close()

# async def conversation2(configSetting, file):
#     with open('/Users/longn/CodeStuffs/podcast-generator/server/audio.wav', 'rb') as f:
#         audio_bytes = f.read()


#     response = client.models.generate_content(
#     model='gemini-2.0-flash',
#     contents=[
#         'Transcript this audio (print only content)',
#             types.Part.from_bytes(data=audio_bytes,mime_type='audio/wav')
#         ]
#     )
#     print(response.text)
#     # response.text

#     return await conversation(response.text, configSetting, file)


async def main():
    podcastScript = podcastContent("Jazz", 5)
    responseData1 = await conversation(podcastScript, config1, 'audio.wav')
    # print(responseData1)
    responseData2 = await conversation(podcastScript, config2, 'response.wav')
    # startConversation = 
    # for i in range(2): 
    #     responseData = await conversation()
    #     conversationFlow.append(responseData)

    # wf = wave.open("audio.wav", "wb")
    # wf.setnchannels(1)
    # wf.setsampwidth(2)
    # wf.setframerate(24000)

    # for x in conversationFlow:
    #     wf.writeframes(x)

    # wf.close()



    # async with client.aio.live.connect(model=model, config=config) as session:
    #     wf = wave.open("audio.wav", "wb")
    #     wf.setnchannels(1)
    #     wf.setsampwidth(2)
    #     wf.setframerate(24000)

    #     message = "Hello? Gemini are you there?"
    #     await session.send_client_content(
    #         turns={"role": "user", "parts": [{"text": message}]}, turn_complete=True
    #     )

    #     async for response in session.receive():
    #         if response.data is not None:
    #             wf.writeframes(response.data)

    #         # Un-comment this code to print audio data info
    #         # if response.server_content.model_turn is not None:
    #         #      print(response.server_content.model_turn.parts[0].inline_data.mime_type)

    #     wf.close()

if __name__ == "__main__":
    asyncio.run(main())

# return "Audio saved successfully!", 200 except Exception as e: return str(e), 500 if __name__ == '__main__': app.run(debug=True)

# if __name__ == "__main__": 
#     app.run(debug=True, port=8080)
    