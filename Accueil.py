import streamlit as st

st.set_page_config(page_title="Projet2", page_icon="🎥", layout="wide")

col_left_spacer, col_content, col_right_spacer = st.columns([1, 3, 1])
with col_content:
    # À l'intérieur de cette colonne centrale, créez deux colonnes supplémentaires :
    # une pour votre logo et une pour votre texte.
    # Ajustez les ratios [1, 2] pour contrôler la largeur relative du logo et du texte.
    logo_col, text_col = st.columns([1, 2])

    with logo_col:
        # Vous pouvez ajuster la 'width' (largeur) du logo.
        st.image("logo_team.png", width=800)

    with text_col:
        # Le texte est déjà centré horizontalement grâce à 'text-align: center;'.
        # Pour tenter de centrer le bloc de texte verticalement par rapport au logo,
        # nous utilisons un conteneur HTML avec Flexbox. Cela peut aider à aligner
        # le contenu verticalement au centre de la colonne.
        st.markdown(
            """
            <div style='display: flex; flex-direction: column; justify-content: center; height: 100%;'>
                <h1 style='text-align: center; margin-bottom: 0;'>Bienvenue à notre Projet 2</h1>
                <h2 style='text-align: center; margin-top: 0;'> Par Antoine, Evi, Marie et Maëlle</h2>
            </div>
            """,
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
