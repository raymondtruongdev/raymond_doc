export function AlertBox({ title, content, type = "red" }) {
  const el = document.createElement("aside");

  // map màu (có thể mở rộng sau)
  const styles = {
    red: {
      bg: "bg-red-50",
      border: "border-red-500",
      text: "text-red-800",
    },
    blue: {
      bg: "bg-blue-50",
      border: "border-blue-500",
      text: "text-blue-800",
    },
    green: {
      bg: "bg-green-50",
      border: "border-green-500",
      text: "text-green-800",
    },
  };

  const s = styles[type] || styles.red;

  el.className = `${s.bg} border-l-4 ${s.border} p-6 mb-5 rounded-r-2xl`;

  el.innerHTML = `
    <p class="text-lg ${s.text} font-medium">
      <span class="font-bold">⚠️ ${title}:</span> ${content}
    </p>
  `;

  return el;
}