# Navid Bhuiyan 
# 29/08/2020

"""
This script scrapes job listing websites of my choice with companies
that I want to seek casual employment, and sends an email
which generates reports for open job opportunities in my local area.

This in combination with a bash shell script will become a job searching
bot.

This was integrated into a Raspberry Pi for continual searching.
"""

# Scraping libaries
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
    find_body = soup.find('tbody', id = 'search-results-content')
    find_jobs = find_body.find_all('a', class_ = 'job-link')
    find_dates = find_body.find_all('span', class_ =  'close-date')

    # Generate report
    job_file = open("jb_jobs_report.txt", 'w')
    job_file.write("{}\n\n".format(url))
    for i in range(len(find_jobs)):
        job_file.write("{} | Due: {}\n".format(find_jobs[i].text, find_dates[i].text))
    job_file.close()

    return 0

# Create job file for officworks jobs. It lists all jobs and their posting times.
def officeworks():

    # Scrape website using html indent and tags specific to this website
    url = "https://mycareer.officeworks.com.au/search/?createNewAlert=false&q=&locationsearch=&optionsFacetsDD_customfield1=&optionsFacetsDD_customfield2=&optionsFacetsDD_customfield4=&optionsFacetsDD_customfield3=Australian+Capital+Territory"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    find_body = soup.find('tbody')
    find_jobs = find_body.find_all('span', class_ = "jobTitle hidden-phone")
    find_jobs_location = find_body.find_all('span', class_ = "jobLocation")
    find_dates = find_body.find_all('span', "jobDate visible-phone")

    # Generate report
    job_file = open("officeworks_jobs_report.txt", 'w')
    job_file.write("{}\n\n".format(url))
    for i in range(len(find_jobs)):

        # Remove all starting and trailing space from output and location
        location = find_jobs_location[i].text.strip()
        output = "{} | Location: {} | Posted: {}".format(find_jobs[i].a.text, location, find_dates[i].text)
        output = output.strip()
        output = output + "\n"
        job_file.write(output)

    job_file.close()

    return 0

# Create job file for coles jobs. It lists all jobs and their deadliies.
def coles():

    # Scrape website using html indent and tags specific to this website
    url = "https://search.colescareers.com.au/cw/en/filter/?search-keyword=&location=act%20-%20metro"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    find_body = soup.find('tbody', id = "search-results-content")
    find_jobs = find_body.find_all('a', class_ = "job-link")
    find_jobs_type = find_body.find_all('span', class_ = "work-type")
    find_dates = find_body.find_all('span', class_ = "close-date")

    # Generate report
    job_file = open("coles_jobs_report.txt", 'w')
    job_file.write("{}\n\n".format(url))
    for i in range(len(find_jobs)):
        job_file.write("{} | Type: {} | Due: {}\n".format(find_jobs[i].text, find_jobs_type[i].text, find_dates[i].text))
    job_file.close()

    return 0

def goodguys():

    # Scrape website using html indent and tags specific to this website
    url = "https://careers.thegoodguys.com.au/en/filter/?search-keyword=&location=act%20-%20metro&job-mail-subscribe-privacy=agree"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    find_body = soup.find('ul', id = "search-results-content")
    find_jobs = find_body.find_all('a', class_ = "job-link")
    find_locations = find_body.find_all('div', class_ = "col-lg-3 col-md-3 hidden-xs department")
    find_dates = find_body.find_all('span', class_ = "close-date")

    # Generate report
    job_file = open("goodguys_jobs_report.txt", 'w')
    job_file.write("{}\n\n".format(url))
    for i in range(len(find_jobs)):
        job_file.write("{} | Location: {} | Due: {}\n".format(find_jobs[i].text, find_locations[i].text, find_dates[i].text))
    job_file.close()

    return 0
    

# Creates reports and attaches them to an email to notify me about jobs
def main():

    # List of functions which produce reports per website
    woolworths()
    jb()
    officeworks()
    coles()
    goodguys()

    # List of reports to iterate
    file_list = ["woolworths_jobs_report.txt", "jb_jobs_report.txt", "officeworks_jobs_report.txt", "coles_jobs_report.txt", "goodguys_jobs_report.txt"]

    # EMAIL PROTOCOL
    sender_addr = ""
    password = ""
    reciever_addr = sender_addr
    
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

    # Create SMTP session 
    s = smtplib.SMTP('smtp-mail.outlook.com', 587) 
    s.starttls() 
    s.login(sender_addr, password) 
    text = msg.as_string() 
    s.sendmail(sender_addr, reciever_addr, text) 
    s.quit()
    
if __name__ == "__main__":
    main()