export function CodeBlock({ code, language = "cpp" }) {
  const el = document.createElement("figure");
  el.className = `code-block`;

  const pre = document.createElement("pre");
  const codeEl = document.createElement("code");

  codeEl.className = `language-${language} h-full`;
  codeEl.textContent = code.trim();

  pre.appendChild(codeEl);
  el.appendChild(pre);

  // highlight ngay sau khi render
  if (window.hljs) {
    hljs.highlightElement(codeEl);
  }

  return el;
}