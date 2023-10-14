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

supported_languages = {"French": "French:", "Spanish": "Spanish:", "German": "German:", "Italian": "Italian:", "Portuguese": "Portuguese:", "Dutch": "Dutch:", "Russian": "Russian:", "Japanese": "Japanese:", "Chinese": "Chinese:", "Korean": "Korean:", "Arabic": "Arabic:", "Hindi": "Hindi:", "Swedish": "Swedish:", "Danish": "Danish:", "Finnish": "Finnish:", "Norwegian": "Norwegian:", "Polish": "Polish:", "Turkish": "Turkish:", "Greek": "Greek:", "Hebrew": "Hebrew:"}

def callback(indata):
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

def request_to_openai(url, data):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'User-Agent': 'OpenAI Python Client'
    }
    data["model"] = "gpt-3.5-turbo"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.json()['error']['message']}")
        return None
    return response.json()['choices'][0]['message']['content']

def summarize():
    global transcription
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
        if formatted_info:
            print("\n".join(formatted_info))
    else:
        print("Failed to extract information from OpenAI API.")
        
def translate():
    global transcription
    if not transcription:
        print("Please transcribe the audio first.")
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
            print("Failed to translate using OpenAI API.")
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


# root = tk.Tk()
# root.title("Customer Service Helper")

# start_btn = tk.Button(root, text="Start Recording", command=start_recording)
# start_btn.pack(pady=10)

# stop_btn = tk.Button(root, text="Stop Recording", command=stop_recording)
# stop_btn.pack(pady=10)

# playback_btn = tk.Button(root, text="Playback", command=playback)
# playback_btn.pack(pady=10)

# transcribe_btn = tk.Button(root, text="Transcribe", command=transcribe)
# transcribe_btn.pack(pady=10)

# summarize_btn = tk.Button(root, text="Summarize", command=summarize)
# summarize_btn.pack(pady=10)

# reminders_btn = tk.Button(root, text="Reminders", command=reminders)
# reminders_btn.pack(pady=10)

# load_btn = tk.Button(root, text="Load Recording", command=load_recording)
# load_btn.pack(pady=10)

# language_var = tk.StringVar(root)
# language_var.set("Select Language")

# lang_dropdown = tk.OptionMenu(root, language_var, *supported_languages.keys())
# lang_dropdown.pack(pady=10)

# translate_btn = tk.Button(root, text="Translate", command=translate)
# translate_btn.pack(pady=10)

# root.mainloop()
