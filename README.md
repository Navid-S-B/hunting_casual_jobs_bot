# Casual Job Hunting Bot
This is a project I had made for fun to reduce job hunting times and recieving 
information on opportunities at companies I want to work for.

## How does it work?
The bot utilises python to scrape webpages of job listings and then
a shell script to execute every 2 days to send an email attached with
textfile reports.

The python script then sends an email with text file reports with summarised 
information, depending on the type of job post that a company uses (scraping 
each webpage is a unique case). The script uses bs4, requests, smtplib and 
email libraries.

The shell script adds the bot functionality, using sleep to delay
when the python script executes.

This was integrated into a Raspberry Pi as a dedicated 'server'.

## Required fixes
    - Needs better commenting.
    - Needs try/except error handling when the url's might expire
      or the html structure has changed.
    - Add a better system of adding website and file report arguments.
    - Add a packages file.