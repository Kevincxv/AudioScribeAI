import tkinter as tk
import sounddevice as sd
import numpy as np
import requests
import soundfile as sf
import whisper
import warnings
import os
from langdetect import detect

API_KEY = os.environ.get('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

recording = None
samplerate = 44100
transcription = ""
summary = ""
translation = ""
extracted_reminders = ""
recording = []
stream = None
warnings.filterwarnings("ignore", category=UserWarning)

supported_languages = {"French": "French:", "Spanish": "Spanish:", "German": "German:", "Italian": "Italian:", "Portuguese": "Portuguese:", "Dutch": "Dutch:", "Russian": "Russian:", "Japanese": "Japanese:", "Chinese": "Chinese:", "Korean": "Korean:", "Arabic": "Arabic:", "Hindi": "Hindi:", "Swedish": "Swedish:", "Danish": "Danish:", "Finnish": "Finnish:", "Norwegian": "Norwegian:", "Polish": "Polish:", "Turkish": "Turkish:", "Greek": "Greek:", "Hebrew": "Hebrew:"}

def detect_language(text):
    try:
        detected_language = detect(text)
        return detected_language
    except:
        print("Error detecting language. Defaulting to English.")
        return "en"

def callback(indata, outdata, frames, timeinfo):
    global recording
    recording.append(indata.copy())

def start_recording():
    global stream
    try:
        recording.clear()
        stream = sd.InputStream(samplerate=samplerate, channels=1, dtype=np.int16, callback=callback)
        stream.start()
    except Exception as e:
        print(f"Error starting recording: {e}")

def stop_recording():
    global stream, recording
    try:
        stream.stop()
        stream.close()
        recording = np.concatenate(recording, axis=0)
        np.save("recording.npy", recording)
    except Exception as e:
        print(f"Error stopping recording: {e}")

def playback():
    global recording
    adjusted_samplerate = samplerate * playback_speed.get()
    try:
        sd.play(recording, samplerate=adjusted_samplerate)
    except Exception as e:
        print(f"Error during playback: {e}")


def save_recording():
    global recording
    filename = "saved_recording.wav"
    sf.write(filename, recording, samplerate)
    print("Recording saved successfully!")

def transcribe():
    global transcription, recording
    filename = "recording.wav"
    sf.write(filename, recording, samplerate)
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    raw_transcription = result["text"]

    # Split transcription into sentences
    sentences = [s.strip() for s in raw_transcription.split('.') if s]
    
    labeled_transcription = []
    role = "Agent"
    
    for sentence in sentences:
        labeled_transcription.append(f"{role}: {sentence}.")
        role = "Customer" if role == "Agent" else "Agent"
        
    transcription = "\n".join(labeled_transcription)
    print(transcription)

def request_to_openai(url, data):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python Client'
    }
    data["model"] = "gpt-3.5-turbo"
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def summarize():
    global transcription, summary
    if not transcription:
        print("Please transcribe the audio first.")
        return

    sanitized_transcription = transcription.replace("\n", " ").strip()[:1000]
    content = f'Provide a bullet-point summary for the following customer service call: {sanitized_transcription}'

    data = {
        'messages': [
            {"role": "system", "content": "You are a helpful assistant that provides summaries for customer service calls."},
            {"role": "user", "content": content}
        ],
        'max_tokens': 150
    }

    summary = request_to_openai('https://api.openai.com/v1/chat/completions', data)
    
    if summary:
        print("Summary:", summary)
    else:
        print("There's no summary for the transcription.")

def reminders():
    global transcription
    if not transcription:
        print("Please transcribe the audio first.")
        return
    
    content = f'Extract reminders, meetings, and appointment dates from the following text in the format of "Meeting: DAY TIME, Reminder: TIMEFRAME, Schedule: DATE": {transcription}'
    
    data = {
        'messages': [
            {"role": "system", "content": "You are a helpful assistant that extracts reminders, meetings, and appointments."},
            {"role": "user", "content": content}
        ],
        'max_tokens': 200
    }
    
    extracted_info = request_to_openai('https://api.openai.com/v1/chat/completions', data)
    
    if extracted_info:
        lines = extracted_info.split("\n")
        formatted_info = [line for line in lines if line.startswith(("Meeting:", "Reminder:", "Schedule:"))]
        extracted_reminders = "\n".join(formatted_info)
        if extracted_reminders:
            print(extracted_reminders)
        else:
            print("There's no reminder in the transcription.")
    else:
        print("Failed to extract information from OpenAI API.")
        
