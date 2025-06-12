import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px


def top_acteurs_actrices(selected_dataframe):

    with st.expander("Voir le Top 10 des acteurs et actrices :"):
        # Filtrer pour les acteurs
        actors_only_df = selected_dataframe[selected_dataframe["category"] == "actor"]
        # Compter les films uniques par acteur
        unique_actor_films = actors_only_df[["primaryName", "tconst"]].drop_duplicates()
        film_count_by_actor = unique_actor_films["primaryName"].value_counts()
        # Obtenir le top 10 des acteurs
        top_10_actors = film_count_by_actor.head(10).sort_values(ascending=False)

        # Filtrer pour les actrices
        actresses_only_df = selected_dataframe[
            selected_dataframe["category"] == "actress"
        ]
        # Compter les films uniques par actrice
        unique_actress_films = actresses_only_df[
            ["primaryName", "tconst"]
        ].drop_duplicates()
        film_count_by_actress = unique_actress_films["primaryName"].value_counts()
        # Obtenir le top 10 des actrices
        top_10_actresses = film_count_by_actress.head(10).sort_values(ascending=False)

        # Création du graphique en barres opposées
        fig, ax = plt.subplots(figsize=(8, 4))

        # Inverser l'ordre des tops 10 pour que le plus grand nombre soit en haut du graphique
        top_10_actors_rev = top_10_actors.iloc[::-1]
        top_10_actresses_rev = top_10_actresses.iloc[::-1]

        # Créer les palettes de couleurs
        colors_actors = sns.color_palette("viridis", n_colors=10)
        colors_actresses = sns.color_palette(
            "viridis", n_colors=10
        )  # Changed color palette for variety

        # Tracer les barres pour les Acteurs (à gauche, valeurs négatives)
        for i, (name, count) in enumerate(top_10_actors_rev.items()):
            ax.barh(i, -count, color=colors_actors[i], height=0.7)
            # Afficher le nom de l'acteur
            ax.text(
                -count - 1,
                i,
                name,
                va="center",
                ha="right",
                fontsize=6,
                color="dimgray",
            )
            # Afficher le nombre de films
            ax.text(
                -count / 2,
                i,
                str(int(count)),
                va="center",
                ha="center",
                fontsize=8,
                color="white",
            )

        # Tracer les barres pour les Actrices (à droite, valeurs positives)
        for i, (name, count) in enumerate(top_10_actresses_rev.items()):
            ax.barh(i, count, color=colors_actresses[i], height=0.7)
            # Afficher le nom de l'actrice
            ax.text(
                count + 1, i, name, va="center", ha="left", fontsize=6, color="dimgray"
            )
            # Afficher le nombre de films
            ax.text(
                count / 2,
                i,
                str(int(count)),
                va="center",
                ha="center",
                fontsize=8,
                color="white",
            )

        # Personnalisation des titres et axes
        ax.set_title(
            "Top 10 des acteurs et actrices",
            fontsize=15,
            color="dimgray",
            pad=20,
        )
        ax.set_ylabel("")  # Masquer le label Y
        ax.set_yticks([])  # Masquer les ticks de l'axe Y

        # Ajuster les limites de l'axe X pour qu'elles soient symétriques
        max_val = max(top_10_actors_rev.max(), top_10_actresses_rev.max())
        ax.set_xlim(-max_val - 15, max_val + 15)

        # Formater les étiquettes de l'axe X pour afficher les valeurs absolues
        formatter = plt.FuncFormatter(lambda x, p: f"{abs(int(x))}")
        ax.xaxis.set_major_formatter(formatter)
        ax.tick_params(axis="x", colors="dimgray", labelsize=6)
        ax.set_xlabel("Nombre de films", fontsize=8, color="dimgray", labelpad=6)

        # Ajouter une ligne verticale au centre
        ax.axvline(0, color="grey", linewidth=0.8, alpha=0.7)

        # Ajouter des titres pour chaque côté
        ax.text(
            -max_val / 2,
            len(top_10_actors_rev) - 0.1,  # Adjusted Y position
            "Acteurs",
            ha="center",
            va="bottom",
            fontsize=10,
            color="dimgray",
        )
        ax.text(
            max_val / 2,
            len(top_10_actresses_rev) - 0.1,  # Adjusted Y position
            "Actrices",
            ha="center",
            va="bottom",
            fontsize=10,
            color="dimgray",
        )

        # Set background color for the plot area
        ax.set_facecolor("none")

        # Set figure background color
        fig.patch.set_facecolor("none")
        fig.patch.set_edgecolor("none")
        fig.patch.set_linewidth(0)

        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.markdown(
            """Le graphique ci-dessus met en lumière les **acteurs et actrices les plus prolifiques**, classés par le nombre de films dans lesquels ils ont joué."""
        )
        st.markdown(
            f""" Nous pouvons constaté que <span style="font-size:30px;color: #FF5733;">**{top_10_actors.index[0]}**</span> 
            et <span style="font-size:30px;color: #FF5733;">**{top_10_actresses.index[0]}**</span> sont les 2 acteurs/actrices les plus représentatifs depuis les années 1975,
            avec respectivement <span style="font-size:30px;color: #FF5733;">**{int(top_10_actors.iloc[0])}**</span>  et <span style="font-size:30px;color: #FF5733;">**{int(top_10_actresses.iloc[0])} films**</span> à leur actif.
            
            """,
            unsafe_allow_html=True,
        )


