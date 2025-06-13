import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import modules.graphiques_etude_cine as gec
import plotly.graph_objects as go


st.set_page_config(layout="wide")

# Création de 2 colonnes
col1, col2 = st.columns(2)

# Contenu de la première colonne :
with col1:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUZzfpnK2Q3sx97u7f_i77J1pr7tNF-_-rKQ&s"
    )

# Contenu de la deuxième colonne :
with col2:
    st.markdown(
        "<h1 style='text-align: center; font-size: 50px;'>Etude de marché sur la consommation de cinéma dans la région de la Creuse"
        "\n</h1>",
        unsafe_allow_html=True,
    )


# Création d'un menu
selected = option_menu(
    menu_title=None,
    options=["Population", "Etude cinématographique", "Conclusion"],
    icons=["house", "database", "graph-up-arrow"],
    default_index=0,
    orientation="horizontal",
)

######################################
########## PARTIE POPULATION #########
######################################

if selected == "Population":

    with st.expander("Population par grandes tranches d'âges"):
        slide1 = pd.read_csv("slide 1 - Feuille 1.csv")
        slide1_1 = pd.read_csv("slide 1 - Feuille 2.csv")
        st.subheader("Population par grandes tranches d'âges")
        st.write(
            "On constate que 60% de la population se situe entre 0 et 59 ans et que plus de la moitié se situe entre 30 et 59 ans. A noter que la population a une tendance à la baisse et au vieillissement."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.html(
                """<p style="text-align: center;"><small><b>Evolution de la population</small></b>"""
            )
            slide1.set_index("Tranche_Âge", inplace=True)
            fig, ax = plt.subplots(figsize=(10, 6))
            for column in slide1.columns:
                ax.plot(slide1.index, slide1[column], marker="o", label=column)
            ax.set_xlabel("Tranche d'Âge", color="white")
            ax.set_ylabel("Population (en nombre)", color="white")
            legend = ax.legend(
                title="Année", loc="upper left", facecolor="#333333", labelcolor="white"
            )
            plt.setp(legend.get_title(), color="white", fontweight="bold")
            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")
            ax.grid(True, color="white")
            for spine in ax.spines.values():
                spine.set_edgecolor("white")
            fig.patch.set_facecolor("none")
            ax.set_facecolor("none")
            st.pyplot(fig)
        with col2:
            slide1_1.set_index("Tranche_Âge", inplace=True)
            st.html(
                """<p style="text-align: center;"><small><b>Répartition par tranche d'âge pour 2021</small></b>"""
            )
            fig, ax = plt.subplots(figsize=(10, 6))
            plt.rcParams["font.family"] = "Arial"
            plt.rcParams["font.size"] = 14

            wedges, texts, autotexts = ax.pie(
                slide1_1["2021"],
                labels=slide1_1.index,
                colors=[
                    "crimson",
                    "rebeccapurple",
                    "darkorange",
                    "darkcyan",
                    "seagreen",
                    "indianred",
                    "gold",
                ],
                autopct="%1.1f%%",
                startangle=90,
            )
            ax.axis("equal")
            fig.patch.set_facecolor("none")
            ax.set_facecolor("none")
            for text in texts:
                text.set_color("white")
            st.pyplot(fig)
        st.html(
            """<p style="text-align: center;"><i><small>Sources : Insee, RP2010, RP2015 et RP2021, exploitations principales, géographie au 01/01/2024.</small></i>"""
        )

        data = pd.read_csv("Slide1.2 - Feuille 1.csv")
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.rcParams["font.family"] = "Arial"
        plt.rcParams["font.size"] = 14
        wedges, texts, autotexts = ax.pie(
            data["Pourcentage"],
            labels=data["Tranche_Age"],
            colors=[
                "crimson",
                "rebeccapurple",
                "darkorange",
                "darkcyan",
                "seagreen",
                "indianred",
                "gold",
            ],
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.axis("equal")

        st.subheader("Répartition de la population par tranche d'âge - Gueret")
        col1, col2 = st.columns(2)
        with col1:
            st.html(
                """<p style="text-align: center;"><small><b>Moyenne sur les trois dernières années</small></b>"""
            )
            fig.patch.set_facecolor("none")
            ax.set_facecolor("none")
            for text in texts:
                text.set_color("white")
            st.pyplot(fig)
            st.html(
                "<i><small>Sources : Insee, portant sur les années 2020, 2021 et 2022.</small></i>"
            )

        with col2:
            st.html(
                """<p style="text-align: justify;"> <br><br><br>Ces informations sont confirmées si on regarde la population de Guéret (ville la plus importante de la Creuse) sur la trois dernières années disponibles. <br>  <br>On peut noter une population légèrement plus jeune si on regarde Guéret (+8,7% pour les 15-29 ans et +1,7% pour les 45-59 ans)."""
            )

    # SLIDE 2
    with st.expander("Age et genre de la population Creusoise"):

        slide2 = pd.read_csv("Slide2 - Feuille 1.csv")
        st.subheader("Age et genre de la population Creusoise")
        st.html(
            """<p style="text-align: justify;"> En 2021, on peut constater que la Creuse présente une légère majorité de femmes dans sa population globale. On observe une supériorité numérique des hommes dans les tranches d'âge les plus jeunes.<br><br>La tendance s'inverse progressivement avec l'âge, et la prédominance féminine devient très marquée chez les seniors, en particulier les plus âgés. <br><br><b>La population en âge actif (20-64 ans) représente la part la plus importante de la population, avec une légère dominance masculine.</b></p>"""
        )
        fig, ax = plt.subplots(figsize=(6, 4))
        bar_width = 0.7
        bars_hommes = ax.bar(
            slide2["Tranche_Age"],
            slide2["Hommes%"],
            width=bar_width,
            label="Hommes",
            color="darkcyan",
        )
        ax.bar_label(
            bars_hommes,
            labels=[f"{h:.1f}%" for h in slide2["Hommes%"]],
            label_type="center",
            color="white",
            fontsize=6,
        )
        bars_femmes = ax.bar(
            slide2["Tranche_Age"],
            slide2["Femmes%"],
            width=bar_width,
            bottom=slide2["Hommes%"],
            label="Femmes",
            color="indianred",
        )
        ax.bar_label(
            bars_femmes,
            labels=[f"{f:.1f}%" for f in slide2["Femmes%"]],
            label_type="center",
            color="white",
            fontsize=6,
        )

        ax.set_xlabel("Tranche d'Âge", color="white", fontsize=6)
        st.html(
            """<p style="text-align: center;"><b>Distribution de la population par genre et tranche d'âge</b>"""
        )
        legend = ax.legend(
            title="Genre",
            facecolor="#333333",
            labelcolor="white",
            fontsize=6,
            title_fontsize=7,
        )
        plt.setp(legend.get_title(), color="white", fontweight="bold")
        for spine in ax.spines.values():
            spine.set_edgecolor("white")
        ax.tick_params(axis="x", colors="white", rotation=45, labelsize=6)
        ax.set_yticklabels([])
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")
        plt.tight_layout()
        st.pyplot(fig)
        st.html(
            """<p style="text-align: center;"><i><small>Sources: Insee, RP2021 exploitation principale, géographie au 01/01/2024.</small></i>"""
        )

    # SLIDE 3 / 4

    with st.expander(
        "Population de 15 ans ou plus selon la catégorie socioprofessionnelle"
    ):

        st.subheader(
            "Population de 15 ans ou plus selon la catégorie socioprofessionnelle"
        )
        st.html("<b>Vue Globale </b>")
        st.html(
            """<p style="text-align: justify;"> On peut voir que la population de la Creuse est constituée majoritairement de retraités (40% - cf.population vieillissante). Le reste pouvant être découpé en trois groupes: l’un constitué d’ouvrier et de personnes sans activités professionnelles représentant 27,4%, le
                deuxième constitué d’ouvriers et de professions intermédiaires (20,7%) et enfin pour le troisième, d'agriculteur, artisans, commerçants, cadres et autres professions intellectuelles (12,1%). <br><br> A noter que ces catégories restent stables au fil des années c’est-à-dire qu’il y a peu d'évolutions (faible baisse ou hausse).</p>"""
        )
        slide3 = pd.read_csv("Slide3 - Feuille 1.csv")
        fig, ax = plt.subplots(figsize=(10, 4))
        for year in ["2010", "2015", "2021"]:
            ax.plot(
                slide3["Categorie_socioprofessionnelle"],
                slide3[year],
                marker="o",
                label=year,
            )
        st.html(
            """<p style="text-align: center;"><b>Répartition des catégories socioprofessionnelles</b>"""
        )
        legend = ax.legend(
            title="Année",
            loc="upper left",
            facecolor="#333333",
            labelcolor="white",
            fontsize=9,
            title_fontsize=10,
        )
        plt.setp(legend.get_title(), color="white", fontweight="bold")
        for spine in ax.spines.values():
            spine.set_edgecolor("white")
        ax.tick_params(axis="x", colors="white", rotation=30, labelsize=9)
        ax.tick_params(axis="y", colors="white", labelsize=9)
        plt.xticks(rotation=45, ha="right")
        fig.patch.set_facecolor("none")
        ax.grid(True, color="white")
        ax.set_facecolor("none")
        st.pyplot(fig)

        st.html("<b>Vue par Genre </b>")
        st.html(
            """<p style="text-align: justify;"> En 2021, on peut constater que la Creuse présente forte ségrégation sexuée : certains secteurs sont clairement dominés par un sexe, comme les agriculteurs et les ouvriers (majorité masculine), et les employés (majorité féminine).<br><br> L'âge moyen des différentes catégories socioprofessionnelles semble varier considérablement. Les retraités sont majoritairement des personnes âgées, tandis que la catégorie "Autres personnes sans activité professionnelle" est dominée par les jeunes. Les professions intermédiaires et les employés ont une forte concentration dans la tranche d'âge actif (25-54 ans).<br><br>Pour la plupart des catégories professionnelles, la part des 25-54 ans est la plus élevée, ce qui est attendu car cela correspond à la population active.</p>"""
        )
        slide3_1 = pd.read_csv("Slide3 - Feuille 2.csv")
        fig, ax = plt.subplots(figsize=(10, 4))
        slide3_1.plot(
            kind="bar",
            x="Catégorie socioprofessionnelle",
            y=["Hommes (NB)", "Femmes (NB)"],
            color=["darkcyan", "indianred"],
            ax=ax,
        )
        legend = ax.legend(
            title="Genre",
            loc="upper left",
            facecolor="#333333",
            labelcolor="white",
            fontsize=9,
            title_fontsize=10,
        )
        plt.setp(legend.get_title(), color="white", fontweight="bold")
        plt.xticks(rotation=45, ha="right")
        ax.set_xlabel(" ")
        st.html(
            """<p style="text-align: center;"><b>Distribution selon la Catégorie Socioprofessionnelle par Genre</b>"""
        )
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")
        for spine in ax.spines.values():
            spine.set_edgecolor("white")
        ax.tick_params(axis="x", colors="white", labelsize=9)
        ax.tick_params(axis="y", colors="white", labelsize=9)
        st.pyplot(fig)

    # SLIDE 5
    with st.expander("Composition des ménages"):

        slide5 = pd.read_csv("Slide5 - Feuille 1.csv")
        st.subheader("Composition des ménages")
        st.html(
            """<p style="text-align: justify;">La majorité des ménages est constituée de personnes seules (42% -> 50/50 hommes/femmes) non visibles sur le tableau ci-dessus composé de 50% de personnes de plus de 80 ans et de 30% de personnes entre 65 et 79 ans pour la Creuse. Cette catégorie est suivi des couples sans enfant. On retrouve ensuite les couples avec enfants et famille monoparentale.</b></p>"""
        )

        fig, ax = plt.subplots(figsize=(13, 8))
        bar_width = 0.5
        bars_gueret = ax.bar(
            slide5["Ménages"],
            slide5["Gueret"],
            width=bar_width,
            label="Guéret",
            color="seagreen",
        )
        ax.bar_label(
            bars_gueret,
            labels=[f"{h:.1f}%" for h in slide5["Gueret"]],
            label_type="center",
            color="white",
            fontsize=8,
        )
        bars_creuse = ax.bar(
            slide5["Ménages"],
            slide5["Creuse"],
            width=bar_width,
            bottom=slide5["Gueret"],
            label="Creuse",
            color="darkcyan",
        )
        ax.bar_label(
            bars_creuse,
            labels=[f"{f:.1f}%" for f in slide5["Creuse"]],
            label_type="center",
            color="white",
            fontsize=8,
        )

        ax.set_xlabel("Ménages", color="white")
        st.html(
            """<p style="text-align: center;"><b>Répartition des Ménages (Guéret et Creuse) </b>"""
        )
        legend = ax.legend(
            title="Genre",
            loc="upper right",
            facecolor="#333333",
            labelcolor="white",
            fontsize=9,
            title_fontsize=10,
        )
        plt.setp(legend.get_title(), color="white", fontweight="bold")
        for spine in ax.spines.values():
            spine.set_edgecolor("white")
        ax.tick_params(axis="x", colors="white", rotation=45, labelsize=9)
        ax.set_xlabel(" ")
        fig.patch.set_facecolor("none")
        ax.set_facecolor("none")
        plt.tight_layout()
        st.pyplot(fig)
        st.html(
            "<i><small>Sources : Insee, portant sur les années 2020, 2021 et 2022</small></i>"
        )
        st.html(
            "<i><small>Sources : Insee, RP 2021, exploitation complémentaire, géographie au 01/01/2024.</small></i>"
        )

    # SLIDE 7

    with st.expander(
        "Comparaison de l'âge de la population entre la France et la Creuse"
    ):

        st.subheader(
            "Comparaison de l'âge de la population entre la France et la Creuse"
        )
        Slide7 = pd.read_csv("Slide7 - Feuille 1.csv")
        Slide7_1 = pd.read_csv("Slide7 - Feuille 2.csv")
        fig, ax = plt.subplots(1, 2, figsize=(14, 8))
        plt.rcParams.update({"font.size": 14})

        # Plot  France
        Slide7.plot(
            kind="barh",
            x="Tranche_Age",
            y=["Homme (France%)", "Femme (France%)"],
            ax=ax[0],
            color=["lightblue", "darkcyan"],
            width=0.8,
        )
        ax[0].set_title("Pyramide des âges en France", color="white")
        ax[0].set_xlabel("Pourcentage", fontsize=14, color="white")
        ax[0].set_ylabel("Tranche_Age", fontsize=14, color="white")
        ax[0].legend(title="Sexe", loc="upper right", fontsize=14)
        legend = ax[0].legend(
            title="Sexe",
            loc="upper right",
            fontsize=14,
            facecolor="#333333",
            labelcolor="white",
        )
        plt.setp(legend.get_title(), color="white", fontweight="bold")
        ax[0].tick_params(axis="both", which="major", labelsize=14, colors="white")
        fig.patch.set_facecolor("none")
        ax[0].set_facecolor("none")
        for spine in ax[0].spines.values():
            spine.set_edgecolor("white")

        # Plot  Creuse
        Slide7_1.plot(
            kind="barh",
            x="Tranche_Age",
            y=["Homme (Creuse%)", "Femme (Creuse%)"],
            ax=ax[1],
            color=["lightgreen", "seagreen"],
            width=0.8,
        )
        ax[1].set_title("Pyramide des âges en Creuse", color="white")
        ax[1].set_xlabel("Pourcentage", fontsize=14, color="white")
        ax[1].set_ylabel("Tranche_Age", fontsize=14, color="white")
        legend = ax[1].legend(
            title="Sexe",
            loc="upper right",
            fontsize=14,
            facecolor="#333333",
            labelcolor="white",
        )
        plt.setp(legend.get_title(), color="white", fontweight="bold")
        ax[1].tick_params(axis="both", which="major", labelsize=14, colors="white")

        plt.tight_layout()
        fig.patch.set_facecolor("none")
        ax[1].set_facecolor("none")
        for spine in ax[1].spines.values():
            spine.set_edgecolor("white")
        st.pyplot(fig)
        st.html(
            """<p style="text-align: justify;">Nous pouvons constater que la population est plus âgée qu’au niveau national. En 2021, le taux de personnes d’un âge inférieur à 30 ans s’élève à 25,5%, soit en dessous de la moyenne nationale (35,1%). A l’inverse, le taux de personnes d’âge supérieur à 60 ans est de 39,3%, alors qu’il est de 26,6% pour la France. </p>"""
        )


###################################
######ETUDE CINEMATOGRAPHIQUE######
###################################

elif selected == "Etude cinématographique":

    st.subheader("Etude cinématographique")
    st.write(
        """Le cinéma est un lieu de loisirs important, même dans les territoires ruraux comme la Creuse. Pourtant, les habitudes des spectateurs changent et les salles doivent s’adapter pour continuer à attirer du public.
            Cette étude a pour but de mieux comprendre ce qui plaît ou non aux spectateurs du département. Elle s’appuie sur des chiffres concernant le nombre de films diffusés, les séances organisées et les préférences du public selon l’âge.
            Grâce à ces éléments, nous allons :
            Voir quels types de films rencontrent le plus de succès et lesquels sont encore peu proposés.
            Identifier les publics à privilégier pour relancer la fréquentation.
            Proposer des idées concrètes pour adapter la programmation et mieux répondre aux envies des spectateurs.
            """
    )

    # import des datasets
    # Chargement des différents CSV
    df_entrees = pd.read_csv("df_public_entrees.csv")
    df_genre = pd.read_csv("df_genre.csv")
    df_nationalite = pd.read_csv("df_nationalites.csv")
    df_esf = pd.read_csv("df_entrees_seances_films_nationalites.csv")

    # Récupération des publics (on prend le premier dataframe pour référence)
    publics = df_entrees["Public"].unique()

    # Le sélecteur de public unique
    selected_publics = st.sidebar.multiselect(
        "Sélectionnez le(s) public(s) à afficher :",
        options=publics,
        default=publics,  # Tous sélectionnés par défaut
    )

    # Stocker la sélection dans st.session_state pour qu'elle soit accessible globalement
    st.session_state.selected_publics = selected_publics

    with st.expander("Les gouts du public par tranche d'âge :"):

        with st.container():
            col1, col2 = st.columns([1, 1])

            with col1:
                #########EXPLICATIONS DF_ENTREES###########
                st.markdown(
                    """ 
        ## Répartition par nombre d’entrées (succès des films)
        - <span style="font-size:30px;color: #FF5733;">**Les seniors**</span>  privilégient les films à **moins de 1 million d’entrées**.
        - **Les adultes** sont davantage attirés par les **blockbusters** (>1 million d’entrées).
        - <span style="font-size:30px;color: #FF5733;">Les **films confidentiels**</span>  (<100 000 entrées) séduisent également un **noyau senior**.

        > 📌 **Insight clé :**  
        La demande **senior** s’oriente vers un cinéma **d’auteur ou régional**, <span style="font-size:30px;color: #FF5733;">moins grand public</span> .
        """,
                    unsafe_allow_html=True,
                )

            with col2:
                ###########GRAPHIQUE DF_ENTREES#############
                gec.graphique_barres(df_entrees, colonne_categorie="Entrées")
                st.write("sources : CNC - Vertigo / Cinexpert")

            #########REPARTITION PAR GENRE#########
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                ###########GRAPHIQUE DF_GENRE###########
                gec.graphique_barres(df_genre, colonne_categorie="Genres")
                st.write("sources : CNC - Vertigo / Cinexpert")

            with col2:
                st.markdown(
                    """
        ## Répartition des publics par genre de films  
        Ce graphique montre comment les différents publics fréquentent les salles de cinéma en fonction des types de films proposés :
        - **Les seniors (50 ans et +)** sont très présents sur :
            - Les **comédies** (36,1 % du public)
            - Les **fictions** (37,8 %)
            - Les **documentaires** (36,7 %)
        - **Les enfants (3-14 ans)** dominent largement les séances d’**animation** (41,4 % du public).
        - **Les jeunes (15-24 ans)** et **les adultes (25-49 ans)** se partagent principalement entre **fictions** et **animations**.
        > 📌 **Insight clé :**  
        **<span style="font-size:30px;color: #FF5733;">Les seniors</span> jouent un rôle essentiel dans la fréquentation des salles**, notamment pour les <span style="font-size:30px;color: #FF5733;">films narratifs et les documentaires</span>.  
        Ils constituent un public fidèle et moteur qu’il est important de continuer à séduire et à fidéliser avec une programmation adaptée.
        """,
                    unsafe_allow_html=True,
                )

        ######REPARTITION PAR NATIONALITÉ DU FILM######
        with st.container():
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(
                    """
        ## Répartition par nationalité des films
        - **Les Seniors** plébiscitent les films **français** à **47,4 %**.
        - **Les Adultes** et **Jeunes** préfèrent les films **américains** et **européens non-français**.
        > 📌 **Insight clé :**  
        Les films <span style="font-size:30px;color: #FF5733;">**français**</span> constituent un levier naturel pour les seniors.
        """,
                    unsafe_allow_html=True,
                )
            with col2:
                ###########GRAPHIQUE DF_NATIONALITÉS###########
                gec.graphique_barres(df_nationalite, colonne_categorie="Nationalités")
                st.write("sources : CNC - Vertigo / Cinexpert")

        #################################################################
        ###########ETUDE ENTREES SEANCES FILMS PAR NATIONALITÉ###########
        #################################################################

        tab_public_genre = pd.read_csv("df_public_genre_nat_pop.csv")
        df_tab_pg = pd.DataFrame(tab_public_genre)
        df_tab_pg

        st.write(
            """
            **En clair :**  

- Les <span style="font-size:30px;color: #FF5733;">seniors</span> privilégient les films <span style="font-size:30px;color: #FF5733;">français</span> à <span style="font-size:30px;color: #FF5733;">faible budget/entrées</span> car ils sont perçus comme plus proches de leurs valeurs ou thématiques sociales.

- Les <span style="font-size:30px;color: #FF5733;">adultes</span> seraient segmentables en <span style="font-size:30px;color: #FF5733;">deux sous-publics</span> : amateurs de blockbusters et amateurs de films d’auteur confidentiels.

- Les jeunes privilégient les films à gros succès pour l’effet de groupe et l’effet viral des sorties cinéma.

- Les enfants vont principalement au cinéma pour des films événementiels à forte campagne marketing.
                 """,
            unsafe_allow_html=True,
        )

    with st.expander("Les films dans la Creuse :"):

        with st.container():

            ###########GRAPHIQUE ENTREES SEANCES FILMS PAR NATIONALITÉ###########
            gec.graphique_esf(df_esf)

            st.write("sources : CNC - Vertigo / Cinexpert")

            ###########EXPLICATIONS ENTREES SEANCES FILMS PAR NATIONALITÉ###########
            st.markdown(
                """
**Répartition des films à l’affiche :**  
- <span style="font-size:30px;color: #FF5733;">Films français</span>  : <span style="font-size:30px;color: #FF5733;">60 %</span>  des titres programmés  
- <span style="font-size:30px;color: #FF5733;">Films américains</span>  : <span style="font-size:30px;color: #FF5733;">18 %</span>  des titres seulement  
Les films français dominent largement l’offre.  

**Répartition des séances :**  
- Films américains : 25 % des séances  
- Films français : environ 60 % également  
Les films américains sont moins nombreux, mais obtiennent une part de séances supérieure à leur part dans l’offre, ce qui traduit une stratégie de concentration sur certains titres.
      
**Répartition des entrées :**  
- <span style="font-size:30px;color: #FF5733;">Films américains</span>  : <span style="font-size:30px;color: #FF5733;">32 %</span>  des entrées  
- Films français : en-deçà de leur part de séances  
Les <span style="font-size:30px;color: #FF5733;">films américains</span>  réalisent un succès majeur en fréquentation, avec un <span style="font-size:30px;color: #FF5733;">rendement par séance</span>  bien supérieur aux films français.

                            """,
                unsafe_allow_html=True,
            )


elif selected == "Conclusion":
    st.subheader(
        "Les principaux KPI à retenir"
    )  # ligne modifiée par Evi dans feature_evi
    st.write(
        "Accédez à la synthèse dans les onglets ci-dessous"
    )  # ligne modifiée par Evi dans feature_evi

    # Configuration___partie___Evi:

    # Métriques principales en colonnes:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="👥 Population 60+", value="39.3%", delta="Segment prioritaire")

    with col2:
        st.metric(label="🇫🇷 Films français", value="47.4%", delta="vs 32% américains")

    with col3:
        st.metric(
            label="🏠 Couples sans enfants", value="52.4%", delta="Cible privilégiée"
        )

    with col4:
        st.metric(label="💰 ROI Films US", value="1.49", delta="vs 1.2 français")

        # Onglets principaux
    tab1, tab2, tab3 = st.tabs(["👥 Démographie", "🎭 Préférences", "🤖 Algorithmes"])

    with tab1:
        st.header("Profil Démographique Creusois")

        col1, col2 = st.columns(2)

        with col1:
            # Graphique démographique
            demo_data = pd.DataFrame(
                {
                    "Tranche d'âge": ["60+ ans", "25-59 ans", "18-24 ans", "0-17 ans"],
                    "Pourcentage": [39.3, 35.2, 12.8, 12.7],
                }
            )

            fig_demo = px.pie(
                demo_data,
                values="Pourcentage",
                names="Tranche d'âge",
                title="Répartition par âge",
                color_discrete_sequence=["#FA6BFF", "#4E4ECD", "#45B7D1", "#96CEB4"],
            )
            st.plotly_chart(fig_demo, use_container_width=True)

        with col2:
            st.markdown(
                """
            ### 🎯 Insights démographiques
            """
            )

            st.success(
                """
            **Cible prioritaire : Seniors 60+**
            - 39,3% de la population totale
            - Retraités = 40% population active
            - Stabilité financière élevée
            - Fidélité aux préférences
            """
            )

            st.info(
                """
            **Opportunité ménages**
            52,4% des ménages sans enfants = cible idéale pour soirées cinéma en couple
            """
            )

            st.warning(
                """
            **Défi jeunes**
            Seulement 25,5% de moins de 25 ans = adaptation nécessaire
            """
            )

    with tab2:
        st.header("Préférences Cinématographiques")

        col1, col2 = st.columns(2)

        with col1:
            # Préférences nationalité
            nat_data = pd.DataFrame(
                {
                    "Nationalité": [
                        "Films français",
                        "Films américains",
                        "Autres nationalités",
                    ],
                    "Préférence (%)": [47.4, 32.0, 20.6],
                    "Performance ROI": [1.2, 1.49, 0.8],
                }
            )

            fig_nat = px.bar(
                nat_data,
                x="Nationalité",
                y="Préférence (%)",
                title="Préférences par nationalité",
                color="Performance ROI",
                color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig_nat, use_container_width=True)

        with col2:
            # Genres seniors
            genre_data = pd.DataFrame(
                {
                    "Genre": [
                        "Fiction dramatique",
                        "Documentaire",
                        "Comédie",
                        "Animation",
                        "Action",
                    ],
                    "Préférence (%)": [37.8, 36.7, 36.1, 15.2, 12.4],
                }
            )

            fig_genre = px.bar(
                genre_data,
                x="Préférence (%)",
                y="Genre",
                orientation="h",
                title="Genres préférés (Seniors)",
                color="Préférence (%)",
                color_continuous_scale="Oranges",
            )
            st.plotly_chart(fig_genre, use_container_width=True)

        # Insight business
        st.markdown(
            """
        ### 💰 Insights Business
        """
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                """
            **Films français**
            - 47,4% de préférence
            - ROI : 1.2
            - Base solide et fidèle
            """
            )
        with col2:
            st.markdown(
                """
            **Films américains**
            - 32% de préférence
            - ROI : 1.49 ⭐
            - Potentiel rentabilité
            """
            )
        with col3:
            st.markdown(
                """
            **Autres nationalités**
            - 20,6% de préférence
            - Marché sous-exploité
            - Opportunité de niche
            """
            )

    with tab3:
        st.header("Algorithmes de Recommandation")

        col1, col2 = st.columns([1, 1])

        with col1:
            # Radar chart des critères
            categories = [
                "Âge",
                "Genre",
                "Nationalité",
                "Période",
                "Popularité",
                "Proximité",
            ]
            values = [95, 85, 90, 75, 70, 88]

            fig_radar = go.Figure()
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill="toself",
                    name="Importance des critères",
                )
            )
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                title="Critères de personnalisation",
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col2:
            st.markdown("### Segments recommandés")

            segments = {
                "Cinéphiles seniors": "Films français, comédies, drames, documentaires",
                "Familles crétoises": "Animation, films événementiels weekend",
                "Jeunes adultes": "Blockbusters, nouveautés virales",
                "Couples sans enfants": "Soirées cinéma, films romantiques/comédies",
            }

            for segment, description in segments.items():
                with st.expander(f"👤 {segment}"):
                    st.write(description)

            st.markdown("### ⏰ Timing optimal")
            st.markdown(
                """
            - **Seniors** : Séances en semaine (flexibilité horaire)
            - **Familles** : Weekend après-midi
            - **Couples** : Soirées semaine/weekend
            - **Jeunes** : Soirées et weekend
            """
            )

    # Conclusion finale
    st.markdown("---")
    st.markdown(
        """
    ## 🎯 Conclusion Stratégique

    Cette étude révèle un **marché de niche très spécifique** où la personnalisation fine peut créer un avantage concurrentiel fort,
    en s'appuyant sur les préférences culturelles marquées du public creusois.

    **Points clés :**
    - Population senior dominante (39,3%) = opportunité de fidélisation
    - Préférence films français (47,4%) = levier identitaire
    - ROI films américains supérieur (1,49) = optimisation rentabilité
    - Géographie restreinte (115k hab.) = personnalisation poussée possible
    """
    )

    # Footer
    st.markdown(
        """
    ---
    *Dashboard généré en juin 2025 pour l'étude de marché cinématographique en Creuse
    """,
        help="Données basées sur l'analyse démographique et les préférences culturelles locales, datasets utilisés: IMDb et TMDb",
    )
