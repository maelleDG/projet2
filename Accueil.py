from streamlit_option_menu import option_menu
import streamlit as st

st.set_page_config(page_title="Projet2", page_icon="🎥", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>🎥 Bienvenue à notre Projet 2</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h2 style='text-align: center;'> Par Antoine, Evi, Marie et Maëlle</h2>",
    unsafe_allow_html=True,
)

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
        - Identifier le top 10 des acteurs/actrices les plus représentatifs
        - Identifier les genres dominants pour les acteurs/actrices
        - Étudier l’évolution de la durée des films
        - Identifier le top 10 des films les mieux notés

        ---

        👉 La suite ? Intégrer la recommandation et le système de notification personnalisée.
        """
)
