function saveAuth(token, username) {
  localStorage.setItem("token", token);
  localStorage.setItem("username", username);
}

function getToken() {
  return localStorage.getItem("token");
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  location.href = "index.html";
}

function updateNavAuth() {
  const username = localStorage.getItem("username");
  if (!username || !getToken()) return;

  document.querySelectorAll(".navbar a").forEach((link) => {
    const href = link.getAttribute("href") || "";
    if (link.classList.contains("logo")) return;
    if (!/login/.test(href)) return;

    link.textContent = `👤 ${username} (Logout)`;
    link.setAttribute("href", "#");
    link.onclick = (e) => {
      e.preventDefault();
      logout();
    };
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", updateNavAuth);
} else {
  updateNavAuth();
}
window.addEventListener("pageshow", updateNavAuth);

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  const loginForm = document.getElementById("login-form");

  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = {
        username: document.getElementById("su-username").value,
        email: document.getElementById("su-email").value,
        password: document.getElementById("su-password").value,
      };
      try {
        const res = await fetch(`${BASE_URL}/auth/signup`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Signup failed");
        saveAuth(data.token, data.username);
        location.href = "index.html";
      } catch (err) {
        document.getElementById("auth-error").textContent = err.message;
      }
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = {
        email: document.getElementById("li-email").value,
        password: document.getElementById("li-password").value,
      };
      try {
        const res = await fetch(`${BASE_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Login failed");
        saveAuth(data.token, data.username);
        location.href = "index.html";
      } catch (err) {
        document.getElementById("auth-error").textContent = err.message;
      }
    });
  }
});