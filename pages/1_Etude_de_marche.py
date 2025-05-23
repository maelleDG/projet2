import streamlit as st
from streamlit_option_menu import option_menu

# Création de 2 colonnes
col1, col2 = st.columns(2)

# Contenu de la première colonne :
with col1:
    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUZzfpnK2Q3sx97u7f_i77J1pr7tNF-_-rKQ&s"
    )

# Contenu de la deuxième colonne :
with col2:
    st.header(
        "Etude de marché sur la consommation de cinéma dans la région de la Creuse"
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
elif selected == "Etude cinématographique":
    st.subheader("Vos données personnelles")
    st.write("Vous pouvez gérer et consulter vos informations ici.")
elif selected == "Conclusion":
    st.subheader("Génération de rapports")
    st.write("Accédez à vos rapports personnalisés.")
