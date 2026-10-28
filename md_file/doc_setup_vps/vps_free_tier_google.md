# Hướng Dẫn Chi Tiết Tạo & Cấu Hình Máy Chủ Google Cloud VPS Free Tier (Always Free)

Tài liệu này tổng hợp hướng dẫn đầy đủ, chi tiết và súc tích để tạo máy ảo (Compute Engine) **hoàn toàn miễn phí 100% vĩnh viễn** trên Google Cloud Platform (GCP), tối ưu tốc độ cho người dùng tại Việt Nam, tránh các "bẫy" tính phí ngầm và hướng dẫn cài đặt cơ bản (SSH, Swap RAM, Docker).

---

## 1. Hiểu Rõ Chính Sách "Always Free" Của Google Cloud

Để không bao giờ bị trừ tiền, cấu hình máy ảo bắt buộc phải nằm trong các hạn mức sau:

| Thành phần | Mức miễn phí (Always Free) | Giải thích & Lưu ý quan trọng |
| :--- | :--- | :--- |
| **Loại máy ảo** | **1 instance `e2-micro`** (2 vCPU, 1 GB RAM) | Hạn mức tính theo **tổng số giờ**: ~720–744 giờ/tháng (đủ cho **duy nhất 1 máy** chạy 24/7). Nếu tạo 2 máy chạy song song, số giờ vượt mức sẽ bị tính phí. |
| **Khu vực (Region)** | Chỉ 3 vùng tại Mỹ:<br>• `us-west1` (Oregon)<br>• `us-central1` (Iowa)<br>• `us-east1` (South Carolina) | **Ở Việt Nam, nên chọn `us-west1` (Oregon)** vì nằm ở bờ Tây nước Mỹ, đi cáp quang biển thẳng qua Thái Bình Dương cho độ trễ (ping ~160ms–190ms) thấp nhất. |
| **Ổ cứng (Boot Disk)** | Tối đa **30 GB** loại **Standard Persistent Disk** (`pd-standard`) | • **Tuyệt đối KHÔNG chọn** `Balanced persistent disk` (`pd-balanced`) hay `SSD` (`pd-ssd`) vì sẽ bị tính tiền theo GB hàng tháng.<br>• Mặc định GCP hay gợi ý *Balanced*, cần bấm **Change** để đổi sang *Standard*. |
| **Băng thông (Egress)** | **1 GB/tháng** (chiều gửi ra Internet từ Bắc Mỹ) | • Dữ liệu tải lên máy ảo (Inbound/Ingress) là **miễn phí không giới hạn**.<br>• Dữ liệu gửi ra ngoài chỉ miễn phí 1 GB đầu tiên. Nếu dùng làm web/proxy nhiều lượt tải, phần vượt quá 1 GB sẽ tính phí khoảng $0.085 – $0.12/GB (~2.500đ/GB). |
| **Địa chỉ IP** | **Ephemeral IP (IP động)** | Miễn phí khi máy ảo đang chạy. **Tuyệt đối không tạo Reserved Static IP** (IP tĩnh giữ chỗ khi máy tắt sẽ bị tính phí phạt giữ IP). |

> [!NOTE]
> **Về con số "Monthly estimate: $6.11" khi tạo máy:**  
> Đây chỉ là bảng tính giá niêm yết gốc (List Price) chưa áp dụng khuyến mãi. Cuối tháng, hệ thống tự động áp mã **Free Tier Credit (-$6.11)** đưa hóa đơn thực tế về **$0.00**.

> [!NOTE]
> **Về khoản trừ ~1 USD khi thêm thẻ Visa/Mastercard:**  
> Đây là giao dịch giữ tiền xác minh thẻ (Authorization Hold/Pending). Ngân hàng sẽ **hoàn trả lại 100%** trong 3–30 ngày.

---

## 2. Các Bước Tạo Máy Ảo Chuẩn Free Tier (Chi Tiết Từng Mục)

Truy cập **Google Cloud Console** > vào menu điều hướng chọn **Compute Engine** > **VM instances** > bấm **Create Instance**.

Thiết lập các thông số chính xác theo bảng sau:

### A. Machine Configuration (Cấu hình máy)
* **Name:** Đặt tên tùy ý (ví dụ: `vps-free`).
* **Region:** Chọn **`us-west1 (Oregon)`** (tối ưu nhất cho VN).
* **Zone:** Chọn bất kỳ (`us-west1-a`, `us-west1-b`, hoặc `us-west1-c`).
* **Machine configuration:**
  * **Series:** `E2`
  * **Machine type:** **`e2-micro`** (2 vCPU, 1 GB RAM).

