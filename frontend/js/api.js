const BASE_URL = "https://movie-recommender-api-cutb.onrender.com";

function getParam(name) {
  return new URLSearchParams(location.search).get(name);
}

async function apiGet(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

function posterCard(movie) {
  const img = movie.poster_url
    ? `<img src="${movie.poster_url}" alt="${movie.title}">`
    : `<div class="placeholder-poster">${movie.title}</div>`;
  return `
    <div class="card" onclick="location.href='movie.html?id=${movie.id}'">
      ${img}
      <div class="rating">★ ${movie.vote_average?.toFixed(1) ?? "-"}</div>
      <div class="title">${movie.title}</div>
    </div>`;
}

function showError(elementId, msg = "Something went wrong. Try again.") {
  const el = document.getElementById(elementId);
  if (el) el.innerHTML = `<p style="color:#999;padding:20px;">${msg}</p>`;
}