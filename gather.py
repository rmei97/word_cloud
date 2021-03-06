import numpy
import json
import requests
from bs4 import BeautifulSoup
import time

import sqlite3
import os

def job_info_from_soup(soup):
	try:
		title = soup.find('h1', class_ = "topcard__title").text
	except AttributeError:
		title = numpy.nan

	try:
		company = soup.find('a', class_ = "topcard__org-name-link topcard__flavor--black-link").text
	except AttributeError:
		company = numpy.nan
	
	try:
		location = soup.find('span', class_ = "topcard__flavor topcard__flavor--bullet").text
	except AttributeError:
		location = numpy.nan
	
	try:
		description = soup.find('div', class_ = "description__text description__text--rich").text
	except AttributeError:
		description = numpy.nan
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
#uncomment for which ever type of job
# with open('data_science.html', 'r') as file:  # posting for data science roles
with open('non_data_science.html', 'r') as file: #postings for non ds roles
    contents = file.read()
    search_soup = BeautifulSoup(contents, 'lxml')
    jobs_list = search_soup.findAll('a', class_ = "result-card__full-card-link")
#####

#### script
conn = sqlite3.connect('jobs.db')
c = conn.cursor()

# job_type = 'data_scientist_posting'
job_type = 'non_data_scientist_posting'

#query = """CREATE TABLE IF NOT EXISTS {} (num INTEGER PRIMARY KEY, title TEXT, company TEXT, location TEXT, description TEXT)""".format(job_type)
query = """CREATE TABLE IF NOT EXISTS {} (num INTEGER PRIMARY KEY, title TEXT, company TEXT, location TEXT, description TEXT)""".format(job_type)
c.execute(query)
   
index = 0
for job_link in jobs_list[index:]:

	try:
		request = requests.get(job_link['href'])
	except:
		print('Retry attempt at index: ', index)
		time.sleep(60) #if we fail to get the link wait 1 minute and request again
		request = requests.get(job_link['href'])

	time.sleep(1) #delay to not get locked out

	posting_soup = BeautifulSoup(request.content, 'lxml')
	data = job_info_from_soup(posting_soup)

	data = [index] + data
	query = """INSERT INTO {} VALUES (?, ?, ?, ?, ?);""".format(job_type)
	c.execute(query, data)

	index += 1
	#watch to see its still running
	if index % 5 == 0:
		conn.commit()
		print('Stored and commited at index ', index)

conn.commit() #final commit()
conn.close()
print('Final commit and closed connection')

