import requests
import schedule
import time
import logging

# Configure logging to output to both console and a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        #ogging.FileHandler('server_status.log'),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)


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


# First, run the check when the script starts
job()

# Schedule the job to run every 1 hour
schedule.every(1).hour.do(job)

# Run the scheduled tasks continuously
while True:
    try:
        schedule.run_pending()
    except Exception as e:
        logging.error("An error occurred in the scheduler loop: %s", str(e))

    time.sleep(60)  # Wait for 60 seconds before checking for scheduled tasks