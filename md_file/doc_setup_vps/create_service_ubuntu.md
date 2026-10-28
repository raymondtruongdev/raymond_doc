# Hướng dẫn tạo & quản lý Systemd Service trên Ubuntu

Hướng dẫn tạo service chạy ngầm, tự khởi động cùng hệ thống và các thao tác quản lý cơ bản (ví dụ với `omniroute`).

---

## 1. Tạo Service mới

### Bước 1: Xác định đường dẫn thực thi

```bash
which omniroute
# Ví dụ trả về: /usr/bin/omniroute
```

### Bước 2: Tạo file cấu hình service

Tạo file tại `/etc/systemd/system/<service-name>.service`:

```bash
sudo nano /etc/systemd/system/omniroute.service
```

Nội dung cấu hình mẫu:

```ini
[Unit]
Description=OmniRoute AI Gateway Service
After=network.target

[Service]
Type=simple
User=googlevm
WorkingDirectory=/home/googlevm
ExecStart=/usr/bin/omniroute
Restart=always
RestartSec=10
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

> **Lưu ý:** Cập nhật `User`, `WorkingDirectory` và `ExecStart` đúng với môi trường thực tế.

### Bước 3: Kích hoạt và chạy Service

```bash
sudo systemctl daemon-reload        # Nạp lại cấu hình systemd
sudo systemctl enable --now omniroute  # Bật tự khởi động và chạy ngay lập tức
sudo systemctl status omniroute     # Kiểm tra trạng thái (active/running)
```

---

## 2. Chỉnh sửa Service đã có

Mỗi khi thay đổi file `.service`, thực hiện theo các bước sau:

1. **Mở file chỉnh sửa:**
   ```bash
   sudo nano /etc/systemd/system/omniroute.service
   ```
2. **Áp dụng thay đổi & khởi động lại:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart omniroute
   ```
3. **Kiểm tra trạng thái:**
   ```bash
   sudo systemctl status omniroute
   ```

---

## 3. Bảng lệnh quản lý nhanh (Cheat Sheet)

| Thao tác                            | Lệnh thực thi                                   |
| :----------------------------------- | :------------------------------------------------ |
| **Bật & Chạy ngay**          | `sudo systemctl enable --now <service>`         |
| **Khởi động lại**          | `sudo systemctl restart <service>`              |
| **Dừng service**              | `sudo systemctl stop <service>`                 |
| **Tắt tự khởi động**      | `sudo systemctl disable <service>`              |
| **Kiểm tra trạng thái**     | `sudo systemctl status <service>`               |
| **Xem log realtime**           | `sudo journalctl -u <service> -f`               |
| **Xem N dòng log gần nhất** | `sudo journalctl -u <service> -n 50 --no-pager` |
