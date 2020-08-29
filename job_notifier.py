# Navid Bhuiyan 
# 29/08/2020

"""
This script scrapes job listing websites of my choice with companies
that I want to seek casual employment, and sends an email update every 
3 days with open opportunities in my local area.

This was integrated into a Rasperry Pi.
"""

import requests
from bs4 import BeautifulSoup


def woolworths():

    response = requests.get("https://www.wowcareers.com.au/jobs/listing?query=&refine_requisition_number=&brand=&state=NSW&country=Australia&refine_posted_within=&expertise=&worktype=&postcode=&location_within=&role=")
    soup = BeautifulSoup(response.text,'html.parser')
    find_jobs = soup.find_all('h3', class_ = 'jobs__listing-item-title')
    find_dates = soup.find_all('span', class_ = "jobs__listing-item-icon--calendar")
    find_job_type = soup.find_all('span', class_ = "jobs__listing-item-icon--clock")

    job_file = open("woolworths_jobs.txt", 'w')

    for i in range(len(find_jobs)):
        job_file.write("{} | {} | {}\n".format(find_jobs[i].a.text, find_job_type[i].text, find_dates[i].text))
    
    job_file.close()

    return 0
    

woolworths()

#<div class="jobs__listing-item-brand">Fuel</div>
