# Hướng Dẫn Chi Tiết Tạo & Cấu Hình Máy Chủ Google Cloud VPS Free Tier (Always Free)

Tài liệu này tổng hợp hướng dẫn đầy đủ, chi tiết và súc tích để tạo máy ảo (Compute Engine) **hoàn toàn miễn phí 100% vĩnh viễn** trên Google Cloud Platform (GCP), tối ưu tốc độ cho người dùng tại Việt Nam, tránh các "bẫy" tính phí ngầm và hướng dẫn cài đặt cơ bản (SSH, Swap RAM, Docker).

---

## 1. Hiểu Rõ Chính Sách "Always Free" Của Google Cloud

Để không bao giờ bị trừ tiền, cấu hình máy ảo bắt buộc phải nằm trong các hạn mức sau:

| Thành phần              | Mức miễn phí (Always Free)                                                                                   | Giải thích & Lưu ý quan trọng                                                                                                                                                                                                                  |
| :---------------------- | :----------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Loại máy ảo**         | **1 instance `e2-micro`** (2 vCPU, 1 GB RAM)                                                                 | Hạn mức tính theo**tổng số giờ**: ~720–744 giờ/tháng (đủ cho **duy nhất 1 máy** chạy 24/7). Nếu tạo 2 máy chạy song song, số giờ vượt mức sẽ bị tính phí.                                                                                      |
| **Khu vực (Region)**    | Chỉ 3 vùng tại Mỹ:`<br>`• `us-west1` (Oregon)`<br>`• `us-central1` (Iowa)`<br>`• `us-east1` (South Carolina) | **Ở Việt Nam, nên chọn `us-west1` (Oregon)** vì nằm ở bờ Tây nước Mỹ, đi cáp quang biển thẳng qua Thái Bình Dương cho độ trễ (ping ~160ms–190ms) thấp nhất.                                                                                    |
| **Ổ cứng (Boot Disk)**  | Tối đa**30 GB** loại **Standard Persistent Disk** (`pd-standard`)                                            | •**Tuyệt đối KHÔNG chọn** `Balanced persistent disk` (`pd-balanced`) hay `SSD` (`pd-ssd`) vì sẽ bị tính tiền theo GB hàng tháng.`<br>`• Mặc định GCP hay gợi ý _Balanced_, cần bấm **Change** để đổi sang _Standard_.                          |
| **Băng thông (Egress)** | **1 GB/tháng** (chiều gửi ra Internet từ Bắc Mỹ)                                                             | • Dữ liệu tải lên máy ảo (Inbound/Ingress) là**miễn phí không giới hạn**.`<br>`• Dữ liệu gửi ra ngoài chỉ miễn phí 1 GB đầu tiên. Nếu dùng làm web/proxy nhiều lượt tải, phần vượt quá 1 GB sẽ tính phí khoảng $0.085 – $0.12/GB (~2.500đ/GB). |
| **Địa chỉ IP**          | **Ephemeral IP (IP động)**                                                                                   | Miễn phí khi máy ảo đang chạy.**Tuyệt đối không tạo Reserved Static IP** (IP tĩnh giữ chỗ khi máy tắt sẽ bị tính phí phạt giữ IP).                                                                                                             |

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

- **Name:** Đặt tên tùy ý (ví dụ: `vps-free`).
- **Region:** Chọn **`us-west1 (Oregon)`** (tối ưu nhất cho VN).
- **Zone:** Chọn bất kỳ (`us-west1-a`, `us-west1-b`, hoặc `us-west1-c`).
- **Machine configuration:**
  - **Series:** `E2`
  - **Machine type:** **`e2-micro`** (2 vCPU, 1 GB RAM).

### B. Boot Disk (Ổ đĩa hệ điều hành) — _Bước quan trọng nhất tránh mất tiền_

Bấm nút **Change**:

- **Operating system:** Chọn **Ubuntu**.
  - **Giải thích:** Chọn bản Ubuntu tiêu chuẩn (miễn phí bản quyền). Tuyệt đối **không chọn** _Ubuntu Pro_ (tính phí bản quyền theo giờ) hoặc _Ubuntu Accelerator_ (chỉ cho máy có GPU).
- **Version:** Chọn **`Ubuntu 24.04 LTS`** hoặc **`Ubuntu 22.04 LTS`** (hoặc bản _Minimal_ để hệ thống nhẹ hơn).
- **Boot disk type:** Chuyển sang **Standard persistent disk** _(Bắt buộc, không để Balanced)_.
- **Size:** Nhập **`30 GB`** (hoặc nhỏ hơn).
- Bấm **Select** để lưu.

### C. Backups (Sao lưu)

- Chọn **`No backups`**.
  - **Giải thích:** Tính năng Snapshot Schedule hay Backup Plan lưu dữ liệu lên Cloud Storage và **bị tính phí dung lượng lưu trữ riêng**, không nằm trong Free Tier của máy ảo.

### D. Networking (Mạng)

- **Firewall:**
  - Tích chọn **Allow HTTP traffic** (Cổng 80).
  - Tích chọn **Allow HTTPS traffic** (Cổng 443).
  - _Bỏ chọn_ `Allow Load Balancer Health Checks` (không dùng Load Balancer).
- **Network performance:** Để mặc định, **không bật Tier_1**.
- **IP forwarding:** Để mặc định (**Off/Disabled**).
- **Network interfaces:** Giữ nguyên mặc định (Ephemeral external IP).

### E. Security & Identity

- **Service account:** Chọn **Compute Engine default service account**.
- **Access scopes:** Chọn **Allow default access**.
- **Confidential VM service:** **Tắt (Disabled)** (dịch vụ mã hóa RAM này có tính phí và không hỗ trợ trên `e2-micro`).
- **Shielded VM:** Có thể tích bật cả 3 tùy chọn (_Secure Boot_, _vTPM_, _Integrity Monitoring_) — **Miễn phí 100%**.

Sau khi kiểm tra đúng toàn bộ thông số, nhấn **Create** và chờ 1–2 phút để máy ảo khởi động.

---

## 3. Hướng Dẫn Kết Nối SSH Vào Máy Ảo Google VPS

[Click here view Hướng dẫn kết nối với máy Goolge VPS ](./connect_linux_machine.md)

## 4. Tối Ưu Hệ Thống: Cấu Hình Swap RAM (Bắt buột cho máy VPS có Ram 1GB)

[Click here view Setup Swap RAM](./create_swap_ram_linux.md)

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
