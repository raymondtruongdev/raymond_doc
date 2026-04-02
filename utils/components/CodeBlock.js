// Tự động inject CSS vào trang
const style = document.createElement('style');
style.textContent = `
  .code-block-wrapper {
    position: relative;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
    background-color: #f9fafb;
    margin-bottom: 1.5rem;
  }
  .code-container {
    transition: max-height 0.3s ease-in-out;
    overflow: auto; /* Hiển thị thanh cuộn khi cần */
    position: relative;
  }
  .code-toolbar {
    position: absolute;
    top: 8px;
    right: 16px; /* Cách ra một chút để không đè lên thanh cuộn đứng */
    display: flex;
    gap: 6px;
    z-index: 20;
    opacity: 0;
    transition: opacity 0.2s;
  }
  .code-block-wrapper:hover .code-toolbar {
    opacity: 1;
  }
  .code-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 6px;
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    cursor: pointer;
    color: #4b5563;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
  }
  .code-btn:hover {
    background: #f3f4f6;
    color: #111827;
  }
  .code-btn svg { width: 16px; height: 16px; }
  pre { margin: 0 !important; }
  code { 
    display: block; 
    padding: 1.5rem !important;
    font-family: 'Fira Code', monospace; 
    font-size: 0.9rem !important; 
    line-height: 1.5;
  }
`;
document.head.appendChild(style);

export function CodeBlock({ code, language = "cpp" }) {
  const wrapper = document.createElement("figure");
  wrapper.className = "code-block-wrapper";

  // --- Toolbar ---
  const toolbar = document.createElement("div");
  toolbar.className = "code-toolbar";

  const expandBtn = document.createElement("button");
  expandBtn.className = "code-btn";
  expandBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m7 15 5 5 5-5"/><path d="m7 9 5-5 5 5"/></svg>`;

  const copyBtn = document.createElement("button");
  copyBtn.className = "code-btn";
  copyBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>`;

  toolbar.append(expandBtn, copyBtn);

  // --- Container chứa Code ---
  const container = document.createElement("div");
  container.className = "code-container";
  const MAX_HEIGHT = "200px";
  container.style.maxHeight = MAX_HEIGHT;

  const pre = document.createElement("pre");
  const codeEl = document.createElement("code");
  codeEl.className = `language-${language}`;
  codeEl.textContent = code.trim();

  pre.appendChild(codeEl);
  container.appendChild(pre);

  // --- Logic ---

  // Copy code
  copyBtn.onclick = () => {
    navigator.clipboard.writeText(code.trim()).then(() => {
      const oldIcon = copyBtn.innerHTML;
      copyBtn.innerHTML = `<span style="font-size: 10px; font-weight: bold; color: #059669;">OK!</span>`;
      setTimeout(() => copyBtn.innerHTML = oldIcon, 2000);
    });
  };

  // Toggle Bung/Xổ
  let isExpanded = false;
  expandBtn.onclick = () => {
    isExpanded = !isExpanded;
    if (isExpanded) {
      container.style.maxHeight = "none"; // Bỏ giới hạn để xem hết
      expandBtn.style.backgroundColor = "#e5e7eb"; // Đổi màu nhẹ để báo đang mở
    } else {
      container.style.maxHeight = MAX_HEIGHT;
      expandBtn.style.backgroundColor = "white";
    }
  };

  wrapper.append(toolbar, container);

  if (window.hljs) {
    hljs.highlightElement(codeEl);
  }

  return wrapper;
}