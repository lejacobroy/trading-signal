#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the main application and scheduler in parallel
python main.py &
python -c "from scheduler import start_scheduler; start_scheduler()" &
wait
