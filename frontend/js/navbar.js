document.addEventListener("DOMContentLoaded", () => {
  const nav = document.querySelector(".navbar");
  window.addEventListener("scroll", () => {
    nav.classList.toggle("scrolled", window.scrollY > 50);
  });

  const form = document.getElementById("search-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const q = document.getElementById("search-input").value.trim();
      if (q) location.href = `search.html?q=${encodeURIComponent(q)}`;
    });
  }
});