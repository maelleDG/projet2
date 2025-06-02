import pandas as pd
import duckdb as db
from datetime import datetime
import numpy as np

con = db.connect()

# --- Analyse filmographique Thème acteur ---

# Top 10 des acteurs et actrices sur les 50 dernières années sur le films dont la note moyenne est supérieure à 6.8 et le nombre de votant supérieur à 675.---

# Création de la table complète avant filtre
query = """select T1.nconst, T1.primaryName, T1.birthYear, T1.deathYear, T1.knownForTitles,
T2.category, T2.job, T2.ordering, T2.characters, T3.tconst, T3.primaryTitle, T3.originalTitle, T3.startYear, T3.runtimeMinutes, 
T3.genres, T4.averageRating, T4.numVotes
from name.basics.tsv as T1
join title.principals.tsv as T2 on T1.nconst = T2.nconst
join title.basics.tsv as T3 on T2.tconst = T3.tconst
join title.ratings.tsv as T4 on T3.tconst = T4.tconst
where isAdult = 0 and titleType = 'movie'
"""
df_a = con.execute(query).df()

# Remplacer des \N par None
df_a.replace({"\\N": None}, inplace=True)
# Supprimer les lignes où la colonne 'Genres' contient None
df_a.dropna(subset=["genres"], inplace=True)
# Supprimer les lignes où la colonne 'runTimeMinutes' contient None
df_a.dropna(subset=["runtimeMinutes"], inplace=True)
# Supprimer les lignes où la colonne 'startYear' contient None
df_a.dropna(subset=["startYear"], inplace=True)

# Convertir 'startYear' en numériques et en type nullable integer (Int64)
df_a["startYear"] = pd.to_numeric(df_a["startYear"], errors="coerce").astype("Int64")
# Convertir 'runtimeMinutes' en numériques et en type nullable integer (Int64)
df_a["runtimeMinutes"] = pd.to_numeric(df_a["runtimeMinutes"], errors="coerce").astype(
    "Int64"
)

# Nettoyage de la colonne runtimeMinute
Q1 = df_a["runtimeMinutes"].quantile(0.25)
Q3 = df_a["runtimeMinutes"].quantile(0.75)
IQR = Q3 - Q1
borne_inf = Q1 - 1.5 * IQR
borne_sup_iqr = Q3 + 1.5 * IQR

df_a2 = df_a[
    (df_a["runtimeMinutes"] >= borne_inf) & (df_a["runtimeMinutes"] <= borne_sup_iqr)
]
df_a = df_a2  # Mise à jour du DF

# Pour l'analyse on garde les 50 dernières années
df_a50 = df_a[df_a["startYear"] >= 1975]

# On conserve les valeurs actrices/acteurs/directeurs de la colonne category
categories_to_keep = ["actress", "actor", "director"]
df_a50 = df_a50[df_a50["category"].isin(categories_to_keep)]

# Pour l'analyse on garde les films dont l'averagerating > 6.8
df_a50_ar6 = df_a50[df_a50["averageRating"] > 6.8]

# Pour l'analyse on garde les films dont le numVote > 675
df_a50_ar6_nv675 = df_a50[df_a50["numVotes"] > 675]

# Création du fichier
try:
    df_a50_ar6_nv675.to_parquet(
        "Top10acteurs", index=False
    )  # index=False est souvent une bonne pratique pour Parquet
    print("\nDataFrame 'df_a50_ar6_nv675' sauvegardé avec succès au format Parquet.")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde au format Parquet : {e}")


# ---

# Création de data1_filtered