### B. Boot Disk (Ổ đĩa hệ điều hành) — *Bước quan trọng nhất tránh mất tiền*
Bấm nút **Change**:
* **Operating system:** Chọn **Ubuntu**.
  * **Giải thích:** Chọn bản Ubuntu tiêu chuẩn (miễn phí bản quyền). Tuyệt đối **không chọn** *Ubuntu Pro* (tính phí bản quyền theo giờ) hoặc *Ubuntu Accelerator* (chỉ cho máy có GPU).
* **Version:** Chọn **`Ubuntu 24.04 LTS`** hoặc **`Ubuntu 22.04 LTS`** (hoặc bản *Minimal* để hệ thống nhẹ hơn).
* **Boot disk type:** Chuyển sang **Standard persistent disk** *(Bắt buộc, không để Balanced)*.
* **Size:** Nhập **`30 GB`** (hoặc nhỏ hơn).
* Bấm **Select** để lưu.

### C. Backups (Sao lưu)
* Chọn **`No backups`**.
  * **Giải thích:** Tính năng Snapshot Schedule hay Backup Plan lưu dữ liệu lên Cloud Storage và **bị tính phí dung lượng lưu trữ riêng**, không nằm trong Free Tier của máy ảo.

### D. Networking (Mạng)
* **Firewall:**
  * Tích chọn **Allow HTTP traffic** (Cổng 80).
  * Tích chọn **Allow HTTPS traffic** (Cổng 443).
  * *Bỏ chọn* `Allow Load Balancer Health Checks` (không dùng Load Balancer).
* **Network performance:** Để mặc định, **không bật Tier_1**.
* **IP forwarding:** Để mặc định (**Off/Disabled**).
* **Network interfaces:** Giữ nguyên mặc định (Ephemeral external IP).

### E. Security & Identity
* **Service account:** Chọn **Compute Engine default service account**.
* **Access scopes:** Chọn **Allow default access**.
* **Confidential VM service:** **Tắt (Disabled)** (dịch vụ mã hóa RAM này có tính phí và không hỗ trợ trên `e2-micro`).
* **Shielded VM:** Có thể tích bật cả 3 tùy chọn (*Secure Boot*, *vTPM*, *Integrity Monitoring*) — **Miễn phí 100%**.

Sau khi kiểm tra đúng toàn bộ thông số, nhấn **Create** và chờ 1–2 phút để máy ảo khởi động.

---

## 3. Hướng Dẫn Kết Nối SSH Vào Máy Ảo

### Cách 1: Sử dụng Google Cloud SDK (`gcloud` CLI) — Khuyên dùng cho Mac/Linux

1. Cài đặt SDK trên Mac (qua Homebrew):
   ```bash
   brew install --cask google-cloud-sdk
   ```
2. Đăng nhập tài khoản Google:
   ```bash
   gcloud auth login
   ```
