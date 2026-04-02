export function CardInfo({ title, items, color = "blue" }) {
  const container = document.createElement("div");

  // ✅ self-start để luôn nằm top (quan trọng)
  // container.className = `card-info h-full self-start mb-5 border-l-prime-${color} px-5 py-3`;

container.className = `
  card-info 
  h-full 
  flex flex-col 
  justify-start
  border-l-prime-${color} 
  px-5 py-3
`;

  // Title
  const titleEl = document.createElement("div");
  titleEl.className = "heading-3 mb-2";
  titleEl.textContent = title;

  // List
  const ul = document.createElement("ul");
  ul.className = "space-y-2 text-slate-700 text-justify";

  items.forEach((item) => {
    const li = document.createElement("li");

    // ✅ flex + top align
    li.className = "list-item flex items-start";

    li.innerHTML = `
      <span class="${item.iconColor} font-bold shrink-0 mr-1 leading-none">
        ${item.icon}
      </span>
      <span class="flex-1 leading-relaxed">
        ${item.content}
      </span>
    `;

    ul.appendChild(li);
  });

  container.appendChild(titleEl);
  container.appendChild(ul);

  return container;
}