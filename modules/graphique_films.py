import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def graphique_film_metric(df):
    with st.expander(
        "Voir l'évolution de la durée et le nombre de films depuis les 50 dernières années : "
    ):
        # Calculate average runtime per year for movies longer than 70 minutes
        duree_moyenne_par_annee = (
            df.groupby("startYear")["runtimeMinutes"].mean().reset_index()
        )
        duree_moyenne_par_annee.sort_values(by="startYear", inplace=True)

        # Calculate the number of films released each year
        nombre_films_par_annee = (
            df.groupby("startYear").size().reset_index(name="nombre_de_films")
        )

        # Create the plot with two Y-axes
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # First Y-axis for average movie runtime
        ax1.plot(
            duree_moyenne_par_annee["startYear"],
            duree_moyenne_par_annee["runtimeMinutes"],
            color="skyblue",
            marker="o",
            linestyle="-",
            label="Durée moyenne des films",
        )
        ax1.set_xlabel("Année de sortie", fontsize=12)
        ax1.set_ylabel("Durée moyenne des films (minutes)", fontsize=12)
        ax1.tick_params(axis="y")

        # Create a second Y-axis sharing the same X-axis
        ax2 = ax1.twinx()
        ax2.plot(
            nombre_films_par_annee["startYear"],
            nombre_films_par_annee["nombre_de_films"],
            color="purple",
            marker="o",
            linestyle="-",
            label="Nombre de films sortis",
        )
        ax2.set_ylabel("Nombre de films sortis", fontsize=12)
        ax2.tick_params(axis="y")

        # Plot title
        plt.title(
            f"Évolution de la durée moyenne des films et du nombre de films sortis ({df['startYear'].min()}-{df['startYear'].max()})",
            fontsize=16,
        )

        # Add legends for both axes
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc="upper left")

        # Afficher le graphique dans Streamlit
        st.pyplot(fig)
        plt.close(fig)

        st.markdown(
            """Le graphique révèle une industrie cinématographique <span style="font-size:30px;color: #FF5733;">**dynamique**</span> , 
            avec une <span style="font-size:30px;color: #FF5733;">**croissance explosive**</span>  du volume de production sur deux décennies, 
            suivie d'une période de turbulence (pandémie) et d'une possible réorientation récente, 
            tandis que la durée moyenne des films, bien que sujette à des fluctuations, est restée dans une <span style="font-size:30px;color: #FF5733;">**fourchette relativement stable**</span> sur le long terme.""",
            unsafe_allow_html=True,
        )


def top10_films(df):
    with st.expander("Voir le top 10 des films les mieux notés : "):
        # Grouper les films et agréger les informations pertinentes.
        # Nous utilisons 'first' car ces colonnes devraient être les mêmes pour chaque film.
        df_films = (
            df.groupby(["originalTitle", "startYear"])
            .agg(
                averageRating=("averageRating", "first"),
                numVotes=("numVotes", "first"),
                genres=("genres", "first"),
                runtimeMinutes=("runtimeMinutes", "first"),
            )
            .reset_index()
        )

        # Trier les films par 'averageRating' en ordre décroissant pour obtenir les mieux notés.
        films_mieux_notes = df_films.sort_values(
            by=["numVotes", "averageRating"], ascending=[False, False]
        )
        # Renommer des colonnes spécifiques
        films_mieux_notes_renomme = films_mieux_notes.rename(
            columns={
                "originalTitle": "Titre Original",
                "startYear": "Année de sortie",
                "averageRating": "Note Moyenne",
                "numVotes": "Nombre de Votes",
                "genres": "Genres du Film",
                "runtimeMinutes": "Durée (minutes)",
            }
        )

        st.subheader("Top 10 des films les mieux notés")

        # Afficher les 10 premiers films dans un tableau Streamlit.
        # On inclut des colonnes supplémentaires pour plus de détails.
        st.dataframe(
            films_mieux_notes_renomme[
                [
                    "Titre Original",
                    "Année de sortie",
                    "Note Moyenne",
                    "Nombre de Votes",
                    "Genres du Film",
                    "Durée (minutes)",
                ]
            ].head(10)
        )
