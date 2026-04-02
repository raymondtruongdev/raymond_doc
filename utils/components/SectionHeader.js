export function SectionHeader({ number, content, color = "emerald" }) {
  const el = document.createElement("div");

  el.className = "flex items-center mb-4 group";

  el.innerHTML = `
    <div class="text-white p-4 rounded-2xl mr-5 shadow-xl 
      group-hover:scale-110 transition-transform
      bg-${color}-600 shadow-${color}-200 
      w-12 h-12 flex items-center justify-center">
      
      <span class="font-bold text-3xl">${number}</span>
    </div>

    <h2>${content}</h2>
  `;

  return el;
}