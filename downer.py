#!/usr/bin/env python

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import requests
from bs4 import BeautifulSoup
from urllib import quote_plus
from pprint import pprint
import json
import re

import config

class Downer:
	master = []
	def __init__(self, search):
		if not search:
			raise Exception("Empty Search String")
		self.search = quote_plus(search)
	
	def download_page(self):
		self.url = config.search_mask.replace('$',self.search)
		try:
			r = requests.get(self.url)
			self.page = r.text
			return self.page
		except requests.exceptions.ConnectionError:
			raise Exception("Connection Problem!")
	
	def extract_info(self):
		try:
			soup = BeautifulSoup(self.page)
		except AttributeError, NameError:
			raise Exception("No Data to extract")
		
		song_list = soup.find_all(id='song_html')
		for song in song_list:
			#Getting the individual songs
			detail_class = str(song.find('div', {'class':'left'}))
			#Replacing <br/> with \n
			detail_class = detail_class.replace('<br/>', '\n')
			#Stripping all HTML tags
			details = re.sub(r'<[^>]*>', '', detail_class).strip().split('\n')
			#Classifying the details scrapped
			try:
				det = {
					'bitrate' : details[0],
					'duration' : details[1],
					'file_size' : details[2]
				}
			except IndexError:
				continue
			#Now Fix the URL
			det['dlink'] = song.find(href=(re.compile(r'\.mp3$')))['href']
			det['songName'] = song.find(id='right_song').div.b.get_text()
			self.master.append(det)
		return self.master

	def send_json_reply(self):
		print json.dumps(self.master)