query = """
select * from name.basics.tsv
"""
data1 = con.execute(query).df()
# --- Section de nettoyage et préparation initiale de data1 ---
# Remplacer '\\N' par np.nan dans tout le DataFrame pour une gestion standard des valeurs manquantes
data1.replace({"\\N": np.nan}, inplace=True)
# Convertir 'birthYear' et 'deathYear' en numériques et en type nullable integer (Int64)
# Les erreurs seront converties en NaN (qui est géré par Int64)
data1["birthYear"] = pd.to_numeric(data1["birthYear"], errors="coerce").astype("Int64")
data1["deathYear"] = pd.to_numeric(data1["deathYear"], errors="coerce").astype("Int64")
current_year = datetime.now().year
# --- Calcul des âges ---
# Initialiser les colonnes d'âge avec pd.NA pour Int64
data1["age_deces"] = pd.NA
data1["age_actuel"] = pd.NA
# Calcul de l'âge de décès : pour les personnes ayant une année de décès renseignée (non-NaN)
# Utiliser .loc avec un masque pour éviter les SettingWithCopyWarning
mask_deces = data1["deathYear"].notna()
data1.loc[mask_deces, "age_deces"] = (
    data1.loc[mask_deces, "deathYear"] - data1.loc[mask_deces, "birthYear"]
)
# Calcul de l'âge actuel : pour les personnes vivantes (année de décès est NaN)
# Utiliser .loc avec un masque pour éviter les SettingWithCopyWarning
mask_vivant = data1["deathYear"].isna()
data1.loc[mask_vivant, "age_actuel"] = (
    current_year - data1.loc[mask_vivant, "birthYear"]
)
# Assurez-vous que les colonnes d'âge sont du type Int64 (nullable integer)
data1["age_deces"] = data1["age_deces"].astype("Int64")
data1["age_actuel"] = data1["age_actuel"].astype("Int64")


