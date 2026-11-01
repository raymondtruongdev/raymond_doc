# HƯỚNG ĐẪN KẾT NỐI ĐẾN MÁY LINUX

Tài liệu này hướng dẫn chi tiết các phương thức đăng nhập và xác thực user trên máy LINUX: VPS (Google Cloud Compute Engine) hoặc máy ảo local (VMWare, Parallel Destop), bao gồm giải thích cơ chế hoạt động và cách cấu hình tối ưu.

---

## 1. KẾT NỐI ĐẾN GOOGLE VPS

### Cơ Chế Xác Thực Trên VPS Linux

- **Không có GUI tự đăng nhập**: VPS chạy ở chế độ headless (không màn hình, không giao diện đồ họa). Sau khi khởi động, hệ thống lắng nghe kết nối từ xa qua SSH (cổng 22 mặc định) hoặc Serial Console.
- **Mật khẩu (Password) vs SSH Key**:
  - **Password**: Dễ nhớ nhưng dễ bị tấn công brute-force; mặc định Google Cloud vô hiệu hóa đăng nhập bằng password qua SSH để bảo mật.
  - **SSH Key (Khuyên dùng)**: Sử dụng cặp khóa mã hóa bất đối xứng (_Private Key_ giữ ở máy cá nhân, _Public Key_ đặt trên VPS). An toàn tuyệt đối và đăng nhập không cần gõ mật khẩu.
- **Tài khoản mặc định trên GCP**: Tùy theo cách tạo máy hoặc tài khoản Google, user thường được tạo theo username Google (`tên_email`) hoặc chỉ định khi add SSH Key.

---

### Cách 1: SSH trực tiếp trên trình duyệt Web (GCP Cloud Console)

Dành cho trường hợp cần truy cập khẩn cấp hoặc chưa cấu hình SSH Key trên máy cá nhân.

#### Bước 1: Truy cập vào máy ảo trên google cloud