3. Đặt ID dự án mặc định:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```
4. Kết nối trực tiếp:
   ```bash
   gcloud compute ssh vps-free --zone=us-west1-b
   ```

---

### Cách 2: Kết nối thủ công bằng SSH Key mặc định qua Terminal

#### Bước 1: Tạo SSH Key trên máy tính
Mở Terminal và gõ:
```bash
ssh-keygen -t rsa -f ~/.ssh/gcp_vps -C "tenuser"
```
*(Thay `tenuser` bằng tên người dùng bạn muốn đặt. Bấm Enter 2 lần để bỏ qua mật khẩu passphrase nếu muốn đăng nhập nhanh).*

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

### Cách 3: SSH trực tiếp trên trình duyệt Web (Nhanh nhất)
Tại danh sách **VM instances**, ở cột ngoài cùng bên phải của máy ảo, chỉ cần bấm nút **SSH**. Một cửa sổ terminal web sẽ tự động mở ra.

---

### Mở rộng: Hướng dẫn cài đặt OpenSSH Server & Kết nối SSH từ Mac vào máy ảo Ubuntu (Parallels / Local VM)

Nếu bạn chạy máy ảo Ubuntu cục bộ trên Mac (ví dụ dùng Parallels Desktop, VMware hoặc VirtualBox) thay vì cloud, bạn có 2 cách chính để kết nối SSH:

#### Cách 1: SSH trực tiếp qua IP mạng NAT (Nhanh nhất & Đơn giản nhất)
Mặc dù khác dải IP (`192.168.2.x` vs `10.211.55.x`), máy Mac vẫn có thể kết nối trực tiếp đến IP `10.211.55.20` vì phần mềm ảo hóa (như Parallels) đã tự động tạo một giao diện mạng ảo (`vnic`) trên macOS.

1. **Cài đặt SSH Server trên máy ảo Ubuntu:**
   Mở terminal trong máy ảo Ubuntu và cài đặt gói `openssh-server`:
   ```bash
   sudo apt update
   sudo apt install -y openssh-server
   sudo systemctl status ssh
   ```
   *(Đảm bảo dịch vụ SSH đang hiển thị trạng thái `active (running)`).*

2. **Mở Terminal trên Mac và kết nối:**
   Mở ứng dụng Terminal trên macOS và chạy lệnh:
   ```bash
   ssh raymond@10.211.55.20
   ```
   *(Thay `raymond` bằng tên user và `10.211.55.20` bằng IP thực tế của máy ảo).*

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
   *(Lúc này máy ảo sẽ có IP cùng dải với mạng Mac, ví dụ: `192.168.2.15`).*
3. **Kết nối SSH từ Mac:**
   ```bash
   ssh raymond@192.168.2.15
   ```

#### 💡 Lưu ý xử lý lỗi thường gặp khi SSH:
* **Lỗi `Connection refused`:** Dịch vụ SSH chưa chạy trên Ubuntu. Kích hoạt lại bằng lệnh:
  ```bash
  sudo systemctl enable --now ssh
  ```
* **Bị treo `Connection timed out`:** Tường lửa (`ufw`) trên Ubuntu đang chặn cổng 22. Mở cổng bằng lệnh:
  ```bash
  sudo ufw allow ssh
  ```

---

## 4. Tối Ưu Hệ Thống: Cấu Hình Swap RAM 2GB (Bắt Buộc)

Do máy ảo `e2-micro` chỉ có **1 GB RAM thật**, nếu cài Docker hoặc các ứng dụng nặng máy sẽ bị tràn RAM và sập dịch vụ (Out Of Memory - OOM). Việc tạo **2GB Swap RAM** (bộ nhớ ảo trên ổ cứng) là bắt buộc.

Mở terminal SSH vào máy ảo và chạy lần lượt các lệnh sau:

```bash
# 1. Tạo file swap 2GB
sudo fallocate -l 2G /swapfile

# (Nếu lệnh trên báo lỗi fallocate failed, chạy lệnh thay thế sau:)
# sudo dd if=/dev/zero of=/swapfile bs=1M count=2048

# 2. Phân quyền bảo mật (chỉ tài khoản root mới có quyền đọc/ghi)
sudo chmod 600 /swapfile

# 3. Định dạng và kích hoạt Swap
sudo mkswap /swapfile
sudo swapon /swapfile

# 4. Lưu cấu hình để tự bật Swap khi khởi động lại máy ảo
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 5. Tối ưu Swappiness (giá trị 10 giúp ưu tiên dùng RAM thật trước, khi đầy mới đẩy sang Swap)
sudo sysctl vm.swappiness=10
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf

# 6. Kiểm tra lại kết quả
free -h
```
*(Nếu thấy dòng `Swap:` hiển thị dung lượng khoảng `2.0Gi` là đã thành công).*

---

## 5. Cài Đặt Docker & Docker Compose (Tùy chọn)

Để triển khai các ứng dụng container hóa tiện lợi và an toàn:

```bash
# Cập nhật danh sách gói hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt Docker & Docker Compose Plugin chuẩn
sudo apt install -y ca-certificates curl gnupg lsb-release docker.io docker-compose-v2

# Cho phép user hiện tại dùng Docker không cần gõ 'sudo'
sudo usermod -aG docker $USER
newgrp docker

# Kiểm tra phiên bản hoạt động
docker --version
docker compose version
```

---

## 6. Checklist Kiểm Tra Cuối Cùng (Tránh Phát Sinh Tiền)

Trước khi an tâm sử dụng, hãy vào **GCP Console > Billing > Reports** định kỳ để kiểm tra:

- [ ] Chỉ duy nhất **1 máy ảo `e2-micro`** đang chạy.
- [ ] Khu vực máy ảo thuộc: `us-west1`, `us-central1` hoặc `us-east1`.
- [ ] Loại ổ đĩa là **Standard Persistent Disk**, dung lượng $\le$ **30 GB**.
- [ ] Mục **Snapshots / Backups** không có bản sao lưu tự động nào đang chạy.
- [ ] Không tạo **External Static IP** bị bỏ trống (chỉ dùng Ephemeral IP đi kèm máy đang chạy).
- [ ] Đặt **Budget & Alert** ở mức **$1.00** trong trang Billing để nhận email cảnh báo tức thì nếu có bất kỳ chi phí ngoài ý muốn nào phát sinh.
