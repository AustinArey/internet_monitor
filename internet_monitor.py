import speedtest
import mysql.connector
import subprocess
from datetime import datetime, timedelta
import time
# Import configuration
from config import DB_CONFIG, TEST_INTERVAL, PING_INTERVAL, PING_HOST

def log_ping():
    try:
        subprocess.check_output(['ping', '-c', '1', PING_HOST])
        ping_status = 1  # Ping successful
    except subprocess.CalledProcessError:
        ping_status = 0  # Ping failed

    # Log the ping status to the database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO uptime (ping_status)
    VALUES (%s);
    """
    cursor.execute(insert_query, (ping_status,))
    conn.commit()
    cursor.close()
    conn.close()

# Function to get the current SSID
def get_ssid():
    try:
        ssid = subprocess.check_output(['iwgetid', '-r']).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        ssid = "Unknown"
    return ssid

def perform_test_and_log():
    # Access Point Identifier
    access_point = get_ssid()

    # Initialize Speedtest
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    results_dict = s.results.dict()

    # Parse results
    download_speed = results_dict['download'] / 1_000_000  # Convert to Mbps
    upload_speed = results_dict['upload'] / 1_000_000  # Convert to Mbps
    latency = results_dict['ping']

    # Connect to the database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # SQL query to insert data
    insert_query = """
    INSERT INTO speed_test (timestamp, download_speed, upload_speed, latency, access_point)
    VALUES (%s, %s, %s, %s, %s);
    """
    timestamp = datetime.now()

    # Execute query
    cursor.execute(insert_query, (timestamp, download_speed, upload_speed, latency, access_point))

    # Commit and close
    conn.commit()
    cursor.close()
    conn.close()

    print("Speed test results logged successfully.")

# Main loop
if __name__ == "__main__":
    last_speedtest_run = datetime.min
    last_ping_run = datetime.min

    while True:
        now = datetime.now()

        # Check if it's time for a speed test
        if now - last_speedtest_run >= timedelta(minutes=TEST_INTERVAL):
            perform_test_and_log()
            last_speedtest_run = now

        # Check if it's time for a ping test
        if now - last_ping_run >= timedelta(minutes=PING_INTERVAL):
            log_ping()
            last_ping_run = now

        # Sleep for the shortest interval between the two tests to ensure responsiveness
        next_ping_in = PING_INTERVAL * 60 - (now - last_ping_run).total_seconds()
        next_speedtest_in = TEST_INTERVAL * 60 - (now - last_speedtest_run).total_seconds()
        time_to_sleep = min(next_ping_in, next_speedtest_in)
        
        # Prevent negative sleep time in case of overlap or delays in execution
        if time_to_sleep > 0:
            time.sleep(time_to_sleep)