Truy cập [Google Cloud Console](https://console.cloud.google.com/) -> **Compute Engine** -> **VM instances**.

#### Bước 2: Kết nối ssh trên trình duyệt

Tại dòng của máy ảo Ubuntu, nhấn nút **SSH** ở cột _Connect_.

#### Bước 3: Chờ kết nối hoàn tất

Sau khi thực hiện xong Google Cloud tự động tạo cặp key tạm thời, đẩy public key vào metadata của VM và mở một terminal trực tiếp ngay trên trình duyệt với user mặc định của bạn.

### Cách 2: Kết nối thủ công bằng SSH Key qua Terminal

#### Bước 1: Tạo SSH Key trên máy tính

Mở Terminal và gõ:

```bash
ssh-keygen -t rsa -f ~/.ssh/gcp_vps -C "tenuser"
```

_(Thay `tenuser` bằng tên người dùng bạn muốn đặt và `gcp_vps` bằng tên file key sẽ được tạo ra. Bấm Enter 2 lần để bỏ qua mật khẩu passphrase nếu muốn đăng nhập nhanh)._

Xem và copy toàn bộ nội dung Public Key:

```bash
cat ~/.ssh/gcp_vps.pub
```

#### Bước 2: Thêm SSH Key vào Google Cloud

1. Trên GCP Console, vào **Compute Engine** > menu bên trái chọn **Metadata** (mục Configuration).
2. Chọn tab **SSH Keys** > nhấn **Edit** > nhấn **Add item**.
3. Dán chuỗi Public Key vừa copy vào ô > bấm **Save**.

#### Bước 3: Đăng nhập từ Terminal

Lấy địa chỉ **External IP** của máy ảo trên GCP Console và chạy lệnh:

```bash
ssh -i ~/.ssh/gcp_vps tenuser@YOUR_VM_EXTERNAL_IP
```

> [!IMPORTANT]
> Tên `tenuser` trong lệnh SSH phải **khớp 100%** với phần `-C "tenuser"` lúc tạo SSH Key ở Bước 1. GCP sẽ tự động tạo user này trên Linux và cấp quyền `sudo`.

---

### Cách 3: Đăng Nhập Bằng Mật Khẩu (Password Authentication)

> [!WARNING]
> Không khuyến khích cho môi trường production vì nguy cơ bị scan và dò quét mật khẩu (brute-force).

#### Bước 1: Tạo user + mật khẩu trên máy VPS

Hãy kết nối vào terminal máy VPS và thực hiện các lệnh sau:

1. **Đặt mật khẩu cho user** (chạy trên VPS):

   ```bash
   sudo passwd <your-username>
   ```

2. **Cho phép xác thực mật khẩu qua SSH**:
   Mở file cấu hình SSH Daemon:

   ```bash
   sudo nano /etc/ssh/sshd_config
   ```

   Tìm và đổi (hoặc thêm) các dòng sau:

   ```text
   PasswordAuthentication yes
   KbdInteractiveAuthentication yes
   ```

3. **Khởi động lại dịch vụ SSH**:

   ```bash
   sudo systemctl restart ssh
   ```

#### Bước 2: Dùng máy tính cá nhân kết nối với VPS

Mở Terminal máy tính cá nhân và thực hiện lệnh:

```bash
ssh <your-username>@<IP_PUBLIC_CUA_VPS>
# Hệ thống sẽ yêu cầu nhập mật khẩu vừa đặt
```

---

## Mở Rộng: Sau khi đăng nhập vào máy VPS bằng SSH ta có thể

### Chuyển đổi giữa các user sau khi đăng nhập:

```bash
# Đổi sang user khác:
su - <other-username>

# Chuyển hẳn sang quyền root:
sudo -i
```

## 2. KẾT NỐI VPS Ubuntu (Parallels / Local VM)

Nếu bạn chạy máy ảo Ubuntu cục bộ trên Mac (ví dụ dùng Parallels Desktop, VMware hoặc VirtualBox) thay vì cloud, bạn có 2 cách chính để kết nối SSH:

#### Cách 1: SSH trực tiếp qua IP mạng NAT (Nhanh nhất & Đơn giản nhất)

Mặc dù khác dải IP (`192.168.2.x` vs `10.211.55.x`), máy Mac vẫn có thể kết nối trực tiếp đến IP `10.211.55.20` vì phần mềm ảo hóa (như Parallels) đã tự động tạo một giao diện mạng ảo (`vnic`) trên macOS.

1. **Cài đặt OpenSSH Server trên máy ảo Ubuntu:**
   Mở terminal trong máy ảo Ubuntu và cài đặt gói `openssh-server`:

   ```bash
   sudo apt update
   sudo apt install -y openssh-server
   sudo systemctl status ssh
   ```

   _(Đảm bảo dịch vụ SSH đang hiển thị trạng thái `active (running)`)._

2. **Mở Terminal trên Mac và kết nối:**
   Mở ứng dụng Terminal trên macOS và chạy lệnh:

   ```bash
   ssh raymond@10.211.55.20
   ```

   _(Thay `raymond` bằng tên user và `10.211.55.20` bằng IP thực tế của máy ảo)._

#### Cách 2: Chuyển card mạng sang Bridged Network (Cùng dải mạng LAN với Mac)

Dùng cách này nếu bạn muốn máy ảo nhận IP cùng dải `192.168.2.x` với máy Mac, cho phép các thiết bị khác trong mạng LAN gia đình/văn phòng cũng truy cập được vào máy ảo:

1. **Đổi chế độ mạng:**
   Trên menu Parallels Desktop, vào **Actions** (hoặc biểu tượng bánh răng Cấu hình) $\rightarrow$ **Hardware** $\rightarrow$ **Network**. Đổi từ **Shared Network** sang **Bridged Network** (chọn Wi-Fi hoặc Ethernet tương ứng với mạng Mac đang dùng).
2. **Cập nhật IP mới trên Ubuntu:**
   Trong máy ảo Ubuntu, khởi động lại mạng hoặc chạy lệnh cấp lại IP:

   ```bash
   sudo dhclient -r && sudo dhclient
   ```

   Kiểm tra IP mới bằng lệnh:

   ```bash
   ip a
   ```

   _(Lúc này máy ảo sẽ có IP cùng dải với mạng Mac, ví dụ: `192.168.2.15`)._

3. **Kết nối SSH từ Mac:**

   ```bash
   ssh raymond@192.168.2.15
   ```

### 💡 Lưu ý xử lý lỗi thường gặp khi SSH:

- **Lỗi `Connection refused`:** Dịch vụ SSH chưa chạy trên Ubuntu. Kích hoạt lại bằng lệnh:
  ```bash
  sudo systemctl enable --now ssh
  ```
- **Bị treo `Connection timed out`:** Tường lửa (`ufw`) trên Ubuntu đang chặn cổng 22. Mở cổng bằng lệnh:
  ```bash
  sudo ufw allow ssh
  ```

---
