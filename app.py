import requests
import schedule
import time
import logging
from flask import Flask

# Initialize Flask app
app = Flask(_name_)

# Configure logging to log to the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_file_availability(url, timeout=5):
    headers = {'Range': 'bytes=0-1023'}  # Request the first 1 KB (1024 bytes)
    
    try:
        # Send GET request with Range header
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        
        if response.status_code == 206:  # Partial Content, file exists
            logging.info("Server is active to give files. Status code: %d", response.status_code)
        elif response.status_code == 200:  # OK, some servers may return 200 with the whole file
            logging.info("Server is active to give files (but no partial content). Status code: %d", response.status_code)
        else:
            logging.warning("Server responded with status code: %d", response.status_code)
    except requests.ConnectionError:
        logging.error("Failed to connect to the server.")
    except requests.Timeout:
        logging.error("Request timed out.")

def job():
    url = "https://superior-dareen-firework-d62602f5.koyeb.app/stream/226?hash=e64f94"
    check_file_availability(url)

# Define a route to trigger the job manually
@app.route('/check')
def check_now():
    job()
    return "File availability check completed. Check logs for details."

# Start the Flask app and also schedule the job every 1 hour
if _name_ == '_main_':
    # Schedule the job to run every 1 hour
    schedule.every(1).hour.do(job)

    # Start the Flask app in the background
    while True:
        schedule.run_pending()  # Run scheduled tasks
        time.sleep(60)          # Sleep for 60 seconds

    # Start the Flask web server
    app.run(host='0.0.0.0', port=5000)