# Hướng Dẫn Cấu Hình Cloudflare Tunnel Cho Dịch Vụ OmniRoute Trên Google Cloud VPS

Tài liệu này hướng dẫn cách tạo và cấu hình **Cloudflare Tunnel (`cloudflared`)** trực tiếp trên Google Cloud VPS (Ubuntu) để public dịch vụ **OmniRoute** ra Internet thông qua tên miền riêng một cách an toàn, bảo mật và ổn định.

---

## 1. Cloudflare Tunnel là gì & Tại sao nên dùng?

### 1.1. Nguyên lý hoạt động

- **Mô hình truyền thống:** Cần gán IP tĩnh công cộng (Public Static IP), cấu hình mở port tường lửa Google Cloud Firewall và UFW (ví dụ port `20128`), chịu rủi ro bị quét cổng (port scan) và tấn công DDoS trực diện vào IP máy chủ.
- **Mô hình Cloudflare Tunnel:** Một tiến trình daemon nhẹ (`cloudflared`) chạy trên VPS và chủ động tạo kết nối mã hóa chiều ra (outbound tunnel) tới mạng Anycast toàn cầu của Cloudflare. Khi người dùng truy cập tên miền, Cloudflare sẽ chuyển tiếp request qua đường hầm này về `localhost:20128` trên VPS.

### 1.2. Lợi ích khi public OmniRoute qua Cloudflare Tunnel

- **Không cần mở port Firewall/UFW:** Giữ nguyên quy tắc tường lửa đóng toàn bộ port nội bộ, không cần cấu hình Google Cloud VPC Ingress Rules.
- **Ẩn hoàn toàn IP thật của VPS:** Giảm thiểu tối đa nguy cơ bị dò quét lỗ hổng và tấn công từ chối dịch vụ (DDoS).
- **Tự động cấp chứng chỉ SSL/TLS miễn phí:** Cloudflare tự xử lý chứng chỉ HTTPS hợp lệ mà không cần cài Certbot/Let's Encrypt hay cấu hình gia hạn phức tạp.
- **Bảo mật nhiều lớp (Zero Trust):** Có thể bật tính năng Cloudflare Access để yêu cầu đăng nhập email/OTP trước khi truy cập Dashboard OmniRoute.
- **Chi phí:** Gói Cloudflare Zero Trust Free hỗ trợ tới **1.000 Tunnel**, miễn phí băng thông không giới hạn và tối đa 50 người dùng xác thực Zero Trust Access.

---

## 2. Mô hình kiến trúc triển khai

```
[ Người dùng / Client / App ]
              │ (HTTPS - 443)
              ▼
   [ Cloudflare Edge Network ]
   (Xử lý SSL, WAF, DDoS, CDN)
              │
              │  (Encrypted Outbound Tunnel - cloudflared)
              ▼
   [ Google Cloud VPS (Ubuntu) ]
   └── cloudflared service (systemd)
              └── Chuyển tiếp về: http://localhost:20128
                       └── [ OmniRoute Service / Docker ]
```

> **Lựa chọn mô hình:** Khuyên dùng cách **cài `cloudflared` trực tiếp trên VPS Google Cloud**. Cách này giúp traffic đi thẳng từ Cloudflare về VPS với độ trễ thấp nhất và độc lập 24/7 (không bị ảnh hưởng nếu máy tính cá nhân ở nhà tắt).

---

## 3. Các bước thực hiện chi tiết

### Bước 1: Cài đặt `cloudflared` trên Ubuntu

Truy cập SSH vào Google Cloud VPS và chạy lần lượt:

```bash
# 1. Tải gói cài đặt cloudflared (.deb) cho kiến trúc x86_64
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb

# 2. Cài đặt file .deb vào hệ thống
sudo dpkg -i cloudflared.deb

# 3. Dọn dẹp file cài đặt tạm
rm cloudflared.deb
```

Kiểm tra lại xem công cụ đã nhận diện chưa:

```bash
cloudflared -v
```

_(Nếu hiển thị phiên bản dạng `cloudflared version 202...` là đã thành công)._

### Bước 2: Tạo Tunnel trên Cloudflare Zero Trust Dashboard

