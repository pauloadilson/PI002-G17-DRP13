document.addEventListener("DOMContentLoaded", (event) => {
  const themeToggleBtn = document.getElementById("themeToggleBtn");
  const body = document.body;

  function toggleTheme() {
    const currentTheme = body.getAttribute("data-bs-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    body.setAttribute("data-bs-theme", newTheme);
  }

  themeToggleBtn.addEventListener("click", toggleTheme);
});
