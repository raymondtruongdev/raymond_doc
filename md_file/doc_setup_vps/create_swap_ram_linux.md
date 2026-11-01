# Hướng Dẫn Cấu Hình và Quản Lý Swap Trên Linux VPS

Do máy ảo `e2-micro` chỉ có **1 GB RAM thật**, nếu cài Docker hoặc các ứng dụng nặng máy sẽ bị tràn RAM và sập dịch vụ (Out Of Memory - OOM). Việc tạo **2GB / 4GB Swap RAM** (bộ nhớ ảo trên ổ cứng) là bắt buộc.

Sau hướng dẫn chi tiết cách khởi tạo, cấu hình, tối ưu và gỡ bỏ bộ nhớ ảo (Swap) trên hệ điều hành Linux (Ubuntu, Debian, CentOS, AlmaLinux, Rocky Linux).

Mở terminal SSH vào máy ảo và chạy lần lượt các lệnh sau:

# 1. Kiểm tra Swap hiện có

```bash
sudo swapon --show
free -h
```

_Nếu không có thông số Swap nào xuất hiện hoặc cột `Swap: total` hiển thị `0B`, nghĩa là VPS chưa bật Swap._

# 2. Kiểm tra dung lượng ổ đĩa trống

```bash
df -h /
```

_Đảm bảo dung lượng trống tại phân vùng `/` lớn hơn kích thước Swap dự định tạo ít nhất 2–4 GB._

# 3. Tạo SWAP

## 3.1. Script tạo 2GB Swap

```bash
# 1. Tắt swapfile cũ nếu đang chạy
sudo swapoff /swapfile 2>/dev/null || true

# 2. Phân bổ file swap 2GB (Dùng fallocate, nếu lỗi dùng dd dự phòng)
sudo fallocate -l 2G /swapfile 2>/dev/null || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048 status=progress

# 3. Phân quyền bảo mật (chỉ tài khoản root mới có quyền đọc/ghi)
sudo chmod 600 /swapfile

# 4. Định dạng và kích hoạt vùng Swap
sudo mkswap /swapfile
sudo swapon /swapfile

# 5. Cấu hình tự kích hoạt Swap khi khởi động lại máy ảo
grep -qs "^/swapfile" /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 6. Tối ưu độ ưu tiên RAM (swappiness = 10)
sudo sysctl vm.swappiness=10
grep -qs "^vm.swappiness" /etc/sysctl.conf && sudo sed -i "s/^vm.swappiness=.*/vm.swappiness=10/" /etc/sysctl.conf || echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf

# 7. Kiểm tra lại kết quả
free -h
```

_(Nếu thấy dòng `Swap:` hiển thị dung lượng khoảng `2.0Gi` là đã thành công)._

## 3.2. Script tạo 4GB Swap

```bash
# 1. Tắt swapfile cũ nếu đang chạy
sudo swapoff /swapfile 2>/dev/null || true

# 2. Phân bổ file swap 4GB (Dùng fallocate, nếu lỗi dùng dd dự phòng)
sudo fallocate -l 4G /swapfile 2>/dev/null || sudo dd if=/dev/zero of=/swapfile bs=1M count=4096 status=progress

# 3. Phân quyền bảo mật (chỉ tài khoản root mới có quyền đọc/ghi)
sudo chmod 600 /swapfile

# 4. Định dạng và kích hoạt vùng Swap
sudo mkswap /swapfile
sudo swapon /swapfile

# 5. Cấu hình tự kích hoạt Swap khi khởi động lại máy ảo
grep -qs "^/swapfile" /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 6. Tối ưu độ ưu tiên RAM (swappiness = 10)
sudo sysctl vm.swappiness=10
grep -qs "^vm.swappiness" /etc/sysctl.conf && sudo sed -i "s/^vm.swappiness=.*/vm.swappiness=10/" /etc/sysctl.conf || echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf

# 7. Kiểm tra lại kết quả
free -h
```

_(Nếu thấy dòng `Swap:` hiển thị dung lượng khoảng `2.0Gi` là đã thành công)._

# 4. Hướng Dẫn Gỡ Bỏ Hoàn Toàn Swap (Uninstall / Reset)

Nếu bạn muốn xóa bỏ swap hoặc làm lại từ đầu:

```bash
# 1. Tắt swapfile đang chạy
sudo swapoff /swapfile

# 2. Xóa file swap trên ổ cứng
sudo rm -f /swapfile

# 3. Xóa dòng cấu hình trong /etc/fstab
sudo sed -i '\|^/swapfile|d' /etc/fstab

# 4. (Tùy chọn) Khôi phục giá trị swappiness mặc định (60)
sudo sysctl vm.swappiness=60
sudo sed -i '\|^vm.swappiness|d' /etc/sysctl.conf

# 5. Kiểm tra lại trạng thái
free -h
```

_(Nếu thấy dòng `Swap:` hiển thị dung lượng khoảng `2.0Gi` là đã thành công)._
