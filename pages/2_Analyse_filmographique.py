import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import ast
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import modules.graphique_acteurs as ga
import modules.graphique_films as gf

# Barre latérale
with st.sidebar:
    # Ajout d'un titre à la barre latérale
    st.title("Filtres")

# Création de 2 colonnes
col1, col2 = st.columns(2)

# Contenu de la première colonne :
with col1:
    st.image(
        "https://spaces.filmstories.co.uk/uploads/2022/01/imdb-lead-image.jpg",
        width=400,
    )

# Contenu de la deuxième colonne :
with col2:
    st.markdown(
        "<h1 style='text-align: center; font-size: 60px;'>Analyse filmographique"
        "\n IMDB</h1>",
        unsafe_allow_html=True,
    )

# --- Chargement du dataset ---
# Pour éviter de recharger si déjà chargé, utilisez st.session_state
if "datasets_dispo" not in st.session_state:
    st.session_state["datasets_dispo"] = {
        "Acteurs": pd.read_parquet("Top10acteurs"),
        "Films": pd.read_parquet("Duree_film"),
    }

# Création d'une liste de dataset
datasets_dispo = st.session_state["datasets_dispo"]

# Ajouter la possibilité de choisir un dataset entre acteur et film
theme = st.sidebar.selectbox("Choisissez un thème :", list(datasets_dispo.keys()))

selected_dataframe = datasets_dispo[theme]

st.write(
    f"Vous avez sélectionné le thème: <span style='color: #FF5733;'>**{theme}**</span>",
    unsafe_allow_html=True,
)

# Explication de l'analyse
st.markdown(
    """
    <div style='text-align: justify;'>
    Pour identifier les acteurs/actrices et les réalisateurs les plus représentatifs, notre analyse se concentre sur les films des <span style="font-size:30px;color: #FF5733;">50 dernières années (à partir de 1975)</span>, dont la durée est comprise entre <span style="font-size:30px;color: #FF5733;">70 et 200 minutes</span>,
    en considérant uniquement ceux qui ont reçu un minimum de <span style="font-size:30px;color: #FF5733;">80 000 votes</span> et dont la note moyenne est <span style="font-size:30px;color: #FF5733;">supérieure à 6.8 </span>(ce qui correspond au troisième quartile des notes).
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("---")

# --- Section d'analyse et d'affichage ---

if theme == "Acteurs":
    st.markdown("## Analyses sur les Acteurs")

    # Création de la partie du top 10 des meilleurs acteurs/actrices

    ga.top_acteurs_actrices(selected_dataframe)

    # Création de la partie du top 10 des genres par acteurs et actrices

    ga.top_acteurs_actrices_et_genres(selected_dataframe)

    # Création de la partie du top 10 des réalisateurs

    ga.top_realisateurs(selected_dataframe)


elif theme == "Films":
    st.markdown("## Analyses sur les Films")

    # Création de la partie du top 10 des genres par acteurs et actrices

    gf.graphique_film_metric(selected_dataframe)

    # Création de la partie du top 10 des meilleurs films

    gf.top10_films(selected_dataframe)
