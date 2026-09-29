async function loadWatchlist() {
  const token = getToken();
  const container = document.getElementById("watchlist-results");

  if (!token) {
    container.innerHTML = "<p>Please <a href='login.html' style='color:#e50914'>login</a> to see your watchlist.</p>";
    return;
  }

  try {
    const res = await fetch(`${BASE_URL}/watchlist`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (!res.ok) throw new Error("Failed to load watchlist");
    const movies = await res.json();
    container.innerHTML = movies.length
      ? movies.map(posterCard).join("")
      : "<p>Your watchlist is empty.</p>";
  } catch (e) {
    container.innerHTML = "<p>Error loading watchlist.</p>";
    console.error(e);
  }
}
loadWatchlist();