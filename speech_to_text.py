from pvrecorder import PvRecorder
import pvcheetah
from AccessKey import ACCESS_KEY
import threading
import time
import tkinter as tk

# Hardcoded values
library_path = None
model_path = None
endpoint_duration_sec = 1.0
enable_automatic_punctuation = True
audio_device_index = -1
timeout = 10.0

class Transcriber:
    def __init__(self):
        self.cheetah = pvcheetah.create(
            access_key=ACCESS_KEY,
            library_path=library_path,
            model_path=model_path,
            endpoint_duration_sec=endpoint_duration_sec,
            enable_automatic_punctuation=enable_automatic_punctuation)
        self.recorder = PvRecorder(device_index=audio_device_index, frame_length=self.cheetah.frame_length)
        self.text = ''
        self.running = False

    def start(self):
        self.running = True
        self.recorder.start()
        last_input_time = time.time()

        try:
            while self.running:
                partial_transcript, is_endpoint = self.cheetah.process(self.recorder.read())
                if partial_transcript:
                    self.text += partial_transcript
                if is_endpoint:
                    last_input_time = time.time()
                    print(self.text + self.cheetah.flush())
                    self.text = ''
                if time.time() - last_input_time > timeout:
                    break
        finally:
            self.recorder.stop()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    transcriber = Transcriber()

    def start_transcription():
        # Create a new thread for the transcription process
        threading.Thread(target=transcriber.start).start()

    def stop_transcription():
        transcriber.stop()

    root = tk.Tk()
    start_button = tk.Button(root, text="Start Transcription", command=start_transcription)
    start_button.pack()

    stop_button = tk.Button(root, text="Stop Transcription", command=stop_transcription)
    stop_button.pack()

    root.mainloop()
