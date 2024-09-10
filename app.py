from flask import Flask, jsonify
import requests
import logging
import threading
import time

# Configure logging to output to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        #logging.FileHandler('server_status.log'),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)

app = Flask(__name__)

def check_file_availability(url, timeout=5):
    headers = {'Range': 'bytes=0-1023'}  # Request the first 1 KB (1024 bytes)
    try:
        # Send GET request with Range header
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)

        if response.status_code == 206:  # Partial Content, file exists
            logging.info("Server is active to give files. Status code: %d", response.status_code)
        elif response.status_code == 200:  # OK, some servers may return 200 with the whole file
            logging.info("Server is active to give files (but no partial content). Status code: %d",
                         response.status_code)
        else:
            logging.warning("Server responded with status code: %d", response.status_code)
    except requests.ConnectionError:
        logging.error("Failed to connect to the server.")
    except requests.Timeout:
        logging.error("Request timed out.")
    except Exception as e:
        logging.error("An unexpected error occurred: %s", str(e))

def job():
    url = "https://superior-dareen-firework-d62602f5.koyeb.app/stream/226?hash=e64f94"
    check_file_availability(url)

def scheduled_task():
    while True:
        job()  # Run the job
        time.sleep(3600)  # Wait for 1 hour

# Start the background thread for the scheduled task
thread = threading.Thread(target=scheduled_task, daemon=True)
thread.start()

@app.route('/')
def home():
    return jsonify(message="Flask server is running and scheduler is active.")

@app.route('/check')
def check():
    job()  # Run the job immediately
    return jsonify(message="File availability check triggered.")

if __name__ == '__main__':
    app.run(debug=True)
