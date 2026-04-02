export function CardInfo({ title, items, color = "blue" }) {
  const container = document.createElement("div");
  container.className = `card-info border-l-prime-${color}`;

  const titleEl = document.createElement("div");
  titleEl.className = "heading-3";
  titleEl.textContent = title;

  const ul = document.createElement("ul");
  ul.className = "space-y-4 text-lg text-slate-700";

  items.forEach((item) => {
    const li = document.createElement("li");
    li.className = "list-item";

    li.innerHTML = `
      <span class="${item.iconColor} font-bold">${item.icon}</span>
      <span>${item.content}</span>
    `;

    ul.appendChild(li);
  });

  container.appendChild(titleEl);
  container.appendChild(ul);

  return container;
}