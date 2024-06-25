from app import create_app
import sys
from subprocess import Popen, PIPE, STDOUT

if __name__ == "__main__":
    p = Popen([sys.executable, './scheduler.py'], 
                                    stdout=PIPE, 
                                    stderr=STDOUT)
    app = create_app()
    app.run(host="0.0.0.0", port=4000)
