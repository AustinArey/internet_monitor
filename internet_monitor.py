import speedtest
import mysql.connector
import subprocess
from datetime import datetime
import time
# Import configuration
from config import DB_CONFIG, TEST_INTERVAL

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
    INSERT INTO results (timestamp, download_speed, upload_speed, latency, access_point)
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
    while True:
        perform_test_and_log()
        time.sleep(TEST_INTERVAL * 60)  # Convert minutes to seconds