1. Đăng nhập vào [Cloudflare Dashboard](https://dash.cloudflare.com/) > chọn menu **Zero Trust**.
2. Điều hướng tới **Networks** > **Tunnels**.
3. Nhấp vào **Create a tunnel** (hoặc **Add a tunnel**).
4. Chọn loại kết nối: **Cloudflare** (khuyên dùng, quản lý qua Dashboard) > Bấm **Next**.
5. Đặt tên gợi nhớ cho Tunnel (ví dụ: `gcp-vps-omniroute`) > Bấm **Save tunnel**.

---

### Bước 3: Cài đặt và kích hoạt `cloudflared` trên Google Cloud VPS

Tại trang cấu hình Tunnel vừa tạo:

1. Trong phần **Choose your environment**, chọn:
   - **Operating system:** `Debian` (hoặc `Linux`)
   - **Architecture:** `64-bit` (hoặc `amd64`)
2. Cloudflare sẽ sinh sẵn đoạn lệnh cài đặt kèm **Connector Token**.

Sau khi lệnh `cloudflared` đã có sẵn trong hệ thống, bạn dán lại toàn bộ lệnh chứa token đầy đủ mà Cloudflare Zero Trust đã cung cấp cho bạn trong terminal máy vps:

```bash
sudo cloudflared service install eyJhIjoiZTkyNTkyZjQ2OTdkMDAzNDdjZTg4NzA1ZDhmNmU0ODYiLCJ0IjoiZj...
```

_(Lưu ý: Đảm bảo dán trọn vẹn chuỗi token mã hóa ở cuối lệnh mà không bị cắt cụt)._

Kiểm tra trạng thái service hoạt động:

```bash
sudo systemctl status cloudflared
```

_(Nếu thấy `Active: active (running)` và trên Cloudflare Dashboard hiển thị trạng thái connector là **HEALTHY** màu xanh là đã kết nối thành công)._

---

### Bước 3: Cấu hình Public Hostname trỏ về OmniRoute

Quay lại giao diện Cloudflare Zero Trust Dashboard:

1. Chuyển sang tab **Public Hostname** (nằm trong màn hình cấu hình Tunnel).
2. Nhấp vào **Add a public hostname** và điền thông tin:

| Trường thông tin | Giá trị mẫu                 | Giải thích                                       |
| :--------------- | :-------------------------- | :----------------------------------------------- |
| **Subdomain**    | `omni` _(hoặc `ai`, `api`)_ | Tên miền con bạn muốn dùng                       |
| **Domain**       | `yourdomain.com`            | Chọn tên miền chính đang quản lý trên Cloudflare |
| **Path**         | _(để trống)_                | Áp dụng cho toàn bộ đường dẫn                    |
| **Type**         | `HTTP`                      | Giao thức nội bộ mà OmniRoute đang chạy          |
| **URL**          | `localhost:20128`           | Địa chỉ IP và cổng dịch vụ OmniRoute trên VPS    |

3. Nhấp **Save hostname**.

> Cloudflare sẽ tự động cập nhật bản ghi DNS (CNAME trỏ về `<tunnel-id>.cfargotunnel.com`) mà không cần bạn tạo bản ghi thủ công.

---

### Bước 4: Kiểm tra và sử dụng dịch vụ

1. Mở trình duyệt và truy cập:
   ```text
   https://omni.yourdomain.com
   ```
2. Kết quả mong đợi: Giao diện OmniRoute Web UI / API hiển thị với biểu tượng ổ khóa SSL an toàn (HTTPS).
3. Địa chỉ Endpoint gọi API cho các ứng dụng client (Cline, Roo Code, Chatbox, Cursor,...):
   ```text
   https://omni.yourdomain.com/v1
   ```

---

## 4. Các lệnh quản lý Cloudflared cần biết

```bash
# Xem trạng thái kết nối
sudo systemctl status cloudflared

# Khởi động lại service khi có thay đổi
sudo systemctl restart cloudflared

# Xem log thời gian thực để debug sự cố kết nối
sudo journalctl -u cloudflared -f -n 50

# Dừng hoặc vô hiệu hóa service
sudo systemctl stop cloudflared
sudo systemctl disable cloudflared
```

---

## 5. Kinh nghiệm tối ưu & Xử lý sự cố thường gặp

### 5.1. Lỗi `502 Bad Gateway`

- **Nguyên nhân:** Service OmniRoute chưa chạy, crash, hoặc chọn sai port cấu hình.
- **Cách khắc phục:**
  1. Kiểm tra OmniRoute đang chạy hay không:
     ```bash
     sudo systemctl status omniroute
     # Hoặc kiểm tra docker container nếu chạy qua docker:
     docker ps | grep omniroute
     ```
  2. Kiểm tra port `20128` có đang lắng nghe trên VPS không:
     ```bash
     curl -I http://localhost:20128
     ```
  3. Đảm bảo trong cấu hình Public Hostname chọn giao thức là `HTTP` và URL là `localhost:20128`.

### 5.2. Lỗi `WebSockets` khi dùng Chat Streaming

- OmniRoute trả về kết quả dạng streaming token hoặc WebSockets cho các AI tools.
- Vào Cloudflare Dashboard (giao diện chính của domain) > **Network** > Đảm bảo đã bật **WebSockets** (mặc định bật).

### 5.3. Bảo vệ Dashboard quản trị bằng Cloudflare Zero Trust Access (Tùy chọn nâng cao)

Nếu không muốn public giao diện cấu hình OmniRoute cho tất cả mọi người:

1. Vào **Cloudflare Zero Trust** > **Access** > **Applications** > **Add an application**.
2. Chọn **Self-hosted**.
3. Điền đường dẫn `omni.yourdomain.com` và cấu hình chính sách (Policy) chỉ cho phép gửi mã OTP xác nhận về địa chỉ Email cá nhân của bạn trước khi được phép truy cập.

---

## 6. Hướng dẫn gỡ bỏ Tunnel cũ để cài đặt Tunnel mới trên VPS

Khi cần thay thế Tunnel cũ bằng Tunnel mới trên Google Cloud VPS (Ubuntu), bạn có 2 cách thực hiện: **Cách 1** dùng lệnh gỡ tự động của chính `cloudflared` (khuyên dùng vì nhanh và sạch sẽ), hoặc **Cách 2** gỡ thủ công qua `systemd` nếu lệnh tự động gặp lỗi.

### 6.1. Cách 1: Gỡ tự động bằng lệnh `cloudflared service uninstall` (Khuyên dùng)

> [!NOTE]
> Lệnh này bắt buộc phải có `sudo`. Nếu chạy thiếu `sudo`, hệ thống sẽ báo lỗi do không đủ quyền vô hiệu hóa service systemd.

1. **Gỡ service cũ:**

   ```bash
   sudo cloudflared service uninstall
   ```

   _Lệnh này sẽ tự động dừng service và xóa file cấu hình service khỏi systemd._

2. **Nếu vẫn báo lỗi, kiểm tra các service còn sót lại:**

   ```bash
   sudo systemctl list-unit-files | grep cloudflared
   sudo systemctl status cloudflared
   sudo systemctl status cloudflared-update
   ```

   > Tránh xóa file tùy tiện nếu chưa kiểm tra chính xác service nào đang tồn tại.

---

### 6.2. Cách 2: Gỡ bỏ thủ công bằng `systemd` (Dự phòng khi lệnh uninstall bị lỗi)

Nếu lệnh uninstall tự động không hoạt động hoặc service bị kẹt:

1. **Dừng và vô hiệu hóa service:**

   ```bash
   sudo systemctl stop cloudflared
   sudo systemctl disable cloudflared
   ```

2. **Xóa file service và reset systemd:**

   ```bash
   sudo rm -f /etc/systemd/system/cloudflared.service
   sudo systemctl daemon-reload
   sudo systemctl reset-failed cloudflared
   ```

3. **Dọn dẹp token và file cấu hình cũ:**
   - Chỉ gỡ token/config cũ (giữ lại thư mục):
     ```bash
     sudo rm -f /etc/cloudflared/token
     sudo rm -f /etc/cloudflared/config.yml
     ```
   - Hoặc xóa toàn bộ thư mục cấu hình:
     ```bash
     sudo rm -rf /etc/cloudflared
     ```

---

### 6.3. Kiểm tra trước khi cài Tunnel mới

Chạy kiểm tra:

```bash
sudo systemctl status cloudflared
cloudflared --version
```

**Kết quả mong muốn:**

- Service cũ không còn được `systemd` quản lý (hoặc báo `Unit cloudflared.service could not be found`).
- Lệnh `cloudflared --version` vẫn hoạt động bình thường (không cần cài lại file binary).
- Toàn bộ các dịch vụ khác trên VPS không bị ảnh hưởng.

---

### 6.4. Cài đặt Tunnel mới

1. Đăng nhập vào **Cloudflare Dashboard** > **Zero Trust** > **Networks** > **Tunnels**.
2. Chọn Tunnel mới (ví dụ: `googlevmlinux02`).
3. Sao chép lệnh ở mục **Install as service** và chạy trên VPS bằng quyền `sudo`:
   ```bash
   sudo cloudflared service install <NEW_TUNNEL_TOKEN>
   ```
4. Kiểm tra trạng thái hoạt động:

   ```bash
   sudo systemctl status cloudflared
   ```

   Kết quả hiển thị: `Active: active (running)` và connector trên Dashboard chuyển sang **HEALTHY** màu xanh.

> [!CAUTION] **Lưu ý bảo mật về Token:**
> Connector Token chứa quyền kết nối trực tiếp vào mạng của bạn. Nếu vô tình để lộ token trong terminal log chia sẻ hoặc tin nhắn công khai, hãy vào Cloudflare Dashboard để tạo lại (regenerate/revoke) token trước khi cài đặt.

> [!WARNING] **Lưu ý về Tunnel trên Cloudflare:**
> Các thao tác trên chỉ gỡ Tunnel ở phía VPS. Nếu muốn xóa hẳn Tunnel cũ trên Cloudflare, bạn cần xóa riêng trên Dashboard. Tuy nhiên, không xóa Tunnel cũ trên Dashboard nếu domain hiện tại vẫn đang phân giải qua nó.
