# Casual Job Hunting Bot
This is a project I had made for fun to reduce job hunting times and recieving 
information on opportunities at companies I want to work for. This is intended
to run on a dedicated computer so I can search other job sites
instead of the few outlined in the program which I frequently observe.

This was integrated into a Raspberry Pi as a dedicated device
for continual program execution.

## How does it work?
The bot utilises python to scrape webpages of job listings and then
a shell script to execute every 2 days to send an email attached with
text file reports.

The python script then sends an email with text file reports with summarised 
information, depending on the type of job post that a company uses (scraping 
each webpage is a unique case). The script uses bs4, requests, smtplib and 
email libraries.

The shell script adds the bot functionality, using sleep to delay
when the python script executes.

## How to use it?
The bot is activated through executing the shell script.
#### `./job_searching_bot.sh`

## Error handling
The python script prints the error the STDOUT, and notifies the user via email
that an error has occured (unless an error occurs with sending an email).
However, all errors through the shell script will be logged in a text file and 
bot execution will be halted.

## Required fixes/additional requirements
    - Add a better system of adding website and file report arguments.
    - Add a remote error notification measure when STMP server error has occured.
    - Add a packages file.