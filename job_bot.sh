#!/bin/sh

# Keep bot active to scan every 3 days
while true
do
    python3 job_notifier.py
    rm *report.txt
    # Activate every 3 days
    sleep 3d
done