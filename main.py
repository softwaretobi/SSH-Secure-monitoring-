import os
import time
import subprocess  
import psutil
import logging
import telebot
from collections import deque
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
TELEGRAM_BOT_TOKEN = 'Your Télégram Tokens -- DM @botfather to create one '
TELEGRAM_CHAT_ID = 'chat id telegram | @chatIdrobot'
TRAFFIC_THRESHOLD_MBPS = 3  
TRAFFIC_THRESHOLD_BPS = TRAFFIC_THRESHOLD_MBPS * 1_000_000  
CHECK_INTERVAL = 20  
WATCHED_DIRECTORY = '/root/'  
FILE_STABILITY_DELAY = 5  

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


traffic_history = deque(maxlen=60)  

def send_telegram_alert(message):
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f"Message sent to Telegram:  {message}")
    except Exception as e:
        logging.error(f"Error sending Telegram message:  {e}")

def get_ssh_connections():
    try:
        output = subprocess.check_output(['who']).decode('utf-8')
        return output.strip().split('\n')
    except Exception as e:
        logging.error(f"Error checking SSH connections:  {e}")
        return []

def get_network_traffic():
    try:
        net_io_start = psutil.net_io_counters()
        time.sleep(CHECK_INTERVAL)
        net_io_end = psutil.net_io_counters()
        bytes_sent = net_io_end.bytes_sent - net_io_start.bytes_sent
        bytes_recv = net_io_end.bytes_recv - net_io_start.bytes_recv
        total_bytes = bytes_sent + bytes_recv
        logging.info(f"Total bytes captured: {total_bytes}")
        return total_bytes
    except Exception as e:
        logging.error(f"Network traffic recovery error: {e}")
        return 0

def convert_bytes_to_mbps(bytes_per_sec):
    return bytes_per_sec * 8 / 1_000_000

def convert_bytes_to_gbps(bytes_per_sec):
    return bytes_per_sec * 8 / 1_000_000_000

def check_traffic(current_traffic):
    if len(traffic_history) < 2:
        traffic_history.append(current_traffic)
        return False

    previous_traffic = traffic_history[-1]
    traffic_rate = (current_traffic - previous_traffic) / CHECK_INTERVAL
    traffic_history.append(current_traffic)

    average_rate = sum(traffic_history) / len(traffic_history) / CHECK_INTERVAL
    traffic_rate_mbps = convert_bytes_to_mbps(traffic_rate)
    average_rate_mbps = convert_bytes_to_mbps(average_rate)
    
    logging.info(f"Current traffic rate: {traffic_rate_mbps:.2f} Mbps")
    logging.info(f"Average traffic rate: {average_rate_mbps:.2f} Mbps")
    
    if traffic_rate > TRAFFIC_THRESHOLD_BPS:
        send_telegram_alert(f"anormal network traffic detected : {traffic_rate_mbps:.2f} Mbps")
        return True
    return False

def detect_dos_attack():
    current_traffic = get_network_traffic()
    if check_traffic(current_traffic):
        current_traffic_mbps = convert_bytes_to_mbps(current_traffic / CHECK_INTERVAL)
        send_telegram_alert(f"Possible DDoS attack detected:  {current_traffic_mbps:.2f} Mbps")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_modification_times = {}

    def read_file_content(self, path):
        try:
            with open(path, 'r') as file:
                return file.read()
        except PermissionError:
            logging.error(f"Permission denied to read file {path}.")
            return "Permission denied to read the file."
        except FileNotFoundError:
            logging.error(f"File {path} not found during playback.")
            return "File not found during playback. "
        except Exception as e:
            logging.error(f"Error reading file  {path}: {e}")
            return " Unable to read file . "

    def on_modified(self, event):
        if not event.is_directory and not event.src_path.endswith('.swp'):
            self.file_modification_times[event.src_path] = time.time()

    def on_created(self, event):
        if not event.is_directory and not event.src_path.endswith('.swp'):
            self.file_modification_times[event.src_path] = time.time()
            content = self.read_file_content(event.src_path)
            message = f"New file created: {event.src_path}\nContenu: \n{content}"
            send_telegram_alert(message)
            logging.info(message)

    def on_deleted(self, event):
        if not event.is_directory and not event.src_path.endswith('.swp'):
            message = f"File deleted: {event.src_path}"
            send_telegram_alert(message)
            logging.info(message)

    def process_file_modifications(self):
        current_time = time.time()
        for path, modification_time in list(self.file_modification_times.items()):
            if current_time - modification_time >= FILE_STABILITY_DELAY:
                content = self.read_file_content(path)
                message = f"Modified file: {path}\nContenu: \n{content}"
                send_telegram_alert(message)
                logging.info(message)
                del self.file_modification_times[path]

def main():
    previous_ssh_connections = set()

    
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCHED_DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            try:
                
                current_ssh_connections = set(get_ssh_connections())
                new_connections = current_ssh_connections - previous_ssh_connections
                if new_connections:
                    message = f"New SSH connection(s) detected:\n{', '.join(new_connections)}"
                    send_telegram_alert(message)
                    logging.info(message)

                previous_ssh_connections = current_ssh_connections

              
                detect_dos_attack()

               
                event_handler.process_file_modifications()

                time.sleep(CHECK_INTERVAL)

            except Exception as e:
                error_message = f"Error in main loop:  {e}"
                logging.error(error_message)
                send_telegram_alert(error_message)
                time.sleep(60) 
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
