import json
import requests
from bs4 import BeautifulSoup



with open('jobs.html', 'r') as file:

    contents = file.read()
#turn the contents into soup and store all the links into jobs variable
    search_soup = BeautifulSoup(contents, 'lxml')
    jobs_list = search_soup.findAll('a', class_ = "result-card__full-card-link")


"""psuedo
for job_link in jobs_list:
	get all the data via function
	request = requests.get(job_link)

"""


def job_info_from_soup(soup):
	temp = job_soup.find('div',class_ = "topcard__content-left")
	title = temp.find('h1', class_ = "topcard__title").text
	company = temp.find('a', class_ = "topcard__org-name-link topcard__flavor--black-link").text
	location = temp.find('span', class_ = "topcard__flavor topcard__flavor--bullet").text
	salary = temp.find('div',class_ = "salary topcard__flavor--salary").text
	return [temp, title, company, location, salary]

