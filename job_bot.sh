#!/bin/sh

# Keep bot active to scan every 3 days
while true
do
    python3 job_notifier.py
    rm *report.txt
    # Activate every 2 days
    date="`date`"
    echo "Report Sent on $date"
    sleep 3d
done