from pvrecorder import PvRecorder
import pvcheetah
from AccessKey import ACCESS_KEY
import threading
import time 

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
        print('Successfully loaded, press Enter to start')
    
    def check_stop(self):
        input()
        self.stop_flag.set()
        
    def start(self):
        self.stop_flag = threading.Event()
        self.recorder.start()
        print('Listening... (press Enter to stop or Ctrl+C to terminate)')
        last_input_time = time.time()
        threading.Thread(target=self.check_stop).start()

        try:
            while not self.stop_flag.is_set():
                partial_transcript, is_endpoint = self.cheetah.process(self.recorder.read())
                if partial_transcript:
                    self.text += partial_transcript
                if is_endpoint:
                    last_input_time = time.time()
                    yield self.text+self.cheetah.flush()
                    self.text = ''
                if time.time() - last_input_time > timeout:
                    break
        finally:
            self.recorder.stop()
            self.stop_flag.clear()

if __name__ == "__main__":
    transcriber = Transcriber()
    while True:
        input()
        try:
            for transcript in transcriber.start():
                print(transcript)
        except KeyboardInterrupt:
            print('Stopped by KeyboardInterrupt')
