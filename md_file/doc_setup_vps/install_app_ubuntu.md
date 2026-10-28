# Hướng dẫn cài đặt các ứng dụng và công cụ cần thiết trên Ubuntu Server

Tài liệu này tổng hợp các công cụ cốt lõi cần thiết khi quản trị và vận hành một máy chủ Ubuntu Server (VPS), được phân loại rõ ràng kèm giải thích công dụng và câu lệnh chi tiết.

---

## 1. Cập nhật danh sách gói (Bắt buộc trước khi cài đặt)

Trước khi cài bất kỳ gói phần mềm nào, luôn chạy lệnh cập nhật danh mục gói để đảm bảo tải đúng phiên bản mới nhất từ kho lưu trữ:

```bash
sudo apt update && sudo apt upgrade -y
```

- **`apt update`**: Tải thông tin phiên bản các gói phần mềm mới nhất từ repository.
- **`apt upgrade -y`**: Nâng cấp các gói phần mềm hiện có lên phiên bản mới nhất (`-y` tự động đồng ý cài đặt).

---

## 2. Trình soạn thảo văn bản (Text Editors)

Dùng để xem và sửa đổi các file cấu hình hệ thống (như cấu hình Nginx, Cloudflare Tunnel, Systemd Service,...).

### Cách 1: Cài đặt `nano` (Khuyên dùng cho người mới)

`nano` đơn giản, trực quan, có gợi ý phím tắt ngay bên dưới màn hình.

```bash
sudo apt install nano -y
```

- **Mở/sửa file**: `sudo nano /path/to/file`
- **Phím tắt thường dùng**:
  - `Ctrl + O` rồi `Enter`: Lưu file.
  - `Ctrl + X`: Thoát ra ngoài.
  - `Ctrl + W`: Tìm kiếm từ khóa trong file.

### Cách 2: Sử dụng `vim` / `vi` (Mạnh mẽ, thường có sẵn)

Thường được tích hợp sẵn trên hầu hết các bản phân phối Linux.

```bash
sudo apt install vim -y
```

- **Mở/sửa file**: `sudo vim /path/to/file`
- **Các thao tác cơ bản**:
  - Nhấn phím `i`: Vào chế độ chỉnh sửa (Insert mode).
  - Nhấn `Esc`: Thoát chế độ sửa về chế độ lệnh.
  - Gõ `:wq` rồi nhấn `Enter`: Lưu và thoát.
  - Gõ `:q!` rồi nhấn `Enter`: Thoát không lưu.

---

## 3. Công cụ mạng & tải dữ liệu (Network & Download Utilities)

Dùng để tải file cài đặt, kiểm tra API, ping kiểm tra kết nối mạng và các cổng mở.

```bash
sudo apt install curl wget net-tools ufw -y
```

### Giải thích các công cụ:

- **`curl`**: Gửi request HTTP/HTTPS hoặc tải file qua command line (rất hay dùng để test API hoặc chạy script cài đặt tự động).
  - Ví dụ: `curl -I https://google.com` (Kiểm tra phản hồi header HTTP).
- **`wget`**: Tải file trực tiếp từ internet về server.
  - Ví dụ: `wget https://example.com/file.zip`
- **`net-tools`**: Cung cấp các lệnh kiểm tra mạng kinh điển như `netstat`, `ifconfig`.
  - Ví dụ: `sudo netstat -tulpn` (Kiểm tra cổng nào đang mở và tiến trình nào đang chiếm cổng).
- **`ufw` (Uncomplicated Firewall)**: Tường lửa bảo vệ VPS.
  - Cho phép port SSH: `sudo ufw allow 22/tcp`
  - Bật tường lửa: `sudo ufw enable`
  - Xem trạng thái: `sudo ufw status`

---

## 4. Công cụ giám sát hệ thống & tài nguyên (System Monitoring)

Giúp theo dõi tình trạng tiêu thụ CPU, RAM, ổ cứng và các tiến trình chạy ngầm để phát hiện nghẽn tài nguyên.

```bash
sudo apt install htop iotop -y
```

- **`htop`**: Giao diện trực quan hiển thị CPU, RAM, Swap và danh sách tiến trình.
  - Chạy lệnh: `htop` (Nhấn `F10` hoặc `q` để thoát).
- **`iotop`**: Theo dõi tốc độ đọc/ghi ổ cứng theo từng tiến trình (hữu ích khi server bị đơ do nghẽn I/O disk).
  - Chạy lệnh: `sudo iotop`

---

## 5. Công cụ giải nén & đóng gói (Archive Utilities)

Cần thiết khi tải mã nguồn hoặc dữ liệu đóng gói dạng `.zip`, `.tar.gz`.

```bash
sudo apt install zip unzip tar -y
```

- **Giải nén file `.zip`**: `unzip archive.zip -d /path/to/destination`
- **Nén thư mục thành file `.zip`**: `zip -r archive.zip /path/to/folder`
- **Giải nén file `.tar.gz`**: `tar -xzvf archive.tar.gz`

---

## 6. Công cụ quản lý phiên làm việc & chạy ngầm (Terminal Multiplexers)

Tránh bị gián đoạn tiến trình đang chạy khi mất kết nối mạng hoặc tắt terminal SSH.

```bash
sudo apt install tmux -y
```

- **`tmux`**: Cho phép tạo các phiên làm việc độc lập. Khi đóng SSH, tiến trình trong `tmux` vẫn tiếp tục chạy trên server.
  - Tạo phiên mới: `tmux new -s my_session`
  - Thoát tạm thời (Detach): Nhấn `Ctrl + B`, sau đó nhấn `D`.
  - Vào lại phiên làm việc: `tmux attach -t my_session`
  - Liệt kê các phiên: `tmux ls`

---

## 7. Quản lý mã nguồn & tiện ích dòng lệnh (Git & Utilities)

```bash
sudo apt install git jq -y
```

- **`git`**: Quản lý source code, clone repository từ GitHub/GitLab.
  - Kiểm tra phiên bản: `git --version`
- **`jq`**: Tiện ích lọc, định dạng và xử lý dữ liệu JSON ngay trên command line (cực kỳ tiện khi debug API hoặc xem log JSON).

---

## 💡 Tổng hợp lệnh cài nhanh tất cả các công cụ trên một dòng

Nếu vừa tạo VPS mới và muốn chuẩn bị đầy đủ môi trường cơ bản, bạn chỉ cần chạy một lệnh duy nhất:

```bash
sudo apt update && sudo apt install -y nano vim curl wget net-tools ufw htop iotop zip unzip tar tmux git jq
```

```bash
sudo apt update && sudo apt install -y nano vim curl wget net-tools ufw htop iotop zip unzip tar tmux git jq
```
