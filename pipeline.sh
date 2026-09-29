#!/bin/bash
cd /home/orlya/mini-siem
source venv/bin/activate
python3 lire_logs.py >> pipeline.log 2>&1
python3 detection.py >> pipeline.log 2>&1
