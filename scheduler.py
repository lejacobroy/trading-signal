import time
from alerts import check_alerts

if __name__ == "__main__":
    print("Starting Scheduler")
    while True:
        print("Checking Alerts")
        check_alerts()
        time.sleep(3600)  # Run every hour