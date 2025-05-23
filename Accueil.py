from streamlit_option_menu import option_menu
import streamlit as st

st.set_page_config(
    page_title="Projet2",
    page_icon="🎥",
)

st.title("🎥 Bienvenue à notre Projet 2")
st.write("## Par Antoine, Evi, Marie et Maëlle")

st.markdown(
    """
        ---
        Notre équipe Data a été contactée par un **cinéma en perte de vitesse** situé dans **la Creuse**.  
        Pour se moderniser, il souhaite créer un **site Internet** taillé pour les locaux, 
        avec un **moteur de recommandations de films** personnalisées.

        🎯 **Objectif** : Développer un système de recommandations malgré une situation de *cold start* (aucune donnée utilisateur).


        ---
        ### 🗺️ Étude de marché
        Avant de commencer, nous avons étudié les habitudes de consommation cinématographique des habitants de la Creuse.  
        Cette démarche nous a aidés à cibler différents éléments au sein du public.

        ---
        ### 📊 Analyse filmographique
        Ensuite, nous avons exploré la base de données pour :
        - Identifier les acteurs les plus présents au fil des décennies
        - Étudier l’évolution de la durée des films
        - Comparer les acteurs présents au cinéma et dans les séries
        - Calculer l’âge moyen des acteurs
        - Repérer les films les mieux notés et ce qu’ils ont en commun

        ---

        👉 La suite ? Intégrer la recommandation et le système de notification personnalisée.
        """
)
