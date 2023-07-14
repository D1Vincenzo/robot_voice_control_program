import tkinter as tk
from speech_to_text import Transcriber
import threading

root = tk.Tk()

root.geometry("500x500")
root.title("Robot Voice Control")


def initialize():
    global transcriber
    transcriber = Transcriber()
    text = 'Successfully loaded, press Enter to start'
    output_text.insert(tk.END, text + '\n')

def start_transcription():
    # Create a new thread for the transcription process
    transcription_thread = threading.Thread(target=perform_transcription)
    transcription_thread.start()

def perform_transcription():
    for transcript in transcriber.start():
        print(transcript)
        output_text.insert(tk.END, transcript + '\n')

def stop_transcription():
    transcriber.stop()



create_button = tk.Button(root, text="Initialize", command=initialize)
create_button.pack()


start_button = tk.Button(root, text="Start Transcription", command=start_transcription)
start_button.pack()

stop_button = tk.Button(root, text="Stop Transcription", command=stop_transcription)
stop_button.pack()

output_text = tk.Text(root)
output_text.pack()



root.mainloop()



