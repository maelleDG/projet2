import streamlit as st
import pandas as pd
import ast

# Chargement du dataset
# pour éviter de recharger si déjà charger
if "df" in st.session_state:
    df = st.session_state["df"]
else:
    df = pd.read_parquet("film_fr_tmdb.parquet")
st.session_state["df"] = df

# slider pour la durée minimale et maximale
selected_runtime_min, selected_runtime_max = st.sidebar.slider(
    "Sélectionnez la plage de durée du film (en minutes) :",
    min_value=int(df["runtime"].min()),
    max_value=int(df["runtime"].max()),
    value=(
        int(df["runtime"].min()),
        int(df["runtime"].max()),
    ),  # Valeurs initiales min et max
)

# Nettoyage de chaque genre : suppression des espaces et uniformisation de la casse
df["genres"] = df["genres"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)

# Nettoyage des genres (suppression des espaces et uniformisation de la casse)
# C'est important pour que 'Action ' et 'Action' ne soient pas considérés comme uniques.
df["genres"] = df["genres"].apply(
    lambda genre_list: (
        [g.strip().title() for g in genre_list] if isinstance(genre_list, list) else []
    )
)

# 1. Utiliser `explode()` pour aplatir la liste de listes en une seule Series.
# 2. Utiliser `unique()` pour obtenir les valeurs uniques.
# 3. Convertir le résultat (un array NumPy) en une liste Python.
# 4. Trier la liste pour avoir un ordre prévisible.
genres_uniques_liste = sorted(df["genres"].explode().dropna().unique().tolist())

# Menu déroulant multiselect
selected_genres = st.sidebar.multiselect(
    "Sélectionnez un ou plusieurs genres :", genres_uniques_liste
)

# Application de filtres:
filtered_df = df.copy()

# Filtrer le DataFrame selon la sélection de temps (plage min et max)
filtered_df = filtered_df[
    (filtered_df["runtime"] >= selected_runtime_min)
    & (filtered_df["runtime"] <= selected_runtime_max)
]

# Filtrer le DataFrame selon la sélection de genre
# Cette partie doit s'appliquer au filtered_df qui a déjà le filtre de durée
if selected_genres:
    filtered_df = filtered_df[  # IMPORTANT : Filtrer sur filtered_df, pas sur df
        filtered_df["genres"].apply(
            lambda genres: any(g in genres for g in selected_genres)
        )
    ]
    st.write(
        f"Films correspondant aux genres : {selected_genres} et durée entre {selected_runtime_min} et {selected_runtime_max} minutes"
    )
else:
    st.write(
        f"Aucun genre sélectionné. Affichage de tous les films avec une durée entre {selected_runtime_min} et {selected_runtime_max} minutes."
    )

# Afficher le DataFrame filtré après toutes les applications de filtres
st.dataframe(filtered_df)

# Pour illustrer, reprenons le filtrage de votre code précédent pour le thème Film
# 1. Slider pour la durée minimale et maximale (déjà dans votre code précédent)
#    Il faut s'assurer que ces variables (selected_runtime_min, selected_runtime_max, selected_genres)
#    sont définies ou déplacées dans ce bloc if.

# Pour que votre code de filtrage des films fonctionne ici:
# 1. Déplacez les lignes de création des sliders et multiselect dans ce bloc `if theme == "Films":`
# 2. Réinitialisez ou adaptez `genres_uniques_liste` en fonction de `selected_dataframe` (qui est maintenant le df des films)

# Exemple simplifié pour ne pas dupliquer tout le code de filtrage des films ici,
# mais pour montrer comment l'appeler si vous l'avez refactorisé dans une fonction.
# Sinon, vous devrez coller le code du slider et du multiselect ici.

# # Nettoyage de chaque genre pour le dataframe 'Films'
# selected_dataframe["genres"] = selected_dataframe["genres"].apply(
#     lambda x: ast.literal_eval(x) if isinstance(x, str) else x
# )
# # Nettoyage des genres (suppression des espaces et uniformisation de la casse)
# selected_dataframe["genres"] = selected_dataframe["genres"].apply(
#     lambda genre_list: (
#         [g.strip().title() for g in genre_list] if isinstance(genre_list, list) else []
#     )
# )
#
# genres_uniques_liste_films = sorted(selected_dataframe["genres"].explode().dropna().unique().tolist())
#
# selected_genres_films = st.sidebar.multiselect(
#     "Sélectionnez un ou plusieurs genres de films :", genres_uniques_liste_films
# )
#
# # Ajoutez ici les filtres de durée et de genre pour les films
# #...
