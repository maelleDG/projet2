import streamlit as st
import pandas as pd
import plotly.express as px


def graphique_barres(df, colonne_categorie, couleur=None):
    """
    Crée un graphique en barres empilées à partir d'un dataframe.

    Paramètres :
    - df : dataframe source avec une colonne 'public' et des colonnes numériques.
    - colonne_categorie : nom de la colonne qui deviendra l'axe X après transformation.
    - couleur : liste de couleurs optionnelle.
    """

    if "Public" not in df.columns:
        st.error("Le dataframe doit contenir une colonne 'Public'.")
        return

    # Récupérer les colonnes de données (elles commencent après 'Public')
    cols = df.columns[1:]

    # Conversion en float avec remplacement des virgules
    for col in cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "."), errors="coerce"
        )

    # Transposition pour avoir les publics en ligne
    df_stacked = df.set_index("Public").T

    # Normalisation à 100%
    df_stacked = df_stacked.div(df_stacked.sum(axis=1), axis=0) * 100

    # Format long
    df_long = df_stacked.reset_index().melt(
        id_vars="index", var_name="Public", value_name="Pourcentage"
    )
    df_long.rename(columns={"index": colonne_categorie}, inplace=True)

    # Sélecteur
    publics = df_long["Public"].unique()
    selected_publics = st.sidebar.multiselect(
        "Choisissez le(s) public(s) à afficher :",
        options=publics,
        default=publics,
        key=f"multiselect_{colonne_categorie}",  # <- clé unique ici
    )

    # Filtrer
    df_filtered = df_long[df_long["Public"].isin(selected_publics)]

    # Couleurs par défaut
    if not couleur:
        couleur = ["#4c72b0", "#55a868", "#c44e52", "#8172b3"]

    # Graphique Plotly
    fig = px.bar(
        df_filtered,
        x=colonne_categorie,
        y="Pourcentage",
        color="Public",
        color_discrete_sequence=couleur,
        text_auto=".2f",
    )

    fig.update_layout(
        barmode="stack",
        legend_title="Public",
        legend=dict(x=1.05, y=1),
        margin=dict(t=60, b=40, l=40, r=40),
    )

    return st.plotly_chart(fig, use_container_width=True)


def graphique_esf(data):
    df = pd.DataFrame(data)

    # Conversion des pourcentages en float
    for col in ["films diffusés", "séances", "entrées"]:
        df[col] = df[col].str.replace(",", ".").str.rstrip("%").astype(float)

    # Transformation en format long
    df_long = pd.melt(
        df, id_vars="nationalité", var_name="indicateur", value_name="valeur"
    )

    # Création du graphique Plotly
    fig = px.bar(
        df_long,
        y="nationalité",
        x="valeur",
        color="indicateur",
        orientation="h",
        text="valeur",
        color_discrete_map={
            "films diffusés": "#4285F4",
            "séances": "#DB4437",
            "entrées": "#F4B400",
        },
    )

    # Personnalisation
    fig.update_traces(
        texttemplate="%{text:.2f}%", textposition="outside", textfont_color="grey"
    )
    fig.update_layout(
        title="Films diffusés, séances et entrées dans la Creuse en 2023",
        xaxis_title="Pourcentage (%)",
        yaxis_title="",
        barmode="group",
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",  # Fond extérieur transparent
        plot_bgcolor="rgba(0,0,0,0)",  # Fond intérieur (zone du graphique) transparent
        title_font_color="grey",
        xaxis=dict(title_font=dict(color="grey"), tickfont=dict(color="grey")),
        yaxis=dict(title_font=dict(color="grey"), tickfont=dict(color="grey")),
        legend=dict(font=dict(color="grey")),
    )

    # Affichage
    fig.show()
    return st.plotly_chart(fig, use_container_width=True)
