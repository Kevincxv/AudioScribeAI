import tkinter as tk
import sounddevice as sd
import numpy as np
import requests
import soundfile as sf
import whisper
import warnings
import os

API_KEY = os.environ.get('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

recording = None
samplerate = 44100
transcription = ""
recording = []
stream = None
warnings.filterwarnings("ignore", category=UserWarning)

def callback(indata, frames, time, status):
    global recording
    recording.append(indata.copy())

def start_recording():
    global stream
    recording.clear()
    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype=np.int16, callback=callback)
    stream.start()

def stop_recording():
    global stream, recording
    stream.stop()
    stream.close()
    recording = np.concatenate(recording, axis=0)
    np.save("recording.npy", recording)

def playback():
    global recording
    sd.play(recording, samplerate=samplerate)

def transcribe():
    global transcription, recording
    filename = "recording.wav"
    sf.write(filename, recording, samplerate)
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    transcription = result["text"]
    print(transcription)

def request_to_openai(endpoint, data):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python Client'
    }
    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except requests.RequestException as e:
        print("API Error:", e)

def summarize():
    global transcription
    if not transcription:
        print("Please transcribe the audio first.")
        return

    sanitized_transcription = transcription.replace("\n", " ").strip()[:1000]

    prompt = f"Summarize the following customer service call: {sanitized_transcription}"
    data = {'prompt': prompt, 'max_tokens': 150}
    summary = request_to_openai('https://api.openai.com/v1/engines/davinci/completions', data)
    
    if summary:
        print("Summary:", summary)


def extract_reminders():
    global transcription
    if not transcription:
        print("Please transcribe the audio first.")
        return
    
    prompt = f'Extract reminders, meetings, and appointment dates from the following text: {transcription}'
    data = {'prompt': prompt, 'max_tokens': 200}
    extracted_info = request_to_openai('https://api.openai.com/v1/engines/davinci/completions', data)
    if extracted_info:
        print("Extracted Information:", extracted_info)


root = tk.Tk()
root.title("Customer Service Helper")

start_btn = tk.Button(root, text="Start Recording", command=start_recording)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop Recording", command=stop_recording)
stop_btn.pack(pady=10)

playback_btn = tk.Button(root, text="Playback", command=playback)
playback_btn.pack(pady=10)

transcribe_btn = tk.Button(root, text="Transcribe", command=transcribe)
transcribe_btn.pack(pady=10)

summarize_btn = tk.Button(root, text="Summarize", command=summarize)
summarize_btn.pack(pady=10)

reminders_btn = tk.Button(root, text="Extract Reminders", command=extract_reminders)
reminders_btn.pack(pady=10)

root.mainloop()
