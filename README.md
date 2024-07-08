
# RANDOM VNC

Đây là một script Python để quét các VNC (Virtual Network Computing) server và thu thập thông tin chi tiết từ các server ngẫu nhiên. Script này sử dụng API từ [ComputerNewb](https://computernewb.com/) để lấy thông tin.

## Chức năng

Script hỗ trợ các chức năng sau:

1. Quét một mục ngẫu nhiên.
2. Quét theo Clientname.
3. Quét theo mã quốc gia.
4. Quét theo ASN của nhà cung cấp dịch vụ.

## Yêu cầu

- Python 3.6+
- Các thư viện Python: `requests`

## Cài đặt

### 1. Cài đặt Python

Nếu bạn chưa có Python, bạn có thể tải và cài đặt từ [đây.](https://www.python.org/downloads/).

### 2. Cài đặt thư viện cần thiết

Chạy lệnh sau để cài đặt thư viện, nếu chưa có:

```sh
pip install requests
```

### 3. Tải mã nguồn

Bạn có thể tải mã nguồn bằng cách sử dụng `git` hoặc `wget`.

#### Sử dụng Git

```sh
git clone https://github.com/vinzcyun/vnc_random.git
cd vnc_random
python rdvnc.py
```

#### Sử dụng Wget

```sh
wget -O rdvnc.py https://raw.githubusercontent.com/vinzcyun/random_vnc/main/rdvnc.py
python rdvnc.py
```

## Sử dụng

### Chạy script

Để chạy script, mở terminal hoặc cmd và điều hướng đến thư mục chứa file `rdvnc.py`. Sau đó, chạy lệnh:

```sh
python rdvnc.py
```

### Hướng dẫn sử dụng chi tiết

Sau khi chạy script, bạn sẽ thấy menu với các tùy chọn như sau:

```
 __      ___   _  _____ 
 \ \    / / \ | |/ ____|
  \ \  / /|  \| | |     
   \ \/ / | . ` | |     
    \  /  | |\  | |____ 
     \/   |_| \_|\_____|
                        
Telegram: @oatdonemdume
API: ComputerNewb
---------------------------------
CHỌN CHỨC NĂNG:))
1: Quét một mục ngẫu nhiên
2: Quét theo Clientname
3: Quét theo mã quốc gia
4: Quét theo ASN của nhà cung cấp dịch vụ
```

#### Lựa chọn 1: Quét một mục ngẫu nhiên

1. Nhập số lần request để lấy IP ngẫu nhiên. Ví dụ: `10`
2. Script sẽ thực hiện các request và kiểm tra các cổng VNC. Nếu tìm thấy cổng mở, thông tin sẽ được lưu vào file `good.txt` và hiển thị trên màn hình.

#### Lựa chọn 2: Quét theo Clientname

1. Nhập tên client (ví dụ: `Qemu`, `Meta`, `JDownloader`,...).
2. Script sẽ tìm kiếm các server VNC với tên client đã nhập và kiểm tra các cổng VNC. Nếu tìm thấy cổng mở, thông tin sẽ được lưu vào file `good.txt` và hiển thị trên màn hình.

#### Lựa chọn 3: Quét theo mã quốc gia

1. Nhập mã quốc gia (ví dụ: `VN` - Việt Nam, `CN` - Trung Quốc, `RU` - Nga,...).
2. Script sẽ tìm kiếm các server VNC trong quốc gia đã nhập và kiểm tra các cổng VNC. Nếu tìm thấy cổng mở, thông tin sẽ được lưu vào file `good.txt` và hiển thị trên màn hình.

#### Lựa chọn 4: Quét theo ASN của nhà cung cấp dịch vụ

1. Nhập ASN (có thể tìm trên Google).
2. Script sẽ tìm kiếm các server VNC với ASN đã nhập và kiểm tra các cổng VNC. Nếu tìm thấy cổng mở, thông tin sẽ được lưu vào file `good.txt` và hiển thị trên màn hình.

## Lưu ý

- Các kết quả quét sẽ được lưu trong file `good.txt` nếu tìm thấy cổng mở.
- Script chỉ hoạt động nếu máy chủ VNC trả về thông tin hợp lệ và cổng mở.

## Liên hệ

Nếu có bất kỳ câu hỏi nào, vui lòng liên hệ qua Telegram: [@oatdonemdume](https://t.me/@oatdonemdume)

---
