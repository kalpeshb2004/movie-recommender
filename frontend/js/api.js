const BASE_URL = "http://127.0.0.1:8000";

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