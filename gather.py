import json
import requests
from bs4 import BeautifulSoup



with open('jobs.html', 'r') as file:

    contents = file.read()
#turn the contents into soup and store all the links into jobs variable
    search_soup = BeautifulSoup(contents, 'lxml')
    jobs_list = search_soup.findAll('a', class_ = "result-card__full-card-link")


"""psuedo
for job in jobs_list:
	get all the data via function

"""