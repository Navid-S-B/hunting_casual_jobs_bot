#!/bin/sh

# Keep bot active to scan every 2 days
while true
do
    # Activate program every 2 days
    sleep 2d
    output="`python3 job_report_generator.py`"
    date="`date`"
    # Error detection measures;
    # the python script will produce an error or success message
    # and log it.
    echo "$output | $date\n" >> debug_log.txt
    if test "$output" = "Reports Sent"
    then
        rm *report.txt
    else
        # Remove files if any were produced
        rm *report.txt 2> /dev/null
        exit 1
    fi
done
