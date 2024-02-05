# Raspberry Pi Speed Test Logger

## Overview
This project enables a Raspberry Pi to perform periodic internet speed tests and log the results to a MariaDB database. It includes the ability to detect the current WiFi SSID, making it useful for monitoring the performance of different networks.

## Features
- Automatic speed tests every 5 minutes (configurable).
- Logs download speed, upload speed, latency, and SSID.
- Data stored in a MariaDB database for analysis and tracking over time.

## Prerequisites
- Raspberry Pi with Raspberry Pi OS installed.
- Internet connection (WiFi or Ethernet).
- MariaDB server setup.
- Python 3 installed on Raspberry Pi.

## Installation

### 1. Clone the Repository
First, clone this repository to your Raspberry Pi:
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip3 install speedtest-cli mysql-connector-python
```

### 3. Configuration
- Rename `config.py.example` to `config.py`.
- Edit `config.py` to set your database credentials and desired test interval.

### 4. Database Setup
Ensure your MariaDB database and table are set up as described in the project documentation.

## Usage

### Running the Script
Execute the script manually to start logging speed test results:
```bash
python3 my_speedtest.py
```

### Scheduling the Script
To run the script at a set interval, use the crontab entry (for every 5 minutes as an example):
```bash
*/5 * * * * /usr/bin/python3 /path/to/my_speedtest.py
```

## Customization
- Modify the test interval in `config.py` for different scheduling.
- Extend the database schema in `setup.sql` to capture additional data.

## Troubleshooting
Refer to the script's output and your MariaDB logs for troubleshooting any issues with the speed test logging or database insertion.

## Contributing
Contributions to the project are welcome. Please follow the standard pull request process.

## License
Specify the license under which the project is released.

