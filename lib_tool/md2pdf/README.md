# Markdown to PDF Tool (A4 Clean Print)

Tool chuyển đổi Markdown sang PDF chuẩn A4, hỗ trợ:

- Sơ đồ **Mermaid** & **PlantUML** (vector SVG sắc nét).
- Các hộp thoại Alert GitHub (`[!NOTE]`, `[!TIP]`, `[!IMPORTANT]`, `[!WARNING]`, `[!CAUTION]`).
- Dark theme cho code block (có nhận diện lệnh Shell/Bash).
- Bảng biểu (Tables), Badges, Highlight (`<mark>`), chống rách trang giữa chừng (`break-inside: avoid`).
- Support HTM to break page PDF (`<div style="page-break-after: always; break-after: page;"></div>`)

---

## 🚀 Cách sử dụng

### 1. Phím tắt trong Antigravity / VS Code:

Mở bất kỳ file `.md` nào $\rightarrow$ nhấn **`Cmd + Shift + B`** (hoặc `Terminal` $\rightarrow$ `Run Task...` $\rightarrow$ `Export current Markdown to PDF`).

### 2. Dòng lệnh Terminal:

```bash
./lib_tool/md2pdf/md2pdf.sh "path/to/document.md"
```

---

## 📦 Mang sang Repo khác:

1. Copy cả thư mục `lib_tool/md2pdf` này vào repo mới.
2. Thêm task vào file `.vscode/tasks.json` của repo mới:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Export current Markdown to PDF",
      "type": "shell",
      "command": "${workspaceFolder}/lib_tool/md2pdf/md2pdf.sh \"${file}\"",
      "group": { "kind": "build", "isDefault": true }
    }
  ]
}
```
