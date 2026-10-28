# Hướng Dẫn Cài Đặt và Khởi Chạy OmniRoute (AI Gateway) Trên Ubuntu Server

Tài liệu hướng dẫn triển khai **OmniRoute** để làm AI Gateway/Proxy trên máy ảo Ubuntu Server, cấu hình tường lửa và thiết lập chạy nền tự khởi động cùng hệ thống.

---

## 1. Phương Pháp Cài Đặt

Bạn có thể chọn 1 trong 2 cách: **Cách 1 (NPM)** khuyên dùng vì gọn nhẹ và tốn ít RAM nhất; hoặc **Cách 2 (Docker)** nếu bạn muốn môi trường đóng gói cô lập.

### Cách 1: Cài đặt trực tiếp qua NPM (Khuyên dùng)

*Yêu cầu:* Node.js phiên bản $\ge$ 20 hoặc 22.

#### Bước 1: Cài đặt Node.js v22 LTS (NodeSource)

```bash
sudo apt update && sudo apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

Kiểm tra phiên bản cài đặt thành công:

```bash
node -v && npm -v
```

#### Bước 2: Cài đặt gói OmniRoute toàn cục

```bash
sudo npm install -g omniroute
```

#### Bước 3: Khởi chạy thử nghiệm

```bash
omniroute
```

> Mặc định dịch vụ sẽ lắng nghe tại cổng **`20128`**.

---

### Cách 2: Chạy bằng Docker

Nếu máy ảo đã có Docker và Docker Compose, chỉ cần chạy 1 container duy nhất:

```bash
docker run -d \
  --name omniroute \
  --restart unless-stopped \
  -p 20128:20128 \
  -v omniroute_data:/app/data \
  diegosouzapw/omniroute:latest
```

*Giải thích tham số:*

- `--restart unless-stopped`: Tự khởi động lại container khi máy ảo reboot hoặc crash.
- `-p 20128:20128`: Ánh xạ cổng `20128` từ máy ảo vào container.
- `-v omniroute_data:/app/data`: Lưu trữ dữ liệu cấu hình bền vững vào Docker volume.

---

## 2. Thiết Lập Tường Lửa (UFW) Mở Cổng 20128

Để máy tính bên ngoài (máy Mac) có thể kết nối vào Dashboard hoặc gửi API request đến OmniRoute:

```bash
# Mở cổng 20128 cho giao thức TCP
sudo ufw allow 20128/tcp

# Nạp lại cấu hình tường lửa và kiểm tra
sudo ufw reload
sudo ufw status
```

---

## 3. Chạy Nền Bằng Dịch Vụ Systemd (Tự Bật Cùng Máy Ảo)

Khi cài bằng NPM, chạy lệnh `omniroute` trực tiếp sẽ tắt khi đóng cửa sổ terminal. Dưới đây là cách tạo service `systemd` để OmniRoute tự động chạy nền 24/7:

1. **Xác định đường dẫn nhị phân của `omniroute`:**

   ```bash
   which omniroute
   # Kết quả thường là: /usr/bin/omniroute
   ```
2. **Tạo file service systemd:**

   ```bash
   sudo nano /etc/systemd/system/omniroute.service
   ```
3. **Dán cấu hình sau (thay `raymond` bằng username thực tế của bạn):**

   ```ini
   [Unit]
   Description=OmniRoute AI Gateway Service
   After=network.target

   [Service]
   Type=simple
   User=raymond
   WorkingDirectory=/home/raymond
   ExecStart=/usr/bin/omniroute
   Restart=always
   RestartSec=5
   Environment=NODE_ENV=production

   [Install]
   WantedBy=multi-user.target
   ```
4. **Kích hoạt và khởi động service:**

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now omniroute
   ```
5. **Kiểm tra trạng thái hoạt động:**

   ```bash
   sudo systemctl status omniroute
   ```

---

## 4. Kiểm Tra & Truy Cập Dashboard Từ Máy Mac

Sau khi OmniRoute chạy:

### A. Kiểm tra API nội bộ trên Ubuntu

```bash
curl http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"auto","messages":[{"role":"user","content":"Hello!"}]}'
```

### B. Mở Dashboard từ trình duyệt trên Mac

Mở trình duyệt (Safari/Chrome) và truy cập vào IP của máy ảo:

```plaintext
http://<IP_MAY_AO>:20128/dashboard
```

*Ví dụ:*

- Dùng mạng ảo NAT (Parallels): `http://10.211.55.20:20128/dashboard`
- Dùng mạng Bridged / VPS Cloud: `http://192.168.2.x:20128/dashboard` hoặc `http://<EXTERNAL_IP>:20128/dashboard`
