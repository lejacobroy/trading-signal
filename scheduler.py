import time
from alerts import check_alerts


def start_scheduler():
    while True:
        print("Starting Scheduler")
        check_alerts()
        time.sleep(3600)  # Run every hour

if __name__ == "__main__":
    start_scheduler()