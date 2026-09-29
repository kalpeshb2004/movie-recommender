async function loadHome() {
  try {
    const trending = await apiGet("/movies/trending?limit=20");
    const topRated = await apiGet("/movies/top-rated?limit=20");

    if (trending.length) {
      const hero = trending[0];
      document.getElementById("hero").style.backgroundImage =
        `url('${hero.backdrop_url || hero.poster_url || ""}')`;
      document.getElementById("hero-title").textContent = hero.title;
      document.getElementById("hero-overview").textContent =
        (hero.genres || "").split(",").join(" • ");
      document.getElementById("hero-more").onclick =
        () => location.href = `movie.html?id=${hero.id}`;
    }

    document.getElementById("trending-row").innerHTML =
      trending.map(posterCard).join("");
    document.getElementById("top-rated-row").innerHTML =
      topRated.map(posterCard).join("");

    const genres = ["Action", "Comedy", "Horror", "Romance"];
    for (const g of genres) {
      const movies = await apiGet(`/movies/genre/${g}?limit=20`);
      const row = document.createElement("div");
      row.className = "row";
      row.innerHTML = `<h2>${g}</h2><div class="row-items">${movies.map(posterCard).join("")}</div>`;
      document.getElementById("genre-rows").appendChild(row);
    }
  } catch (e) {
    console.error(e);
  }
}
loadHome();