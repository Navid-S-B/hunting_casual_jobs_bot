# Navid Bhuiyan 
# 29/08/2020

"""
This script scrapes job listing websites of my choice with companies
that I want to seek casual employment, and sends an email
which generates reports for open job opportunities that I will 
be interested in in my local area.

This was integrated into a Rasperry Pi.
"""

# Scraping libreries
import requests
from bs4 import BeautifulSoup
# Send email notification
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

# Create file for woolworths jobs. It only looks on the first page for the job, job type and time posted.
def woolworths():
    
    # Scrape website using html indent and tags specific to this website
    url = "https://www.wowcareers.com.au/jobs/listing?query=&refine_requisition_number=&brand=&state=ACT&country=Australia&refine_posted_within=&expertise=&worktype=&postcode=&location_within=&role="
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    find_jobs = soup.find_all('h3', class_ = 'jobs__listing-item-title')
    find_dates = soup.find_all('span', class_ = "jobs__listing-item-icon--calendar")
    find_job_type = soup.find_all('span', class_ = "jobs__listing-item-icon--clock")

    # Generate report
    job_file = open("woolworths_jobs_report.txt", 'w')
    job_file.write("{}\n\n".format(url))
    for i in range(len(find_jobs)):
        job_file.write("{} | Type: {} | Posted: {}\n".format(find_jobs[i].a.text, find_job_type[i].text, find_dates[i].text))
    job_file.close()

    return 0

# Create job file for JB jobs. It lists all jobs and their deadliies.
def jb():

    # Scrape website using html indent and tags specific to this website
    url = "https://careers.jbhifi.com.au/en/filter/?search-keyword=&location=act%20-%20metro&job-mail-subscribe-privacy=agree"
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    # This website produces double reads, so I specified rhe body tag to search
    find_body = soup.find('tbody',id = "search-results-content")
    find_jobs = find_body.find_all('a', class_ = 'job-link')
    find_dates = find_body.find_all('span', class_ =  'close-date')

    # Generate report
    job_file = open("jb_jobs_report.txt", 'w')
    job_file.write("{}\n\n".format(url))
    for i in range(len(find_jobs)):
        job_file.write("{} | Due: {}\n".format(find_jobs[i].text, find_dates[i].text))
    job_file.close()

    return 0

# Creates files currently, plan to send email notification.
def main():

    # List of functions which produce reports per website
    woolworths()
    jb()

    # List of reports to iterate
    file_list = ["woolworths_jobs_report.txt", "jb_jobs_report.txt"]

    # EMAIL PROTOCOL
    sender_addr = "sender"
    reciever_addr = "reciever"
    
    # Email message
    msg = MIMEMultipart()
    msg['From'] = sender_addr
    msg['To'] = reciever_addr
    msg['Subject'] = "Current Job Listings"
    body = "Generated job reports on {}".format(datetime.now())
    msg.attach(MIMEText(body, 'plain')) 

    # Attaching reports
    for report in file_list:

        # Open file
        attachment = open(report, "rb")
        # Encoding files for email notification
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % report) 
        msg.attach(p)
        # Close file
        attachment.close()

    # SEND EMAIL
    # Create SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(sender_addr, "password") 
    text = msg.as_string() 
    s.sendmail(sender_addr, reciever_addr, text) 
    s.quit()

if __name__ == "__main__":
    main()