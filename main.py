import tkinter as tk
from speech_to_text import Transcriber
import threading
from word_embedding import find_the_most_similar_command

root = tk.Tk()
root.geometry("500x500")
root.title("Robot Voice Control")

transcriber = None  # Global variable to hold the Transcriber instance
transcription_thread = None  # Global variable to hold the transcription thread
transcription_running = False  # Variable to track the state of the transcription process
initialized = False

def initialize():
    global transcriber, initialized
    transcriber = Transcriber()
    text = 'Successfully loaded, press Enter to start'
    output_text.insert(tk.END, text + '\n')
    initialized = True

def toggle_transcription():
    global transcription_running, transcription_thread
    if initialized != True:
        initialize()
        start_button.config(text="Start Transcription")
    else:
        if not transcription_running:
            # Start the transcription process
            transcription_thread = threading.Thread(target=perform_transcription)
            transcription_thread.start()
            start_button.config(text="Stop Transcription")
            transcription_running = True
        else:
            # Stop the transcription process
            transcriber.stop()
            start_button.config(text="Start Transcription")
            transcription_running = False

def perform_transcription():
    for transcript in transcriber.start():
        output_text.insert(tk.END, transcript + '\n')  
        if find_the_most_similar_command(transcript): 
            output_text.insert(tk.END, "Command Received:")   
            output_text.insert(tk.END, find_the_most_similar_command(transcript))   
            output_text.insert(tk.END, "\n")   
            print(find_the_most_similar_command(transcript))



start_button = tk.Button(root, text="Initialize", command=toggle_transcription)
start_button.pack()

output_text = tk.Text(root)
output_text.pack()

root.mainloop()
