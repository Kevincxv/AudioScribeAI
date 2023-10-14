import tkinter as tk
import sounddevice as sd
import numpy as np
import requests
import soundfile as sf
import whisper
import warnings

API_KEY = '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'

recording = None
samplerate = 44100
transcription = ""
recording = []
stream = None
warnings.filterwarnings("ignore", category=UserWarning)

def callback(indata, frames, time, status):
    global recording
    recording.append(indata.copy())

def on_start_recording():
    global stream
    recording.clear()
    stream = sd.InputStream(samplerate=samplerate, channels=1, dtype=np.int16, callback=callback)
    stream.start()

def on_stop_recording():
    global stream, recording
    stream.stop()
    stream.close()
    recording = np.concatenate(recording, axis=0)
    np.save("recording.npy", recording)

def on_playback():
    global recording
    sd.play(recording, samplerate=samplerate)

def on_transcribe():
    global recording
    
    filename = "recording.wav"
    sf.write(filename, recording, samplerate)
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    print(result["text"])
    
    print(transcription)


def on_summarize():
    global transcription
    
    endpoint = "https://api.openai.com/v1/engines/davinci/completions"

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python Client'
    }

    data = {
        'prompt': f"Summarize the following customer service call: {transcription}",
        'max_tokens': 150
    }

    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        summary = response.json()["choices"][0]["text"].strip()
        print("Summary:", summary)
    else:
        print("Error:", response.status_code, response.text)


def on_extract_reminders():
    global transcription
    
    # Check if transcription exists
    if not transcription:
        print("Please transcribe the audio first.")
        return
    
    headers = {
        'Authorization': 'Bearer ' + API_KEY,
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python Client'
    }
    
    data = {
        'prompt': 'Extract reminders, meetings, and appointment dates from the following text: ' + transcription,
        'max_tokens': 200
    }
    
    response = requests.post('https://api.openai.com/v1/engines/davinci/completions', headers=headers, json=data)
    
    if response.status_code == 200:
        extracted_info = response.json()["choices"][0]["text"].strip()
        print("Extracted Information:", extracted_info)
    else:
        print("Error:", response.status_code, response.text)


root = tk.Tk()
root.title("Customer Service Helper")

start_btn = tk.Button(root, text="Start Recording", command=on_start_recording)
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop Recording", command=on_stop_recording)
stop_btn.pack(pady=10)

playback_btn = tk.Button(root, text="Playback", command=on_playback)
playback_btn.pack(pady=10)

transcribe_btn = tk.Button(root, text="Transcribe", command=on_transcribe)
transcribe_btn.pack(pady=10)

summarize_btn = tk.Button(root, text="Summarize", command=on_summarize)
summarize_btn.pack(pady=10)

reminders_btn = tk.Button(root, text="Extract Reminders", command=on_extract_reminders)
reminders_btn.pack(pady=10)

root.mainloop()
