import customtkinter as ctk
import pyaudio
import wave
import numpy as np
import threading
import time
import speech_recognition as sr
from PIL import Image, ImageTk
import tkinter as tk
import os


class AudioRecorderApp(ctk.CTk):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.initialize()

    def initialize(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.p = pyaudio.PyAudio()

        self.is_recording = False
        self.audio_data = []
        self.fs = 16000
        self.recording_duration = 0
        self.max_duration = 30

        self.geometry("300x300")
        self.resizable(False, False)

        self.mainFrame = ctk.CTkFrame(self)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        self.label = ctk.CTkLabel(self.mainFrame, text="Audio Recorder", font=("Arial", 20))
        self.label.pack(pady=10)

        self.language = tk.StringVar(value="fa-IR")

        # Create a dropdown (OptionMenu)
        options = ["en-US", "fa-IR", "de-DE","it-IT",'fr-FR']
        self.dropdown = ctk.CTkOptionMenu(self, values=options, variable=self.language,)
        self.dropdown.pack(pady=20)

        # self.progress_bar = ctk.CTkProgressBar(self.mainFrame, width=300)
        # self.progress_bar.pack(pady=10)
        # self.progress_bar.set(0)

        # Load images with `master` specified
        try:
            microphone_icon_path = os.path.abspath("./icons/voice.png")
            stop_icon_path = os.path.abspath("./icons/stop.png")

            if not os.path.exists(microphone_icon_path) or not os.path.exists(stop_icon_path):
                raise FileNotFoundError("Icon files not found.")

            # Load and tie images to mainFrame as their master
            self.microphone_image = ImageTk.PhotoImage(
                Image.open(microphone_icon_path).resize((30, 30)),
                master=self.mainFrame
            )
            self.stop_image = ImageTk.PhotoImage(
                Image.open(stop_icon_path).resize((30, 30)),
                master=self.mainFrame
            )
        except Exception as e:
            print(f"Error loading images: {e}")
            self.microphone_image = None
            self.stop_image = None

        self.record_button = ctk.CTkButton(
            self.mainFrame,
            text="Start Recording",
            command=self.start_recording,
            fg_color="red",
            image=self.microphone_image if self.microphone_image else None,
        )
        self.record_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(
            self.mainFrame,
            text="Stop Recording",
            command=self.stop_recording,
            state="disabled",
            image=self.stop_image if self.stop_image else None,
        )
        self.stop_button.pack(pady=10)

        self.exitButton = ctk.CTkButton(
            self.mainFrame,
            text="Exit",
            font=("Arial", 10),
            command=self.exit_app,
            width=80,
        )
        self.exitButton.pack(padx=(30, 10), pady=20)

    def start_recording(self):
        self.is_recording = True
        self.record_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.audio_data = []  # Reset audio data for a new recording
        self.recording_duration = 0
        # self.progress_bar.set(0)  # Reset progress bar

        self.language = self.dropdown.get()

        # Start recording in a separate thread
        threading.Thread(target=self.record).start()

        # Start updating the progress bar
        threading.Thread(target=self.update_progress).start()

    def record(self):
        try:
            # Open a stream with pyaudio to record the audio
            stream = self.p.open(format=pyaudio.paInt16,  # 16-bit audio format
                                 channels=1,  # Mono audio
                                 rate=self.fs,  # Sample rate
                                 input=True,
                                 frames_per_buffer=1024)

            print("Recording started")
            while self.is_recording:
                # Read data from the microphone
                audio_chunk = stream.read(1024)
                self.audio_data.append(audio_chunk)

        except Exception as e:
            print(f"Recording failed: {e}")

    def update_progress(self):
        while self.is_recording and self.recording_duration < self.max_duration:
            time.sleep(1)
            self.recording_duration += 1
            progress = self.recording_duration / self.max_duration
            # self.progress_bar.set(progress)

            # Stop recording automatically if the maximum duration is reached
            if self.recording_duration >= self.max_duration:
                self.stop_recording()

    def stop_recording(self):
        self.is_recording = False
        self.record_button.configure(state="normal")
        self.stop_button.configure(state="disabled")

        # Save the audio data to a WAV file
        audio_file_path = "recorded_audio.wav"
        self.save_audio_to_wav(audio_file_path)

        # Pass the audio file to the transcription function
        self.transcribe(audio_file_path)

    def save_audio_to_wav(self, file_path):
        """Save the audio chunks as a WAV file."""
        # Flatten the list of audio chunks into a single byte string
        audio_bytes = b''.join(self.audio_data)

        # Write the audio data to a WAV file using the PyAudio library
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)  # Mono audio
            wf.setsampwidth(2)  # 2 bytes per sample (16-bit audio)
            wf.setframerate(self.fs)  # Set the sample rate to 16000 Hz
            wf.writeframes(audio_bytes)  # Write the audio to the file

    def transcribe(self, audio_file_path):
        try:
            recognizer = sr.Recognizer()

            # Open the saved audio file and recognize speech
            with sr.AudioFile(audio_file_path) as source:
                audio = recognizer.record(source)

            # Use Google Web Speech API for transcription
            text = recognizer.recognize_google(audio, language=str(self.language))  # Recognize Persian text
            self.root.insert_transcribe_text(text)
            print(f"Recognized text: {text}")
            self.label.configure(text=f"Recognized: {text}")  # Update the label with the recognized text

            # Optionally, delete the audio file after transcription
            os.remove(audio_file_path)

        except sr.RequestError as e:
            print(f"Error while requesting results from Google Speech Recognition service: {e}")
            self.label.configure(text="Error in Speech Recognition")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            self.label.configure(text="Unable to understand the audio")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            self.label.configure(text="Error during transcription")
        except Traceback:
            pass

    def exit_app(self):
        self.destroy()


