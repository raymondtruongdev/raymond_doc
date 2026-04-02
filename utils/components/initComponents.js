import { CardInfo } from "./CardInfo.js";
import { AlertBox } from "./AlertBox.js";
import { SectionHeader } from "./SectionHeader.js";
import { CodeBlock } from "./CodeBlock.js";
import { TextIconItem } from "./TextIconItem.js";

// helper tránh crash JSON
function safeParse(str, fallback = []) {
  try {
    return JSON.parse(str);
  } catch {
    return fallback;
  }
}

// mount generic
function mount(tagName, component, mapProps) {
  document.querySelectorAll(tagName).forEach((el) => {
    const props = mapProps(el);
    const node = component(props);
    el.replaceWith(node);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  // ===== CardInfo =====
  mount("card-info", CardInfo, (el) => ({
    title: el.getAttribute("title"),
    color: el.getAttribute("color"),
    items: el.getAttribute("items") ? safeParse(el.getAttribute("items")) : [],
  }));

  // ===== AlertBox =====
  mount("alert-box", AlertBox, (el) => ({
    title: el.getAttribute("title"),
    type: el.getAttribute("type") || "red",
    content: el.innerHTML || el.getAttribute("content") || "",
  }));

  // ===== SectionHeader =====
  mount("section-header", SectionHeader, (el) => ({
    number: el.getAttribute("number"),
    content: el.innerHTML || el.getAttribute("content") || "",
    color: el.getAttribute("color") || "emerald",
  }));

  // ===== CodeBlock =====
  mount("code-block", CodeBlock, (el) => ({
    language: el.getAttribute("language") || "cpp",
    code: el.textContent, // 👈 lấy nội dung bên trong
  }));
  // ===== TextIconItem =====
  mount("text-icon-item", TextIconItem, (el) => ({
    icon: el.getAttribute("icon") || "",
    iconColor: el.getAttribute("iconColor"),
    content: el.innerHTML || el.getAttribute("content") || "",
  }));

});