def top_acteurs_actrices_et_genres(selected_dataframe):

    with st.expander("Voir le Top 10 des genres par acteurs/actrices :"):
        # Assurez-vous que la colonne 'genres' est de type string et non nulle
        selected_dataframe["genres"] = selected_dataframe["genres"].astype(str)

        # 1. Séparer les genres et les "exploser" pour avoir une ligne par genre par film
        # Crée une liste de genres pour chaque entrée, puis déploie chaque genre sur une nouvelle ligne
        df_genres_exploded = selected_dataframe.assign(
            genres=selected_dataframe["genres"].str.split(",")
        ).explode("genres")

        # Nettoyer les espaces blancs autour des noms de genres après le split
        df_genres_exploded["genres"] = df_genres_exploded["genres"].str.strip()

        # 2. Filtrer pour les acteurs et les actrices
        actors_df = df_genres_exploded[df_genres_exploded["category"] == "actor"]
        actresses_df = df_genres_exploded[df_genres_exploded["category"] == "actress"]

        # 3. Compter les genres les plus fréquents pour les acteurs
        top_genres_actors = actors_df["genres"].value_counts().reset_index()
        top_genres_actors.columns = ["Genre", "Nombre de films"]

        # 4. Compter les genres les plus fréquents pour les actrices
        top_genres_actresses = actresses_df["genres"].value_counts().reset_index()
        top_genres_actresses.columns = ["Genre", "Nombre de films"]

        # Pour obtenir un genre en particulier si vous voulez l'intégrer dans une phrase
        most_common_genre_actor = (
            top_genres_actors["Genre"].iloc[0] if not top_genres_actors.empty else "N/A"
        )
        most_common_genre_actress = (
            top_genres_actresses["Genre"].iloc[0]
            if not top_genres_actresses.empty
            else "N/A"
        )

        ## Visualisation des genres par Treemap
        ### Treemap pour les ACTEURS
        if not top_genres_actors.empty:
            st.write("#### Répartition des genres pour les acteurs")
            st.write(
                """
            Ce treemap met en évidence les genres les plus fréquents dans lesquels les **acteurs** sont apparus.
            """
            )
            st.markdown(
                f'Le genre le plus courant pour les acteurs est <span style="font-size:30px;color: #FF5733;">**{most_common_genre_actor}**</span>.',
                unsafe_allow_html=True,
            )
            fig_actors = px.treemap(
                top_genres_actors.head(
                    10
                ),  # Limiter aux top 10 pour une meilleure lisibilité
                path=["Genre"],
                values="Nombre de films",
                title="Top Genres pour les Acteurs",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_actors.update_layout(margin=dict(t=50, l=25, r=25, b=25))
            st.plotly_chart(fig_actors, use_container_width=True)
        else:
            st.write("Pas assez de données pour générer le treemap des acteurs.")

        ### Treemap pour les ACTRICES
        if not top_genres_actresses.empty:
            st.write("#### Répartition des genres pour les actrices")
            st.write(
                """
            Ce treemap présente les genres les plus communs dans lesquels les **actrices** ont joué.
            """
            )
            st.markdown(
                f'Le genre le plus courant pour les actrices est <span style="font-size:30px;color: #FF5733;">**{most_common_genre_actress}**</span>.',
                unsafe_allow_html=True,
            )
            fig_actresses = px.treemap(
                top_genres_actresses.head(
                    10
                ),  # Limiter aux top 10 pour une meilleure lisibilité
                path=["Genre"],
                values="Nombre de films",
                title="Top Genres pour les Actrices",
                color_discrete_sequence=px.colors.qualitative.Plotly,  # Une autre palette de couleurs
            )
            fig_actresses.update_layout(margin=dict(t=50, l=25, r=25, b=25))
            st.plotly_chart(fig_actresses, use_container_width=True)
        else:
            st.write("Pas assez de données pour générer le treemap des actrices.")


def top_realisateurs(df):
    with st.expander("Voir le Top 10 des réalisateurs :"):
        # Assurez-vous que la colonne "category" existe et que "director" est une valeur valide.
        df_director = df[df["category"] == "director"]

        # Obtenir le top 10 des réalisateurs
        # top_directors_by_films est une Série. Pour Plotly Express, il est préférable de la convertir en DataFrame.
        top_directors_series = df_director["primaryName"].value_counts().head(10)

        if top_directors_series.empty:
            st.warning("Aucun réalisateur trouvé après le filtrage ou dans le top 10.")
            return

        # Convertir la Série en DataFrame pour Plotly Express
        df_top_directors = top_directors_series.reset_index()
        df_top_directors.columns = ["Nom du réalisateur", "Nombre de films réalisés"]

        # Créer le graphique avec Plotly Express
        fig = px.bar(
            df_top_directors,
            x="Nom du réalisateur",
            y="Nombre de films réalisés",
            title="Top 10 des réalisateurs par nombre de films (avec notes > 6.8 et > 80k votes)",
            labels={
                "Nom du réalisateur": "Réalisateur",
                "Nombre de films réalisés": "Nombre de films",
            },
            color_discrete_sequence=["blue"],  # Définit la couleur des barres
        )

        # Personnalisations supplémentaires (équivalent de plt.xticks, ax.grid, etc.)
        fig.update_layout(
            xaxis_title_text="Nom du réalisateur",
            yaxis_title_text="Nombre de films réalisés",
            xaxis_tickangle=-45,  # Fait pivoter les étiquettes de l'axe X
            title_font_size=16,
            height=500,  # Hauteur du graphique
        )
        # Ajoute une grille sur l'axe Y
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")

        # Affiche le graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f"""
                    Le graphique révèle que <span style="font-size:30px;color: #FF5733;">**{top_directors_series.index[0]}**</span> domine clairement le classement des réalisateurs avec la plus grande quantité de films 
                    ayant obtenu une note moyenne supérieure à 6.8 et plus de 80 000 votes, affichant environ 30 réalisations dans ces critères. 
                    Il est suivi par <span style="font-size:30px;color: #FF5733;">**{top_directors_series.index[1]}**</span> 
                    et un groupe de réalisateurs comme <span style="font-size:30px;color: #FF5733;">**{top_directors_series.index[2]}**</span>, 
                    <span style="font-size:30px;color: #FF5733;">**{top_directors_series.index[3]}**</span>, et <span style="font-size:30px;color: #FF5733;">**{top_directors_series.index[4]}**</span> qui ont un nombre significatif de films qualifiés, 
                    démontrant ainsi la persistance et la reconnaissance critique de ces cinéastes au sein de la base de données filtrée.
""",
            unsafe_allow_html=True,
        )
