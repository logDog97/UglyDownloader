#!/usr/bin/python3
import commands
import requests
import os, errno
from bs4 import BeautifulSoup
import urllib.request
import threading

from tkinter import *
from tkinter import ttk, filedialog

download_size = 0

def frame_configure(canvas):
	root.update()
	canvas.configure(scrollregion = canvas.bbox("all"))

def get_path():
	path.set(filedialog.askdirectory())


def start_download(webpage_url, path, frame):
	progress = IntVar()
	pbar = ttk.Progressbar(frame, orient = HORIZONTAL, length = 100, mode = "determinate", variable = progress)
	pbar.grid(column = 0, row = 5, sticky = "S W E") 
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
	for i in range(0, len(commands.files_to_download)):
		if(commands.files_to_download[i].checkVar.get()):
			url = commands.construct_url(webpage_url, commands.files_to_download[i].link['href'])
			response = requests.get(url, stream = True)
			response_head = requests.head(url)
			file_size = len(response.content)
			#file_name = os.path.join(path, files_to_download[i].link['href'])
			with open(path + "/" + commands.files_to_download[i].link['href'], "wb") as dl_file:
				for chunk in response.iter_content(chunk_size = 1024):
					progress.set()
					if chunk:
						dl_file.write(chunk)
			#progress.set((int(response_head.headers['Content-Length']) * 100)/download_size)

def start_download_thread(webpage_url, path, frame):
	'''
	global download_size
	for i in range(0, len(commands.files_to_download)):
		if(commands.files_to_download[i].checkVar.get()):
			url = commands.construct_url(webpage_url, commands.files_to_download[i].link['href'])
			response = requests.head(url)
			download_size += int(response.headers['Content-Length'])
	'''
	download_thread = threading.Thread(target = start_download, args = (webpage_url, path, frame))
	download_thread.start()
	
# Headline frames and canvases ####################################################################

root = Tk()
root.resizable(width = False, height = False)
main_frame = ttk.Frame(root, padding = (5, 12))
list_canvas = Canvas(main_frame, background = "white",borderwidth = 2, relief = GROOVE)
list_frame = Frame(list_canvas, bg = "#ffffff")
first_line_frame = ttk.Frame(root)

# Content for main_frame ##########################################################################

website_label = ttk.Label(first_line_frame, text = "Enter website URL:")
website_url = StringVar()
website_input_box = ttk.Entry(first_line_frame, textvariable = website_url)
website_input_box.focus()
path_label = ttk.Label(main_frame, text = "Enter download location:")
path = StringVar()
content = StringVar()
path_input_box = ttk.Entry(main_frame, textvariable = path)
browse_button = ttk.Button(main_frame, text = "Browse...", command = get_path)
list_canvas.create_window(0, 0, anchor = "nw",window = list_frame)
populate_list = ttk.Button(main_frame, text = "Populate file list", command = lambda: commands.get_list(website_url, list_frame, root))
file_head =  ttk.Label(main_frame, text = "List of available links:")
root.bind("<Return>", lambda e, b = populate_list : b.invoke())
#list_frame.bind("<Configure>", lambda event, canvas = list_canvas : commands.frame_configure(canvas))
#progress = IntVar()
#pbar = ttk.Progressbar(main_frame, orient = HORIZONTAL, length = 100, mode = "determinate", variable = progress)
dl_button = ttk.Button(main_frame, text = "Download", command = lambda : start_download_thread(website_url.get(), path.get(), main_frame))

# scrollbar and related functionality #############################################################

scrollbar = ttk.Scrollbar(root, orient = VERTICAL, command = list_canvas.yview)
list_canvas['yscrollcommand'] = scrollbar.set
root.bind("<Configure>", lambda event, canvas = list_canvas: frame_configure(canvas))

# grid attributes ##################################################################################
first_line_frame.grid(column = 0, row = 0, padx = 5, columnspan = 2, sticky = "W N E S")
main_frame.grid(column = 0, row = 1)
website_label.grid(column = 0, row = 0, sticky = "W N E S")
website_input_box.grid(column = 1, row = 0, pady = 5, sticky = "E W")
path_label.grid(column = 0, row = 0 , sticky = "W")
path_input_box.grid(column = 0, row = 1, pady = 5, columnspan = 2, sticky = "W E")
browse_button.grid(column = 2, row = 1, sticky = "E")
populate_list.grid(column = 2, row = 2, sticky = "E", columnspan = 2)
list_canvas.grid(column = 0, row = 4, sticky = "E")
#list_frame.grid(column = 0, row = 0)
scrollbar.grid(column = 1, row = 1, sticky = "N S E")
file_head.grid(column = 0, row = 3)
#pbar.grid(column = 0, row = 5, sticky = "S W E") 
dl_button.grid(column = 1, row = 5,columnspan = 2, sticky = "E")

first_line_frame.columnconfigure(1, weight = 1)
#root.rowconfigure(0, weight = 1)

root.mainloop()