# Suppression des outliers
def limite_iqr(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    borne_inf = Q1 - 1.5 * IQR
    borne_sup_iqr = Q3 + 1.5 * IQR
    return borne_inf, borne_sup_iqr


# Obtention des limites pour les âges de décès
ages_deces_valide = data1["age_deces"].dropna()
if not ages_deces_valide.empty:
    borne_inf_deces, borne_sup_iqr_deces = limite_iqr(ages_deces_valide)
else:
    borne_inf_deces, borne_sup_iqr_deces = -np.inf, np.inf
# Obtention des limites pour les âges actuels
ages_actuels_valide = data1["age_actuel"].dropna()
if not ages_actuels_valide.empty:
    borne_inf_actuel, borne_sup_iqr_actuel = limite_iqr(ages_actuels_valide)
else:
    borne_inf_actuel, borne_sup_iqr_actuel = -np.inf, np.inf
# Création d'un masque pour les lignes qui NE SONT PAS des outliers
# Une ligne est conservée si :
# 1. Elle est décédée ET son âge de décès est dans les limites IQR
# OU
# 2. Elle est en vie ET son âge actuel est dans les limites IQR
non_outlier_mask = (
    data1["age_deces"].notna()
    & (data1["age_deces"] >= borne_inf_deces)
    & (data1["age_deces"] <= borne_sup_iqr_deces)
) | (
    data1["age_actuel"].notna()
    & (data1["age_actuel"] >= borne_inf_actuel)
    & (data1["age_actuel"] <= borne_sup_iqr_actuel)
)
# Filtrer data1 pour supprimer les outliers ET inclure uniquement les acteurs/actrices
# Cette étape combine les deux filtrages finaux de 'data1' pour créer 'data1_filtered'
data1_filtered = data1[
    non_outlier_mask
    & data1["primaryProfession"].str.contains(
        "actor|actress", case=False, na=False, regex=True
    )
].copy()  # Utiliser .copy() pour éviter les SettingWithCopyWarning

# Création de titles_df

query = """
select * from title.basics.tsv
"""
titles_df = con.execute(query).df()

# --- Préparation des tables avant la jointure ---

# Filtrer pour inclure uniquement les acteurs/actrices ET supprimer les NaN dans 'knownForTitles'
# La colonne data1["primaryProfession"] a déjà été utilisée pour créer data1_filtered.
# Ici, nous partons de data1_filtered pour ne conserver que les acteurs valides avec knownForTitles.
acteurs_df_cleaned = data1_filtered.dropna(subset=["knownForTitles"]).copy()
# Appliquez la conversion de chaîne et le remplacement sur cette copie propre
acteurs_df_cleaned.loc[:, "knownForTitles"] = (
    acteurs_df_cleaned["knownForTitles"].astype(str).replace("nan", "")
)
# Éclater 'knownForTitles'
# Chaque ligne représentera un acteur associé à UN SEUL titre connu.
acteurs_expanded_titles = acteurs_df_cleaned.assign(
    tconst=acteurs_df_cleaned["knownForTitles"].str.split(",")
).explode("tconst")
acteurs_expanded_titles["tconst"] = acteurs_expanded_titles[
    "tconst"
].str.strip()  # Supprimer les espaces blancs autour des tconst
# Supprimer les lignes où tconst est vide après le split (ex: si 'knownForTitles' était ',,')
acteurs_expanded_titles = acteurs_expanded_titles[
    acteurs_expanded_titles["tconst"] != ""
]
# SÉLECTIONNER LES COLONNES POUR actors_expanded_titles avant la jointure principale
# Pour s'assurer que seules les colonnes avec les types de données appropriés sont incluses
# et éviter les colonnes redondantes ou de type problématique pour le parquet.
acteurs_expanded_titles = acteurs_expanded_titles[
    [
        "nconst",
        "primaryName",
        "birthYear",
        "deathYear",  # Ces colonnes sont maintenant Int64
        "primaryProfession",
        "age_deces",
        "age_actuel",
        "tconst",
    ]
].copy()  # Utiliser .copy() ici aussi pour être sûr
# Nettoyage et préparation de titles_df (les titres)
titles_df_cleaned = titles_df.copy()  # Travailler sur une copie
# Convertir 'startYear' en numérique et gérer les erreurs (coerce les erreurs en NaN)
titles_df_cleaned["startYear"] = pd.to_numeric(
    titles_df_cleaned["startYear"], errors="coerce"
).astype("Int64")
# Supprimer les lignes où 'startYear' est NaN, car nous en avons besoin pour la décennie et les analyses temporelles
titles_df_cleaned = titles_df_cleaned.dropna(subset=["startYear"])
# Calculer la décennie
titles_df_cleaned["decade"] = (titles_df_cleaned["startYear"] // 10 * 10).astype(int)

# Jointure des deux dataframes

# Joindre 'acteurs_expanded_titles' avec 'titles_df_cleaned' sur 'tconst'.
# Cela va créer un dataframe où chaque ligne est une association acteur-titre
# avec toutes les informations pertinentes des deux côtés.
acteurs_complet_df = pd.merge(
    acteurs_expanded_titles,
    titles_df_cleaned[
        ["tconst", "primaryTitle", "titleType", "startYear", "genres", "decade"]
    ],
    on="tconst",
    how="inner",  # Utilisez inner pour ne garder que les correspondances valides dans les deux jeux de données
)
# Ajout de colonnes d'analyse (Cinéma/Séries)
# Ajout de flags pour faciliter le regroupement par type de production
acteurs_complet_df["is_movie"] = acteurs_complet_df["titleType"] == "movie"
acteurs_complet_df["is_tv_series"] = acteurs_complet_df["titleType"] == "tvSeries"

# Gestion des \N de la colonne genre sur le df finale
acteurs_complet_df.replace({"\\N": None}, inplace=True)
# Supprimer les lignes où la colonne 'Genres' contient None
acteurs_complet_df.dropna(subset=["genres"], inplace=True)

# Nomination des colonnes pour le dataframe final
acteurs_complet_df = acteurs_complet_df.rename(
    columns={
        "nconst": "ID_Acteur",
        "primaryName": "Nom",
        "birthYear": "Annee_naissance",
        "deathYear": "Annee_deces",
        "primaryProfession": "Profession",
        "age_deces": "Age_deces",
        "age_actuel": "Age_actuel",
        "tconst": "ID_titre",
        "primaryTitle": "Titre",
        "titleType": "Type",
        "startYear": "Annee_sortie",
        "genres": "Genres",
        "is_movie": "Film?",
        "is_tv_series": "Serie?",
    }
)

# Base de données des acteurs complète

try:
    acteurs_complet_df.to_parquet(
        "acteurs.parquet", index=False
    )  # index=False est souvent une bonne pratique pour Parquet
    print("\nDataFrame 'acteurs_complet_df' sauvegardé avec succès au format Parquet.")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde au format Parquet : {e}")


# Vous avez maintenant 'acteurs_complet_df' qui est votre dataframe pour toutes les analyses futures.
# Il contient:
# - Informations sur l'acteur (nconst, primaryName, birthYear, deathYear, primaryProfession, age_deces, age_actuel)
# - L'identifiant du titre (tconst)
# - Informations sur le titre (primaryTitle, titleType, startYear, genres, decade)
# - Indicateurs is_movie et is_tv_series

# --- Exemple d'analyse que vous pouvez faire avec ce dataframe ---

# 1. Nombre de films/séries par acteur
# print("\nNombre de films/séries par acteur (Top 10) :")
# print(acteurs_complet_df['primaryName'].value_counts().head(10))

# 2. Acteurs uniques qui ont joué dans des films
# print("\nActeurs uniques ayant joué dans des films (Top 10) :")
# print(acteurs_complet_df[acteurs_complet_df['is_movie']]['primaryName'].nunique())

# 3. Répartition des genres par décennie pour les films d'acteurs
# print("\nRépartition des genres de films par décennie (Top 5 genres pour 2000s) :")
# film_genres_2000s = acteurs_complet_df[(acteurs_complet_df['is_movie']) & (acteurs_complet_df['decade'] == 2000)]
# print(film_genres_2000s['genres'].str.split(',').explode().value_counts().head())

# --- Thème film ---

# Création de film_fr_tmdb
query = """
SELECT *
from tmdb_full.csv 
where adult = 'False'
"""
film_notadult = con.execute(query).df()
# Nettoyage du df sur runtime
Q1 = film_notadult["runtime"].quantile(0.25)
Q3 = film_notadult["runtime"].quantile(0.75)
IQR = Q3 - Q1
borne_inf = Q1 - 1.5 * IQR
borne_sup_iqr = Q3 + 1.5 * IQR
# Créez une COPIE explicite ici pour garantir l'indépendance
film_notadult_cleaned = film_notadult[
    (film_notadult["runtime"] >= borne_inf)
    & (film_notadult["runtime"] <= borne_sup_iqr)
].copy()
film_notadult = (
    film_notadult_cleaned  # Mise à jour de votre DataFrame avec les données nettoyées
)
# Suppression de la ligne dont le status = canceled
# Utilisez .copy() ici aussi si cette opération est susceptible de créer une vue
film_notadult = film_notadult[
    ~film_notadult["status"].str.contains("Canceled", case=True)
].copy()
# Suppression de la colonne adult
film_notadult.drop(columns="adult", inplace=True)
# Création d'un DataFrame contenant que les films dont spoken_language = fr
film_fr_tmdb = film_notadult[
    film_notadult["spoken_languages"].str.contains("'fr'", regex=False)
]
# Traitement des genres
lignes_avec_fr_vide = film_fr_tmdb[film_fr_tmdb["genres"] == "[]"]
# Supposons que 'lignes_avec_fr_vide' contienne les lignes à supprimer
indices_a_supprimer = lignes_avec_fr_vide.index
# Supprimer les lignes du dataframe original en utilisant les indices
film_fr_tmdb = film_fr_tmdb.drop(indices_a_supprimer)
new_genres = []
for var in film_fr_tmdb["genres"]:
    liste = eval(var)
    new_genres.append(liste)
film_fr_tmdb["genres"] = new_genres
film_fr_tmdb["genres"] = film_fr_tmdb["genres"].astype(str).str.replace("[", "[ ")
film_fr_tmdb["genres"] = film_fr_tmdb["genres"].astype(str).str.replace("]", " ]")
# Suppression des TVmovie
tv_movies = film_fr_tmdb[film_fr_tmdb["genres"].apply(lambda x: "TV Movie" in x)]
# Supprimer les films qui ont le genre 'TV Movie' du DataFrame original
film_fr_tmdb = film_fr_tmdb.drop(tv_movies.index)
# Enregistrement du dataset
try:
    film_fr_tmdb.to_parquet(
        "film_fr_tmdb.parquet", index=False
    )  # index=False est souvent une bonne pratique pour Parquet
    print("\nDataFrame 'film_fr_tmdb' sauvegardé avec succès au format Parquet.")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde au format Parquet : {e}")

con.close()
