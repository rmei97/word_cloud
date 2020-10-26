import json
import requests
from bs4 import BeautifulSoup
import time

import sqlite3
import os

def job_info_from_soup(soup):
	# temp = soup.find('div',class_ = "topcard__content-left")
	#variables
	title = soup.find('h1', class_ = "topcard__title").text
	company = soup.find('a', class_ = "topcard__org-name-link topcard__flavor--black-link").text
	location = soup.find('span', class_ = "topcard__flavor topcard__flavor--bullet").text
	description = soup.find('div', class_ = "description__text description__text--rich").text
	# salary = soup.find('div',class_ = "salary topcard__flavor--salary").text
	return [title, company, location, description]

def connect_to_db():
	"""Create a connection to a jobs.db. Useful if I want to update every x scrapes """
	conn = sqlite3.connect('jobs.db')
	c = conn.cursor()
	try:
	    query = """CREATE TABLE listings (index INTEGER PRIMARY KEY, title TEXT NOT NULL, company TEXT NOT NULL, location TEXT NOT NULL, description TEXT NOT NULL)"""
	    c.execute(query)
	except: #trying to catch OperationalError but will commit a sin of except pass:
		pass

def insert():
	return None

###### turn the contents into soup and store all the links into jobs variable
with open('jobs.html', 'r') as file:
    contents = file.read()
    search_soup = BeautifulSoup(contents, 'lxml')
    jobs_list = search_soup.findAll('a', class_ = "result-card__full-card-link")
#####

#### script
conn = sqlite3.connect('jobs.db')
c = conn.cursor()

query = """CREATE TABLE IF NOT EXISTS listings (num INTEGER PRIMARY KEY, title TEXT NOT NULL, company TEXT NOT NULL, location TEXT NOT NULL, description TEXT NOT NULL)"""
c.execute(query)

   
index = 1
for job_link in jobs_list[:3]:
	request = requests.get(job_link['href'])
	time.sleep(1)
	print('sleep')
	posting_soup = BeautifulSoup(request.content, 'lxml')
	
	data = job_info_from_soup(posting_soup)
	data = [index] + data
	query = """INSERT INTO listings VALUES(?, ?, ?, ?, ?);"""
	c.execute(query, data)

	index += 1
	print('Stored')
conn.commit()
conn.close()
print('Connection Closed')

