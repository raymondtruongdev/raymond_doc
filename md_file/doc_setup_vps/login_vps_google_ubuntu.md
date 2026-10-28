# Hướng Dẫn Đăng Nhập Tài Khoản User Trên VPS Ubuntu (Google Cloud)

Tài liệu này hướng dẫn chi tiết các phương thức đăng nhập và xác thực user trên VPS Ubuntu (Google Cloud Compute Engine), bao gồm giải thích cơ chế hoạt động và cách cấu hình tối ưu.

---

## 1. Cơ Chế Xác Thực Trên VPS Linux

- **Không có GUI tự đăng nhập**: VPS chạy ở chế độ headless (không màn hình, không giao diện đồ họa). Sau khi khởi động, hệ thống lắng nghe kết nối từ xa qua SSH (cổng 22 mặc định) hoặc Serial Console.
- **Mật khẩu (Password) vs SSH Key**:
  - **Password**: Dễ nhớ nhưng dễ bị tấn công brute-force; mặc định Google Cloud vô hiệu hóa đăng nhập bằng password qua SSH để bảo mật.
  - **SSH Key (Khuyên dùng)**: Sử dụng cặp khóa mã hóa bất đối xứng (_Private Key_ giữ ở máy cá nhân, _Public Key_ đặt trên VPS). An toàn tuyệt đối và đăng nhập không cần gõ mật khẩu.
- **Tài khoản mặc định trên GCP**: Tùy theo cách tạo máy hoặc tài khoản Google, user thường được tạo theo username Google (`tên_email`) hoặc chỉ định khi add SSH Key.

---

## 2. Cách 1: Đăng Nhập Nhanh Qua Trình Duyệt (GCP Cloud Console)

Dành cho trường hợp cần truy cập khẩn cấp hoặc chưa cấu hình SSH Key trên máy cá nhân.

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/) -> **Compute Engine** -> **VM instances**.
2. Tại dòng của máy ảo Ubuntu, nhấn nút **SSH** ở cột _Connect_.
3. **Giải thích**: Google Cloud tự động tạo cặp key tạm thời, đẩy public key vào metadata của VM và mở một terminal trực tiếp ngay trên trình duyệt với user mặc định của bạn.

---

## 3. Cách 2: Đăng Nhập Bằng SSH Key Từ Máy Cá Nhân (Chuẩn & Tiện Lợi Nhất)

### Bước 1: Tạo cặp SSH Key trên máy tính cá nhân (Mac/Linux/Windows)

Mở Terminal (hoặc PowerShell) trên máy bạn:

```bash
ssh-keygen -t ed25519 -C "your_email@gmail.com"
```

- Nhấn `Enter` để chọn đường dẫn mặc định (`~/.ssh/id_ed25519`).
- Có thể đặt mật khẩu bảo vệ key (passphrase) hoặc để trống (`Enter` 2 lần).

### Bước 2: Thêm Public Key vào VPS Google Cloud

Có 2 cách thực hiện:

#### Lựa chọn A: Thêm qua GCP Console (Áp dụng toàn diện, tự tạo user nếu chưa có)

1. Lấy nội dung public key trên máy bạn:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Vào GCP Console -> **Compute Engine** -> **VM instances** -> Nhấn vào tên VM -> **Edit**.
3. Cuộn xuống mục **SSH Keys** -> Nhấn **Add Item**.
4. Dán public key vào. Định dạng thường là:

   ```text
   ssh-ed25519 AAAA... your-username
   ```

   _(Bạn có thể sửa `your-username` ở cuối thành tên user bạn muốn dùng)._

5. Nhấn **Save**. GCP sẽ tự tạo user và thư mục home trên Ubuntu nếu chưa tồn tại.

#### Lựa chọn B: Thêm trực tiếp trên VPS

Nếu bạn đã SSH được vào VPS (qua Console):

```bash
mkdir -p ~/.ssh && chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
# Dán public key vào file, sau đó phân quyền:
chmod 600 ~/.ssh/authorized_keys
```

### Bước 3: Cấu hình SSH Config để đăng nhập 1 lệnh (Alias)

Trên máy cá nhân, chỉnh sửa hoặc tạo file `~/.ssh/config`:

```text
Host my-vps
    HostName <IP_PUBLIC_CUA_VPS>
    User <your-username>
    IdentityFile ~/.ssh/id_ed25519
```

### Bước 4: Đăng nhập

Bây giờ bạn chỉ cần gõ:

```bash
ssh my-vps
```

> **Giải thích**: SSH client sẽ tự đọc cấu hình, dùng khóa `id_ed25519` để đối chiếu với `authorized_keys` trên VPS của user `<your-username>` và xác thực phiên làm việc tức thì.

---

## 4. Cách 3: Bật Đăng Nhập Bằng Mật Khẩu (Password Authentication)

> [!WARNING]
> Không khuyến khích cho môi trường production vì nguy cơ bị scan và dò quét mật khẩu (brute-force).

Nếu bạn vẫn cần dùng user + mật khẩu:

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

4. **Đăng nhập từ máy cá nhân**:

   ```bash
   ssh <your-username>@<IP_PUBLIC_CUA_VPS>
   # Hệ thống sẽ yêu cầu nhập mật khẩu vừa đặt
   ```

---

## 5. Mở Rộng: Các Nhu Cầu Tự Động Hóa Khác

### Chuyển đổi giữa các user sau khi đăng nhập:

```bash
# Đổi sang user khác:
su - <other-username>

# Chuyển hẳn sang quyền root:
sudo -i
```
