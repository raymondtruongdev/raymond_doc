export function TextIconItem({ icon= "", iconColor = "text-blue-600", content }) {
  const el = document.createElement("div");

  el.className = "flex gap-2 text-lg text-slate-700";

  el.innerHTML = `
    <span class="${iconColor} font-bold shrink-0">${icon}</span>
    <span class="flex-1 text-justify">${content}</span>
  `;

  return el;
}