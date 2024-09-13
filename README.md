### 📋 ☆ Installation  :

1. Prerequisites

Ensure you have the following installed on your server:

    Python 3.x
    pip for Python package management
    vnstat for network traffic monitoring
    watchdog for file system monitoring
    pyshark for detailed traffic analysis
    telebot for Telegram integration
2. Install Required Packages

Open a terminal and execute the following commands to install the necessary Python packages:
 - pip install watchdog pyshark pyTelegramBotAPI

You may also need to install vnstat and tcpdump if they are not already installed:
 - sudo apt install vnstat tcpdump

3. Set Up vnstat

Initialize the vnstat database for network monitoring:

- sudo vnstat -u -i eth0
- 
4. Set Up Watchdog Permissions

Ensure that the script has the necessary permissions to read and write files in the directories you wish to monitor. You might need to adjust permissions or run the script with elevated privileges:
- sudo chmod -R 755 /root/


### 📋 ☆ Project SSH Montitoring  :
Are you looking for a robust solution to monitor your server's network traffic and file changes in real-time? This script is designed to help you stay on top of your server's activity with minimal hassle.
Key Features:

    Real-Time Traffic Monitoring: Continuously tracks network traffic and alerts you if the traffic exceeds a specified threshold (e.g., 3 Mbps), helping you detect potential DoS attacks or unusual activity.
    File Change Detection: Monitors specific directories for file changes, creations, and deletions. Alerts are sent for any modifications, with detailed content included to keep you informed.
    SSH Connection Alerts: Notifies you of new SSH connections to your server, giving you an overview of who is accessing your system.
    Telegram Integration: Sends instant alerts via Telegram, ensuring that you receive timely notifications directly on your mobile device.
    Customizable Settings: Easily adjust thresholds, check intervals, and monitored directories to fit your specific needs.
    Detailed Logging: Logs all actions and errors for easy troubleshooting and historical review.

Why Use This Script?

    Proactive Security: Quickly identify and respond to unusual network activity or unauthorized file modifications.
    Ease of Use: Simple setup and configuration, with automatic real-time alerts.
    Comprehensive Monitoring: Combines network traffic analysis and file system monitoring in one convenient tool.
    Convenient Notifications: Get real-time updates via Telegram to stay informed on-the-go.

Whether you're managing a single server or multiple systems, this script provides essential monitoring and alerting capabilities to help you maintain the security and integrity of your infrastructure.

-----

### 💻 ☆ Languages & Technologies :

[![Languages](https://skillicons.dev/icons?i=python)]

-----
### 💻 Need Help : 
[!] Contact : https://t.me/payforsmurf | Discord : @tjrsencrime.


### 📲 ☆ Socials :
[![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/softwaretobi)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/payforsmurf)
![Discord](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)

