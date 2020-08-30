#!/bin/sh

# Keep bot active to scan every 2 days
while true
do
    python3 job_report_generator.py
    rm *report.txt
    # Activate python script every 2 days
    date="`date`"
    echo "Report Sent on $date"
    sleep 2d
done
