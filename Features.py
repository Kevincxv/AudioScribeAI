import os
import threading
import warnings

import numpy as np
import requests
import sounddevice as sd
import soundfile as sf
import tkinter as tk
import whisper
from flask import Flask, jsonify, request
from flask_cors import CORS
from langdetect import detect

app = Flask(__name__)
CORS(app)

# API_KEY = os.environ.get('OPENAI_API_KEY')
# if not API_KEY:
#     raise ValueError("Please set the OPENAI_API_KEY environment variable.")

API_KEY ='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'

recording = []
samplerate = 44100
stream = None
transcription = ""
summary = ""
translation = ""
extracted_reminders = ""

warnings.filterwarnings("ignore", category=UserWarning)

supported_languages = {"French": "French:", "Spanish": "Spanish:", "German": "German:", "Italian": "Italian:", "Portuguese": "Portuguese:", "Dutch": "Dutch:", "Russian": "Russian:", "Japanese": "Japanese:", "Chinese": "Chinese:", "Korean": "Korean:", "Arabic": "Arabic:", "Hindi": "Hindi:", "Swedish": "Swedish:", "Danish": "Danish:", "Finnish": "Finnish:", "Norwegian": "Norwegian:", "Polish": "Polish:", "Turkish": "Turkish:", "Greek": "Greek:", "Hebrew": "Hebrew:"}

def detect_language(text):
    try:
        detected_language = detect(text)
        return detected_language
    except:
        print("Error detecting language. Defaulting to English.")
        return "en"

def request_to_openai(url, data, role_system, content_user):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python Client'
    }
    data["model"] = "gpt-3.5-turbo"
    data["messages"] = [
        {"role": "system", "content": role_system},
        {"role": "user", "content": content_user}
    ]
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        api_response_content = response.json()['choices'][0]['message']['content']
        print(f"API Response: {api_response_content}")  # Debug log
        return api_response_content
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def callback(indata, _, __, ___):
    recording.append(indata.copy())

def start_recording():
    global stream
    recording.clear()
    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype=np.int16, callback=callback)
    stream.start()

def stop_recording():
    global stream
    stream.stop()
    stream.close()
    np.save("recording.npy", np.concatenate(recording, axis=0))

def playback():
    if not recording:
        return "No recording data available."
    sd.play(np.concatenate(recording, axis=0), samplerate)

def transcribe():
    global transcription
    if not recording:
        return "No recording data available."

    filename = "recording.wav"
    sf.write(filename, np.concatenate(recording, axis=0), samplerate)
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    raw_transcription = result["text"]
    
    sentences = [s.strip() for s in raw_transcription.split('.') if s]
    labeled_transcription = [f"{'Agent' if i % 2 == 0 else 'Customer'}: {sentence}." for i, sentence in enumerate(sentences)]
    transcription = "\n".join(labeled_transcription)

def summarize():
    global summary
    sanitized_transcription = transcription.replace("\n", " ").strip()[:1000]
    content = f'Provide a bullet-point summary for the following customer service call: {sanitized_transcription}'
    role_system = "You are a helpful assistant that provides summaries for customer service calls."
    summary = request_to_openai('https://api.openai.com/v1/chat/completions', {}, role_system, content)


def reminders():
    global extracted_reminders, lines
    content = f'From the following conversation, identify and format the information about any appointments, reminders, or meetings. Text: {transcription}'
    role_system = "You are a helpful assistant that extracts and formats information about reminders, meetings, and appointments from conversations."
    extracted_info = request_to_openai('https://api.openai.com/v1/chat/completions', {}, role_system, content)
    lines = extracted_info.split("\n")
    extracted_reminders = "\n".join([line for line in lines if line.startswith(("Meeting:", "Reminder:", "Appointment Date:", "Appointment Time:", "Timezone:"))])
        
def translate():
    global translation
    detected_lang = detect_language(transcription)
    
    if detected_lang not in supported_languages:
        print(f"Detected language {detected_lang} is not supported for translation.")
        return
    content = f"Translate the following text from {detected_lang} to English: {transcription}"
    role_system = "You are a helpful assistant that translates text."
    translation = request_to_openai('https://api.openai.com/v1/chat/completions', {}, role_system, content)

@app.route('/start_recording', methods=['POST'])
def start_recording_route():
    start_recording()
    return jsonify({"message": "Recording started"}), 200

@app.route('/stop_recording', methods=['POST'])
def stop_recording_route():
    stop_recording()
    transcribe()
    return jsonify({"message": "Recording stopped"}), 200

@app.route('/play_audio', methods=['GET'])
def play_audio_route():
    response = playback()
    if response:
        return jsonify({"error": response}), 400
    return jsonify({"audio": "Audio is playing..."}), 200

@app.route('/display_transcript', methods=['GET'])
def display_transcript_route():
    response = transcribe()
    if response:
        return jsonify({"error": response}), 400
    return jsonify({"transcript": transcription}), 200

@app.route('/display_summary', methods=['GET'])
def display_summary_route():
    summarize()
    return jsonify({"summary": summary}), 200

@app.route('/display_reminders', methods=['GET'])
def display_reminders_route():
    reminders()
    return jsonify({"reminders": lines}), 200

@app.route('/translate', methods=['GET'])
def translate_route():
    translate()
    return jsonify({"translation": translation}), 200

if __name__ == '__main__':
    app.run(debug=True)