def translate():
    global transcription, translation
    if not transcription:
        print("Please transcribe the audio first.")
        return
    
    detected_language = detect_language(transcription)
    
    language_map = {"fr": "French", "es": "Spanish", "de": "German", "it": "Italian", "pt": "Portuguese", "nl": "Dutch", "ru": "Russian", "ja": "Japanese", "zh-cn": "Chinese", "ko": "Korean", "ar": "Arabic", "hi": "Hindi", "sv": "Swedish", "da": "Danish", "fi": "Finnish", "no": "Norwegian", "pl": "Polish", "tr": "Turkish", "el": "Greek", "he": "Hebrew", "en": "English"}

    if detected_language in language_map:
        language_var.set(language_map[detected_language])
    else:
        print(f"Detected language ({detected_language}) is not supported. Please select a translation target manually.")
        return
    
    prompt_language = supported_languages.get(language_var.get())
    
    if prompt_language:
        content = f'{prompt_language} {transcription}'
        data = {
            'messages': [
                {"role": "system", "content": "You are a helpful assistant that translates text."},
                {"role": "user", "content": content}
            ],
            'max_tokens': 500  
        }
        translation = request_to_openai('https://api.openai.com/v1/chat/completions', data)
        if translation:
            print(translation)
        else:
            print("There's no translation for the transcription.")
    else:
        print(f"{language_var.get()} is not supported or not selected.")


def load_recording():
    global recording
    filename = "recording.wav"
    if os.path.exists(filename):
        recording, _ = sf.read(filename, dtype=np.int16)
        print("Recording loaded.")
    else:
        print("No recording file found. Please record first.")
        
def save_to_file(content, file_type):
    with open(f"{file_type}.txt", "w") as file:
        file.write(content)
    print(f"{file_type} saved successfully!")

root = tk.Tk()
root.title("Customer Service Helper")

start_btn = tk.Button(root, text="Start Recording", command=start_recording)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_btn.pack(pady=10)

playback_btn = tk.Button(root, text="Playback", command=playback)
playback_btn.pack(pady=10)

playback_speed = tk.DoubleVar(root)
playback_speed.set(1.0)
playback_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Playback Speed", variable=playback_speed)
playback_scale.pack(pady=10)

transcribe_btn = tk.Button(root, text="Transcribe", command=transcribe)
transcribe_btn.pack(pady=10)

summarize_btn = tk.Button(root, text="Summarize", command=summarize)
summarize_btn.pack(pady=10)

reminders_btn = tk.Button(root, text="Reminders", command=reminders)
reminders_btn.pack(pady=10)

save_transcription_btn = tk.Button(root, text="Save Transcription", command=lambda: save_to_file(transcription, "transcription"))
save_transcription_btn.pack(pady=10)

save_summary_btn = tk.Button(root, text="Save Summary", command=lambda: save_to_file(summary, "summary"))
save_summary_btn.pack(pady=10)

save_translation_btn = tk.Button(root, text="Save Translation", command=lambda: save_to_file(translation, "translation"))
save_translation_btn.pack(pady=10)

save_reminders_btn = tk.Button(root, text="Save Reminders", command=lambda: save_to_file(extracted_reminders, "reminders"))
save_reminders_btn.pack(pady=10)

save_playback_btn = tk.Button(root, text="Save Playback", command=save_recording)
save_playback_btn.pack(pady=10)

language_var = tk.StringVar(root)
language_var.set("Select Language")

lang_dropdown = tk.OptionMenu(root, language_var, *supported_languages.keys())
lang_dropdown.pack(pady=10)

translate_btn = tk.Button(root, text="Translate", command=translate)
translate_btn.pack(pady=10)

load_btn = tk.Button(root, text="Load Recording", command=load_recording)
load_btn.pack(pady=10)

root.mainloop()
