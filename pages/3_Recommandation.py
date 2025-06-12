import streamlit as st
import pandas as pd
import joblib
import streamlit.components.v1 as components

# --- Chargement des données ---
if "reco" not in st.session_state:
    df = pd.read_parquet("reco")
    st.session_state["reco"] = df
else:
    df = st.session_state["reco"]

# Chargement de la cartographie des voisins
carto = joblib.load("carto.pkl")

# Initialisation favoris
if "favoris" not in st.session_state or not isinstance(
    st.session_state["favoris"], set
):
    st.session_state["favoris"] = set()

# --- Préparation des genres ---
df["genres"] = df["genres"].fillna("[]")
df["genres_list"] = df["genres"].apply(lambda x: eval(x) if isinstance(x, str) else [])
all_genres = sorted({g for sublist in df["genres_list"] for g in sublist})

st.title("🎬 Ciné-Affinités : Votre Sélection Intelligente")
st.write("---")

# --- Choix du film principal ---
film_titles = df["title"].dropna().unique()
selected_title = st.selectbox("📽️ Choisissez un film:", sorted(film_titles))

# Réinitialisation si le film change
if "last_selected_title" not in st.session_state:
    st.session_state["last_selected_title"] = selected_title
elif st.session_state["last_selected_title"] != selected_title:
    st.session_state["selected_film_id"] = None
    st.session_state["last_selected_title"] = selected_title

n = df[df["title"] == selected_title].index[0]

# --- Sidebar ---
with st.sidebar:
    st.title("Filtres")
    if st.button("♻️ Réinitialiser les filtres"):
        st.session_state["selected_genres"] = []
        st.session_state["year_range"] = (1960, 2025)
        st.session_state["min_vote"] = 5.0

    selected_genres = st.multiselect(
        "Genres", all_genres, default=st.session_state.get("selected_genres", [])
    )
    min_year, max_year = st.slider(
        "Période de sortie",
        1960,
        2025,
        st.session_state.get("year_range", (1960, 2025)),
    )
    min_vote = st.slider(
        "Note moyenne minimale",
        0.0,
        10.0,
        st.session_state.get("min_vote", 5.0),
        step=0.1,
    )

    st.session_state["selected_genres"] = selected_genres
    st.session_state["year_range"] = (min_year, max_year)
    st.session_state["min_vote"] = min_vote

    # --- Affichage des favoris ---
    st.markdown("### 🎯 Mes Favoris")
    if st.session_state["favoris"]:
        for fav_id in st.session_state["favoris"]:
            try:
                fav_film = df.loc[fav_id]
                st.markdown(f"**🎞️ {fav_film['title']}**")
                if pd.notna(fav_film["poster_path"]):
                    st.image(
                        "https://image.tmdb.org/t/p/w92" + fav_film["poster_path"],
                        width=80,
                    )
            except:
                continue
    else:
        st.write("Aucun favori pour le moment.")

# --- Récupération des voisins ---
voisins_indices = carto[n]
voisins_indices = [i for i in voisins_indices if i != n]

# --- Filtrage des voisins ---
filtered_indices = []
for idx in voisins_indices:
    f = df.loc[idx]
    genres = eval(f["genres"]) if isinstance(f["genres"], str) else []
    year = int(str(f["release_date"])[:4]) if pd.notna(f["release_date"]) else 0
    vote = f["vote_average"] if pd.notna(f["vote_average"]) else 0

    if selected_genres and not any(g in genres for g in selected_genres):
        continue
    if not (min_year <= year <= max_year):
        continue
    if vote < min_vote:
        continue
    filtered_indices.append(idx)

# --- Affichage du film de départ ---
st.write("### 🎬 Film de départ :")
film = df.loc[n]
col1, col2 = st.columns([1, 3])
with col1:
    if pd.notna(film["poster_path"]):
        st.image(
            "https://image.tmdb.org/t/p/w200" + film["poster_path"],
            caption=film["title"],
            width=150,
        )
with col2:
    st.write(f"**Titre :** {film['title']}")
    st.write(f"**Date de sortie :** {film['release_date']}")
    st.write(f"**Langue :** {film['original_language']}")
    st.write(f"**Genres :** {film['genres']}")
    st.write(f"**Overview :** {film.get('overview', 'Aucun résumé disponible')}")

    # Bouton favoris
    if n not in st.session_state["favoris"]:
        if st.button("⭐ Ajouter aux favoris"):
            st.session_state["favoris"].add(n)
            st.success("Ajouté aux favoris !")
            st.rerun()
    else:
        if st.button("❌ Retirer des favoris"):
            st.session_state["favoris"].remove(n)
            st.info("Retiré des favoris.")
            st.rerun()

# --- Carrousel Swiper des films similaires ---
st.markdown("### 🎞️ Films similaires correspondants :")

if not filtered_indices:
    st.warning("Aucun film similaire ne correspond à vos critères.")
else:
    carousel_html = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.css"/>
    <style>
    .swiper-slide img {
        border-radius: 12px;
        max-height: 280px;
        cursor: pointer;
    }
    .swiper {
        width: 100%;
        padding-top: 10px;
        padding-bottom: 30px;
    }
    </style>
    <div class="swiper">
      <div class="swiper-wrapper">
    """

    for idx in filtered_indices:
        film = df.loc[idx]
        if pd.notna(film["poster_path"]):
            img_url = "https://image.tmdb.org/t/p/w300" + film["poster_path"]
            title = film["title"].replace('"', "'")
            tmdb_id = film["id"]
            tmdb_url = f"https://www.themoviedb.org/movie/{tmdb_id}"
            carousel_html += f"""
            <div class="swiper-slide">
            <a href="{tmdb_url}" target="_blank" rel="noopener noreferrer">
                <img src="{img_url}" title="{title}" />
            </a>
            </div>
            """

    carousel_html += """
      </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js"></script>
    <script>
    const swiper = new Swiper('.swiper', {
      slidesPerView: 5,
      spaceBetween: 10,
      freeMode: true,
    });
    </script>
    """

    components.html(carousel_html, height=330)
