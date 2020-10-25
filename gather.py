import json
import requests
from bs4 import BeautifulSoup
import time

def job_info_from_soup(soup):
	# temp = soup.find('div',class_ = "topcard__content-left")
	#variables
	title = soup.find('h1', class_ = "topcard__title").text
	company = soup.find('a', class_ = "topcard__org-name-link topcard__flavor--black-link").text
	location = soup.find('span', class_ = "topcard__flavor topcard__flavor--bullet").text
	description = soup.find('div', class_ = "description__text description__text--rich").text
	# salary = soup.find('div',class_ = "salary topcard__flavor--salary").text
	return [title, company, location, description]


with open('jobs.html', 'r') as file:
    contents = file.read()
#turn the contents into soup and store all the links into jobs variable
    search_soup = BeautifulSoup(contents, 'lxml')
    jobs_list = search_soup.findAll('a', class_ = "result-card__full-card-link")


for job_link in jobs_list[:3]:
	request = requests.get(job_link['href'])
	time.sleep(1)
	print('sleep')
	posting_soup = BeautifulSoup(request.content, 'lxml')
	data = job_info_from_soup(posting_soup)

