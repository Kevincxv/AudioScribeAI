import os
import warnings
import numpy as np
import requests
import sounddevice as sd
import soundfile as sf
import whisper
from flask import Flask, jsonify, request
from flask_cors import CORS
from langdetect import detect
from dotenv import load_dotenv
import nltk
from nltk.tokenize import sent_tokenize


load_dotenv()
nltk.download('punkt')
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv('API_KEY')
API_URL = 'https://api.openai.com/v1/chat/completions'

recording = []
samplerate = 44100
stream = None
transcription = ""
summary = ""
translation = ""
extracted_reminders = ""

supported_languages = {"French": "French:", "Spanish": "Spanish:", "German": "German:", "Italian": "Italian:", "Portuguese": "Portuguese:", "Dutch": "Dutch:", "Russian": "Russian:", "Japanese": "Japanese:", "Chinese": "Chinese:", "Korean": "Korean:", "Arabic": "Arabic:", "Hindi": "Hindi:", "Swedish": "Swedish:", "Danish": "Danish:", "Finnish": "Finnish:", "Norwegian": "Norwegian:", "Polish": "Polish:", "Turkish": "Turkish:", "Greek": "Greek:", "Hebrew": "Hebrew:"}

def detect_language(text):
    try:
        detected_language = detect(text)
        return detected_language
    except:
        print("Error detecting language. Defaulting to English.")
        return "en"

def openai_request(role_system, content_user):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python Client'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": role_system},
            {"role": "user", "content": content_user}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
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
    filename = "latest_recording.wav"
    sf.write(filename, np.concatenate(recording, axis=0), samplerate)

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
    
    sentences = sent_tokenize(raw_transcription)
    
    labeled_transcription = [f"{'Agent' if i % 2 == 0 else 'Customer'}: {sentence}" for i, sentence in enumerate(sentences)]
    
    transcription = "\n".join(labeled_transcription)


def summarize():
    global summary
    sanitized_transcription = transcription.replace("\n", " ").strip()[:1000]
    content = f'Provide a bullet-point summary for the following customer service call: {sanitized_transcription}'
    role_system = "You are a helpful assistant that provides summaries for customer service calls."
    summary = openai_request(role_system, content)


def reminders():
    global extracted_reminders, lines
    content = f'From the following conversation, identify and format the information about any appointments, reminders, or meetings. Text: {transcription}'
    role_system = "You are a helpful assistant that extracts and formats information about reminders, meetings, and appointments from conversations."
    extracted_info = openai_request(role_system, content)
    lines = extracted_info.split("\n")
    extracted_reminders = "\n".join(list(set([line for line in lines if line.startswith(("Meeting:", "Reminder:", "Appointment Date:", "Appointment Time:", "Timezone:"))])))
    
def load_latest_recording():
    global recording
    try:
        data, _ = sf.read("latest_recording.wav", dtype=np.int16)
        recording = [data]
    except Exception as e:
        print(f"Error loading latest recording: {e}")
        return "No saved recording found."
        
def translate(target_language):
    global translation
    detected_lang = detect_language(transcription)
    
    if detected_lang == "en" and target_language == "English":
        print("Source and target language is English. No translation needed.")
        translation = "The provided text is already in English."
        return
    
    if target_language not in supported_languages:
        print(f"Target language {target_language} is not supported for translation.")
        translation = f"Translation to {target_language} is not supported."
        return
    
    if detected_lang == "en":
        content = f"Translate the following text from English to {target_language}: {transcription}"
    else:
        content = f"Translate the following text from {detected_lang} to English: {transcription}"
        transcription_in_english = openai_request("You are a helpful assistant that translates text.", content)
        content = f"Translate the following text from English to {target_language}: {transcription_in_english}"
    
    role_system = "You are a helpful assistant that translates text."
    raw_translation = openai_request(role_system, content)
    
    sentences = sent_tokenize(raw_translation)
    labeled_translation = [f"{'Agent' if i % 2 == 0 else 'Customer'}: {sentence}" for i, sentence in enumerate(sentences)]
    translation = "\n".join(labeled_translation)



@app.route('/start_recording', methods=['POST'])
def start_recording_route():
    if os.path.exists("latest_recording.wav"):
        return jsonify({"message": "A recording already exists. Use /load_latest_recording to load it or /stop_recording to overwrite it."}), 200
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
    formatted_transcription = {
        "title": "Transcription",
        "content": transcription.split('\n')
    }
    return jsonify(formatted_transcription), 200

@app.route('/display_summary', methods=['GET'])
def display_summary_route():
    summarize()
    formatted_summary = {
        "title": "Summary",
        "content": summary.split('\n')
    }
    return jsonify(formatted_summary), 200

@app.route('/display_reminders', methods=['GET'])
def display_reminders_route():
    reminders()
    return jsonify({"reminders": lines}), 200

@app.route('/translate/<target_language>', methods=['GET'])
def translate_route(target_language):
    translate(target_language)
    formatted_translation = {
        "title": "Translation",
        "content": translation.split('\n')
    }
    return jsonify(formatted_translation), 200



@app.route('/load_latest_recording', methods=['GET'])
def load_latest_recording_route():
    response = load_latest_recording()
    if response:
        return jsonify({"error": response}), 400
    return jsonify({"message": "Latest recording loaded"}), 200


if __name__ == '__main__':
    app.run(debug=True)
