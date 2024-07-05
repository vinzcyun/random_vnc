import requests
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

random_url = 'https://computernewb.com/vncresolver/api/scans/vnc/random'
detail_url_base = 'https://computernewb.com/vncresolver/api/scans/vnc/id/'

def is_port_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((ip, port))
    except (socket.timeout, socket.error):
        return False
    finally:
        sock.close()
    return True

def process_data(data):
    ip = data.get('ip')
    port = data.get('port')
    clientname = data.get('clientname')
    username = data.get('username')
    password = data.get('password')

    if is_port_open(ip, port):
        with open('good.txt', 'a') as file:
            file.write(f"{ip}:{port}\\{clientname}\\{username}\\{password}\n")
        print(f"Đã tìm thấy cổng mở và ghi vào tệp: {ip}:{port}\\{clientname}\\{username}\\{password}")
    else:
        print(f"Cổng {port} trên IP {ip} đã đóng.")

def fetch_detail_by_id(id):
    detail_url = f'{detail_url_base}{id}'
    response = requests.get(detail_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Không thể lấy chi tiết cho ID {id}: {response.status_code}")
        return None

def random_scan_parallel(requests_count, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(requests.get, random_url) for _ in range(requests_count)]
        for future in as_completed(futures):
            try:
                response = future.result()
                if response.status_code == 200:
                    data = response.json()
                    executor.submit(process_data, data)
                else:
                    print(f"Không thể lấy dữ liệu: {response.status_code}")
            except Exception as e:
                print(f"Có lỗi xảy ra: {str(e)}")

def search_by_clientname_parallel(clientname, num_threads):
    search_url = f'https://computernewb.com/vncresolver/api/scans/vnc/search?clientname={clientname}'
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(fetch_detail_by_id, id) for id in data.get('result', [])]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        executor.submit(process_data, result)
                except Exception as e:
                    print(f"Có lỗi xảy ra: {str(e)}")
    else:
        print(f"Không thể tìm kiếm theo clientname: {response.status_code}")

def search_by_country_parallel(country_code, num_threads):
    search_url = f'https://computernewb.com/vncresolver/api/scans/vnc/search?country={country_code}'
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(fetch_detail_by_id, id) for id in data.get('result', [])]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        executor.submit(process_data, result)
                except Exception as e:
                    print(f"Có lỗi xảy ra: {str(e)}")
    else:
        print(f"Không thể tìm kiếm theo mã quốc gia: {response.status_code}")

def search_by_asn_parallel(asn, num_threads):
    search_url = f'https://computernewb.com/vncresolver/api/scans/vnc/search?asn={asn}'
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(fetch_detail_by_id, id) for id in data.get('result', [])]
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        executor.submit(process_data, result)
                except Exception as e:
                    print(f"Có lỗi xảy ra: {str(e)}")
    else:
        print(f"Không thể tìm kiếm theo ASN: {response.status_code}")


print("""
 __      ___   _  _____ 
 \ \    / / \ | |/ ____|
  \ \  / /|  \| | |     
   \ \/ / | . ` | |     
    \  /  | |\  | |____ 
     \/   |_| \_|\_____|
                        
                        
                        """)
print("Telegram: @oatdonemdume")
print("API: ComputerNewb")
print("---------------------------------")
print("CHỌN CHỨC NĂNG:))")
print("1: Quét một mục ngẫu nhiên")
print("2: Quét theo Clientname")
print("3: Quét theo mã quốc gia")
print("4: Quét theo ASN của nhà cung cấp dịch vụ")
option = int(input("Nhập lựa chọn\n••> "))
print("---------------------------")

if option == 1:
    requests_count = int(input("Nhập số lần request để lấy IP random\n•••> "))
    num_threads = 10
    random_scan_parallel(requests_count, num_threads)
elif option == 2:
    clientname = input("Nhập clientname (Ví dụ: Qemu, Meta JDownloader,...)\n•••> ")
    num_threads = 40
    search_by_clientname_parallel(clientname, num_threads)
elif option == 3:
    country_code = input("Nhập mã quốc gia\nVí dụ: VN - Việt Nam\n CN - Trung Quôc\n RU - Nga...\n•••> ")
    num_threads = 40
    search_by_country_parallel(country_code, num_threads)
elif option == 4:
    asn = input("Nhập ASN (có thể tìm trên Google)\n•••> ")
    num_threads = 40
    search_by_asn_parallel(asn, num_threads)
else:
    print("Lựa chọn không hợp lệ.")
