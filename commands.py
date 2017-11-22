
from bs4 import BeautifulSoup
import urllib.request
import requests
import os, errno


from tkinter import *
from tkinter import ttk

files_to_download = []

class web_checklist:
	def __init__(self, display_frame, link, col, row):
		self.checkVar = IntVar(value = 1)
		self.link = link
		self.checkbutton = ttk.Checkbutton(display_frame, text = link.string, variable = self.checkVar)		#, command = update)
		self.checkbutton.grid(column = col, row = row, sticky = "W")
		cstyle = ttk.Style()
		cstyle.configure("TCheckbutton", background = "#ffffff")

def get_list(website_url, display_frame, root):
	global files_to_download
	files_to_download.clear()
	for checks in display_frame.winfo_children():
		checks.destroy()
	site = urllib.request.urlopen(website_url.get()).read()
	site_soup = BeautifulSoup(site, "html.parser")
	link_list = site_soup.find_all('a')
	file_list = []
	for i in range(0, len(link_list)):
		link_det = web_checklist(display_frame, link_list[i], 0, i + 1)
		files_to_download.insert(i, link_det)
	root.update()

def ret_download_list():
	return files_to_download		

#def update():
#	print("la la la")
#	test = ret_download_list()
#	for i in range(0, len(test)):
#		print(test[i].checkVar.get())

def construct_url(webpage_url, file_path):
	if webpage_url.endswith("/"):
		return webpage_url + file_path
	else:
		return webpage_url + "/" + file_path
