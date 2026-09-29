function saveAuth(token, username) {
  sessionStorage.setItem("token", token);
  sessionStorage.setItem("username", username);
}

function getToken() {
  return sessionStorage.getItem("token");
}

function updateNavAuth() {
  const username = sessionStorage.getItem("username");
  const loginLink = document.querySelector('a[href="login.html"]');
  if (username && loginLink) {
    loginLink.textContent = `${username} (Logout)`;
    loginLink.href = "#";
    loginLink.onclick = (e) => {
      e.preventDefault();
      sessionStorage.clear();
      location.href = "index.html";
    };
  }
}
document.addEventListener("DOMContentLoaded", updateNavAuth);

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