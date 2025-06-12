import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import modules.graphiques_etude_cine as gec


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


if selected == "Population":
    st.subheader("Vue d'ensemble de l'activité")
    st.write("Ceci est votre page principale de vue d'ensemble.")

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
    with st.expander("Les gouts du public par tranche d'âge :"):

        # import des datasets
        # Chargement des différents CSV
        df_entrees = pd.read_csv("datasets/csv/df_public_entrees.csv")
        df_genre = pd.read_csv("datasets/csv/df_genre.csv")
        df_nationalite = pd.read_csv("datasets/csv/df_nationalites.csv")
        df_esf = pd.read_csv(
            "/Users/antoine/Documents/python/projet2/datasets/csv/df_entrees_seances_films_nationalites.csv"
        )

        # Récupération des publics (on prend le premier dataframe pour référence)
        publics = df_entrees["Public"].unique()

        # Sélecteur global dans la sidebar
        selected_publics = st.sidebar.multiselect(
            "Sélectionnez le(s) public(s) à afficher :",
            options=publics,
            default=publics,
        )

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

        tab_public_genre = pd.read_csv(
            "/Users/antoine/Documents/python/projet2/datasets/csv/df_public_genre_nat_pop.csv"
        )
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

            ######################
            ######CONCLUSION######
            ######################
