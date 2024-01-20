from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

import os
from tkinter import END
import numpy as np
import speech_recognition as sr
import whisper
import torch
import g4f
#test
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform
import threading

charCount=0

def main():
	global stopThread
	root = Tk()
	gui = Window(root)
	root.protocol("WM_DELETE_WINDOW", gui.on_close)  
	gui.root.mainloop()
	
	return None

class Window:

	def __init__(self, root):
		self.root = root
		self.root.geometry('950x550')
		self.root.resizable(0, 0)
		self.root.config(bg='light grey')
		self.root.title("AI Note Taker")
		self.stop_transcriptions = False  # Flag to signal the thread to stop
		

		# Create frames
		top_frame = Frame(root, width=400, height=200, bg='grey')
		top_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=5)

		bottom_frame = Frame(root, width=650, height=1000, bg='grey')
		bottom_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

		# Create open and save buttons
		top_frame.saveB=Button(top_frame, text="Save", command=self.savefile).grid(row=0, column=0, padx=5, pady=5)
		self.button3=Button(top_frame, text="Clear", command=self.clear).grid(row=0, column=1, padx=5, pady=5)
		self.button3=Button(top_frame, text="Record", command=self.record).grid(row=0, column=2, padx=5, pady=5)
		

		# Create transcript textspace
		bottom_frame.textspace = Text(bottom_frame, bg='white', fg='black', font=('Times New Roman', 12), padx=5, pady=5, width=50, wrap=WORD)
		bottom_frame.textspace.grid(row=0, column=0, padx=10, pady=10)
		with open("c:/Users/jayde/OpenAI/gpt/specialgpt/transcription.txt", "r") as file:
			file_content = file.read()
		bottom_frame.textspace.insert(1.0,file_content)
		# Load and display the image for the search button
		image = Image.open("c:/Users/jayde/OpenAI/gpt/specialgpt/right arrow.jpg")
		img = image.resize((50, 50))  # Resize the image
		img = ImageTk.PhotoImage(img)
		Button(bottom_frame, image=img, command=self.search).grid(row=0, column=1, padx=5, pady=0)
		image_label = Label(bottom_frame, image=img)
		image_label.photo = img
		#image_label.grid(row=0, column=1, padx=5, pady=0)

		# Create note textspace
		bottom_frame.notetextspace = Text(bottom_frame, bg='white', fg='black', font=('Times New Roman', 12), padx=5, pady=5, width=50, wrap=WORD)
		bottom_frame.notetextspace.grid(row=0, column=2, padx=10, pady=10)
		with open("c:/Users/jayde/OpenAI/gpt/specialgpt/notes.txt", "r") as file:
			file_content = file.read()
		bottom_frame.notetextspace.insert(1.0,file_content)


	def on_close(self, *args):
			# Get the contents of the Text widget
			print("Closing...")
			bottom_frame = self.root.winfo_children()[1]  # Get the bottom_frame from the root
			transcription = bottom_frame.textspace.get("1.0", "end-1c")
			notes = bottom_frame.notetextspace.get("1.0", "end-1c")
			tfile_path="c:/Users/jayde/OpenAI/gpt/specialgpt/transcription.txt"
			nfile_path="c:/Users/jayde/OpenAI/gpt/specialgpt/notes.txt"
			# Write the contents to the selected file
			with open(tfile_path, "w") as file:
				file.write(transcription)


			with open(nfile_path, "w") as file:
				file.write(notes)
				file.close()
			
			if messagebox.askokcancel("Quit", "Do you want to quit?"):
				self.root.destroy()

	def clear(self):
		bottom_frame = self.root.winfo_children()[1]
		bottom_frame.textspace.delete('1.0', END)
		bottom_frame.notetextspace.delete('1.0', END)

	def search(self):
		self.search_thread = threading.Thread(target=self.search_threaded)
		self.search_thread.daemon = True
		self.search_thread.start()
		
	
	def search_threaded(self):
		g4f.debug.logging = True  
		g4f.debug.version_check = False  
	
		bottom_frame = self.root.winfo_children()[1]  # Get the bottom_frame from the root
		
		global charCount
		print(charCount)
		script1=bottom_frame.textspace.get(1.0, "end-1c")
		print(script1)
		print('')
		script=script1[charCount:len(script1)]
		print(script)
		charCount=len(script1)
		
		response = g4f.ChatCompletion.create(
			model="gpt-3.5-turbo",
			#provider=g4f.Provider.GptGo,
			messages=[{"role": "user", "content":"""Given a section lecture transcription, generate concise and informative
			   bullet points summarizing the key points, 
			  main ideas, and relevant details. Ensure that the bullet points are organized
			   in a logical and coherent structure. Only output bullet points and do not include any boilerplate text that is not part of the transcript. Pay attention to the overall
			   flow of information and aim to create a clear and digestible summary.Here is the transcription """ +script}],
			stream=True,
		)
		for message in response:
			bottom_frame = self.root.winfo_children()[1]  
			bottom_frame.notetextspace.insert(END, message)
			print(message, flush=True, end='')
		bottom_frame.notetextspace.see(END)
			
	def savefile(self):
		savegui = Tk()
		savegui.geometry('560x50')

		filecontents = self.root.winfo_children()[1].notetextspace.get(0.0, END)
		
		def writefile():
			with open(file_name.get() + '.txt', 'w+') as file:
				file.write(filecontents)
				file.close()
				savegui.destroy()
			return None

		Label(savegui, text="File Name").grid(row=0, column=0)
		file_name = Entry(savegui, width=40)
		file_name.grid(row=0, column=1)

		Button(savegui, text="Save", command=writefile).grid(row=0, column=2)

		return None

	def openfile(self):
		opengui = Tk()
		opengui.geometry('560x50')

		def opennew():
			try:
				with open(file_name.get(), "r") as file:
					self.textspace.delete(0.0, END)
					self.textspace.insert(0.0, file.read())
					file.close()
					opengui.destroy()
			except FileNotFoundError:
				file_name.delete(0.0, END)
				file_name.insert(0.0, "FILE NOT FOUND. TRY ANOTHER")

			return None

		Label(opengui, text="File Name").grid(row=0, column=0)
		file_name = Entry(opengui, width=40)
		file_name.grid(row=0, column=1)

		Button(opengui, text="Open", command=opennew).grid(row=0, column=2)

		return None

	def transcribe_threaded(self, model="medium", non_english=False, energy_threshold=1000, record_timeout=2, phrase_timeout=3, default_microphone='pulse'):
		# The last time a recording was retrieved from the queue.
		phrase_time = None
		# Thread safe Queue for passing data from the threaded recording callback.
		data_queue = Queue()
		# We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
		recorder = sr.Recognizer()
		recorder.energy_threshold = energy_threshold
		# Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
		recorder.dynamic_energy_threshold = False

		# Important for linux users.
		# Prevents permanent application hang and crash by using the wrong Microphone
		if 'linux' in platform:
			mic_name = default_microphone
			if not mic_name or mic_name == 'list':
				print("Available microphone devices are: ")
				for index, name in enumerate(sr.Microphone.list_microphone_names()):
					print(f"Microphone with name \"{name}\" found")
				return
			else:
				for index, name in enumerate(sr.Microphone.list_microphone_names()):
					if mic_name in name:
						source = sr.Microphone(sample_rate=16000, device_index=index)
						break
		else:
			source = sr.Microphone(sample_rate=16000)

		# Load / Download model
		if model != "large" and not non_english:
			model = model + ".en"
		audio_model = whisper.load_model(model)

		record_timeout = record_timeout
		phrase_timeout = phrase_timeout
		transcription = ['']

		with source:
			recorder.adjust_for_ambient_noise(source)

		def record_callback(_, audio:sr.AudioData) -> None:
			"""
			Threaded callback function to receive audio data when recordings finish.
			audio: An AudioData containing the recorded bytes.
			"""
			# Grab the raw bytes and push it into the thread safe queue.
			data = audio.get_raw_data()
			data_queue.put(data)

		# Create a background thread that will pass us raw audio bytes.
		# We could do this manually but SpeechRecognizer provides a nice helper.
		recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

		# Cue the user that we're ready to go.
		print("Model loaded.\n")
		bottom_frame = self.root.winfo_children()[1]  # Get the bottom_frame from the root
		bottom_frame.textspace.insert(END, "Recording started...\n")
		while not self.stop_transcriptions:
			try:
				now = datetime.utcnow()
				# Pull raw recorded audio from the queue.
				if not data_queue.empty():
					phrase_complete = False
					# If enough time has passed between recordings, consider the phrase complete.
					# Clear the current working audio buffer to start over with the new data.
					if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
						phrase_complete = True
					# This is the last time we received new audio data from the queue.
					phrase_time = now
					
					# Combine audio data from queue
					audio_data = b''.join(data_queue.queue)
					data_queue.queue.clear()
					
					# Convert in-ram buffer to something the model can use directly without needing a temp file.
					# Convert data from 16 bit wide integers to floating point with a width of 32 bits.
					# Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
					audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

					# Read the transcription.
					result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
					text = result['text'].strip()

					# If we detected a pause between recordings, add a new item to our transcription.
					# Otherwise edit the existing one.
					if phrase_complete:
						transcription.append(text)
					else:
						transcription[-1] = text

					# Clear the console to reprint the updated transcription.
					os.system('cls' if os.name=='nt' else 'clear')
					bottom_frame = self.root.winfo_children()[1]  # Get the bottom_frame from the root
					bottom_frame.textspace.delete('1.0', END)
					for line in transcription:
						print(line)
						bottom_frame = self.root.winfo_children()[1]  # Get the bottom_frame from the root
						bottom_frame.textspace.insert(END, line)
						
					# Flush stdout.
					print('', end='', flush=True)

					# Infinite loops are bad for processors, must sleep.
					sleep(0.25)
			except KeyboardInterrupt:
				break
	
	def transcribe(self, model="medium", non_english=False, energy_threshold=500, record_timeout=2, phrase_timeout=3, default_microphone='pulse'):
		# Create a separate thread for the transcribe_threaded method
		self.transcribe_thread = threading.Thread(target=self.transcribe_threaded, args=(model, non_english, energy_threshold, record_timeout, phrase_timeout, default_microphone))
		self.transcribe_thread.daemon = True
		# Start the thread
		self.transcribe_thread.start()

	def stop_transcription(self):
		# Set the flag to signal the thread to stop
		self.stop_transcriptions = True
		print("Stopping transcription...")
	    # Wait for the thread to finish
		self.transcribe_thread.join()

	
	def record(self):
		if self.root.winfo_children()[0].winfo_children()[2]['relief'] == 'groove':
			# If the button is active, stop transcription and disable the button
			self.stop_transcription()
			self.root.winfo_children()[0].winfo_children()[2]['relief'] = 'raised'
		else:
			# If the button is not active, enable the button, start transcription, and display a message
			self.root.winfo_children()[0].winfo_children()[2]['relief'] = 'raised'
			self.root.update()
			self.stop_transcriptions = False
			self.transcribe("small", False, 1000, 15, 3, 'pulse')  # Reference the transcribe method
			self.root.winfo_children()[0].winfo_children()[2]['relief'] = 'groove'  # Disable the button after recording is complete
		


main()