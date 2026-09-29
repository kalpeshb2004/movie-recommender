
async function loadSearch() {
  const q = getParam("q") || "";
  document.getElementById("search-input").value = q;
  document.getElementById("search-title").textContent = `Results for "${q}"`;

  try {
    const results = await apiGet(`/movies/search?q=${encodeURIComponent(q)}`);
    document.getElementById("search-results").innerHTML =
      results.length ? results.map(posterCard).join("") : "<p>No movies found.</p>";

    if (results.length) {
      const top = results[0];
      const similar = await apiGet(`/movies/${top.id}/recommend?limit=10`);
      document.getElementById("because-title").textContent =
        `Because you searched "${top.title}"`;
      document.getElementById("because-row").innerHTML = similar.map(posterCard).join("");
    }
  } catch (e) {
    console.error(e);
  }
}
loadSearch();