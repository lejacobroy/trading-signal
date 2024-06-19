import time
from alerts import check_alerts

def start_scheduler():
    while True:
        check_alerts()
        time.sleep(3600)  # Run every hour