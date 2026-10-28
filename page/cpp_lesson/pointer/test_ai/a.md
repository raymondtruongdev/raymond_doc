# Chuyên đề: Con trỏ trong C/C++ - Từ cơ bản đến nâng cao

**C & C++ Programming**

Tìm hiểu cách máy tính quản lý bộ nhớ, cách khai báo, giải tham chiếu và các kỹ thuật truyền tham số thông qua sơ đồ minh họa trực quan.

---

## 1. Giới thiệu về Con trỏ (Pointer)

Trong lập trình C/C++, **Con trỏ (Pointer)** là một trong những khái niệm mạnh mẽ nhất nhưng cũng dễ gây nhầm lẫn nhất. Hiểu về con trỏ chính là hiểu cách máy tính quản lý bộ nhớ.

> 💡 "Con trỏ không phải là một giá trị thông thường, nó là một biến lưu trữ **địa chỉ** của một ô nhớ khác."

### Hình dung đơn giản
Hãy tưởng tượng **bộ nhớ là một dãy tủ có khóa**. Biến `int a` là một ngăn tủ có nhãn `a` chứa số 5. Con trỏ `int *p` là một mảnh giấy ghi `"số tủ: 0x1000"` — nó không chứa số 5, mà chỉ ghi **địa chỉ của ngăn tủ** chứa số 5.

---

## 2. Biến và Bộ nhớ (Variable & Memory)

Mỗi khi bạn khai báo một biến (ví dụ: `int a = 5;`), máy tính sẽ dành riêng một khoảng không gian trong bộ nhớ (RAM) để lưu trữ giá trị đó. Mỗi khoảng không gian này có một "số nhà" duy nhất, gọi là **địa chỉ (Address)**.

### Các vùng nhớ chính
Bộ nhớ RAM cho một ứng dụng đang chạy thông thường được phân thành các vùng nhớ:

1. **Stack Memory**: Dùng để lưu trữ các biến cục bộ, tham số hàm. Tự động cấp phát và giải phóng khi hàm kết thúc.
2. **Heap Memory**: Dùng cho cấp phát động (`malloc`/`new`). Người lập trình phải tự quản lý (cấp phát và giải phóng thủ công).

### Sơ đồ bộ nhớ RAM (Memory Layout)

```mermaid
graph TD
    subgraph Memory_Layout [Sơ đồ Phân phối Bộ nhớ]
    direction TB
    subgraph Stack [Vùng nhớ Stack]
    S1[Biến cục bộ: a = 5]
    S2[Biến cục bộ: b = 10]
    end
    subgraph Heap [Vùng nhớ Heap]
    H1[Cấp phát động: malloc]
    H2[Cấp phát động: new]
    end
    subgraph Static_Global [Vùng Static / Global]
    G1[Biến toàn cục]
    end
    end
    style Memory_Layout fill:none,stroke:#58a6ff,stroke-width:2px;
    style Stack fill:rgba(88,166,255,0.1),stroke:#58a6ff,stroke-width:1px,color:#e6edf3;
    style Heap fill:rgba(210,168,255,0.1),stroke:#d2a8ff,stroke-width:1px,color:#e6edf3;
    style Static_Global fill:rgba(63,185,80,0.1),stroke:#3fb950,stroke-width:1px,color:#e6edf3;
    classDef default font-family:'Roboto',sans-serif,font-size:12px;
```

### Phân loại các vùng nhớ chính

| Vùng nhớ | Đặc điểm | Quản lý |
| :--- | :--- | :--- |
| **Stack** | Biến cục bộ, tham số hàm. Kích thước nhỏ (~8MB). | Tự động — cấp phát/giải phóng theo hàm. |
| **Heap** | Dữ liệu cấp phát động. Kích thước lớn. | Thủ công — dùng `malloc()` và `free()`. |
| **Data Segment** | Lưu biến global, biến static. | Tự động — tồn tại suốt vòng đời chương trình. |
| **Code Segment** | Chứa mã máy (instructions) của chương trình. | Chỉ đọc, cố định. |

---

## 3. Khái niệm cơ bản về Pointer

Để làm việc với con trỏ, bạn cần nắm vững hai toán tử quan trọng nhất:

### Toán tử quan trọng

| Toán tử | Tên gọi | Ý nghĩa |
| :--- | :--- | :--- |
| `&` | Toán tử lấy địa chỉ (Address-of) | Trả về địa chỉ của biến. |
| `*` | Toán tử giải tham chiếu (Dereference) | Truy cập vào giá trị tại địa chỉ mà con trỏ đang trỏ tới. |

### Cách nhớ
1. `&a` $\rightarrow$ "Địa chỉ của a" (address-of a)
2. `*p` $\rightarrow$ "Giá trị tại địa chỉ p" (value-at-address p)

### Ví dụ minh họa
```c
#include <stdio.h>

int main() {
    int a = 5;
    int *p = &a; // p lưu địa chỉ của a

    printf("Gia tri cua a: %d\n", a);          // 5
    printf("Dia chi cua a (&a): %p\n", &a);    // Ví dụ: 0x7ffe...
    printf("Gia tri cua p: %p\n", p);          // Giống &a
    printf("Gia tri p tro toi (*p): %d\n", *p); // 5

    *p = 10; // Thay đổi giá trị tại địa chỉ p trỏ tới
    printf("Gia tri moi cua a: %d\n", a);      // 10

    return 0;
}
```

### Minh họa bộ nhớ
- **a**: $\longrightarrow$ [5] $\leftarrow$ Biến a tại địa chỉ 0x1000
- **p**: $\longrightarrow$ [0x1000] $\leftarrow$ p chứa địa chỉ của a (trỏ tới a)

### Bảng quy đổi `p + 1` tăng bao nhiêu byte?

| Kiểu dữ liệu | `sizeof` | `p + 1` tăng (bytes) |
| :--- | :--- | :--- |
| `char *` | 1 byte | +1 byte |
| `short *` | 2 bytes | +2 bytes |
| `int *` | 4 bytes | +4 bytes |
| `double *` | 8 bytes | +8 bytes |

---

## 4. Cách khai báo Pointer

Trong C/C++, có nhiều cách viết để khai báo một con trỏ, tất cả đều có ý nghĩa như nhau:
- `int* p;` — Style C++, nhấn mạnh kiểu dữ liệu là con trỏ int.
- `int *p;` — Style C truyền thống, nhấn mạnh `p` là một biến trỏ.
- `int * p;` — Khoảng trắng hai bên, ít dùng.

> ⚠️ **Cảnh báo: Sự khác biệt quan trọng**
> Khi khai báo nhiều biến trên một dòng, hãy cẩn thận:

```c
int* p1, p2; // SAI LẦM PHỔ BIẾN!
// p1 là con trỏ (int*), nhưng p2 chỉ là một số nguyên (int) thông thường.

int *p1, *p2; // ĐÚNG: Cả p1 và p2 đều là con trỏ.
```

### Minh họa bộ nhớ sau khai báo lỗi
1. **p1**: kiểu `int*` $\rightarrow$ Là con trỏ lưu địa chỉ
2. **p2**: kiểu `int` $\rightarrow$ Chỉ là biến `int` bình thường!

---

## 5. Pass By Value vs Pass By Address

### A. Pass By Value (Truyền tham trị)
Trong C, mặc định mọi tham số được truyền theo **giá trị**. Hàm nhận được một **bản sao** của biến gốc.

> ℹ️ **Lưu ý:** Phần này trong nguồn gốc còn tiếp tục ở các dòng sau 400, nên bản Markdown này chỉ phản ánh đúng phần nội dung có trong đoạn trích 1-400.