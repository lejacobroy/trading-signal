from scheduler import start_scheduler
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
    start_scheduler()