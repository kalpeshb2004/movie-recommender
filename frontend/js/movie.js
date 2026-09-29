async function loadMovie() {
  const id = getParam("id");
  try {
    const m = await apiGet(`/movies/${id}`);

    document.getElementById("backdrop").style.backgroundImage =
      `url('${m.backdrop_url || m.poster_url || ""}')`;
    document.getElementById("poster").src = m.poster_url || "";
    document.getElementById("title").textContent = m.title;
    document.getElementById("meta").textContent =
      `${(m.release_date || "").slice(0, 4)} • ${(m.genres || "").split(",").join(", ")} • ★ ${m.vote_average}`;
    document.getElementById("overview").textContent = m.overview || "No overview available.";
    document.getElementById("cast").textContent = `Cast: ${m.cast_names || "N/A"}`;
    document.getElementById("director").textContent = `Director: ${m.director || "N/A"}`;

    document.getElementById("trailer-search").href =
      `https://www.youtube.com/results?search_query=${encodeURIComponent(m.title + " trailer")}`;

    document.getElementById("watchlist-btn")?.addEventListener("click", async () => {
        const token = getToken();
        const id = getParam("id");
        if (!token) { location.href = "login.html"; return; }
        await fetch(`${BASE_URL}/watchlist/${id}`, {
            method: "POST",
            headers: { Authorization: `Bearer ${token}` },
        });
        document.getElementById("watchlist-btn").textContent = "✓ Added to Watchlist";
    });

    const similar = await apiGet(`/movies/${id}/recommend?limit=10`);
    document.getElementById("similar-row").innerHTML = similar.map(posterCard).join("");
  } catch (e) {
    console.error(e);
    document.getElementById("title").textContent = "Movie not found";
  }
}
loadMovie();