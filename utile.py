import pandas as pd
import duckdb as db
from datetime import datetime
import numpy as np
import ast

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
df_a2 = df_a[(df_a["runtimeMinutes"] >= 70) & (df_a["runtimeMinutes"] <= 200)]
df_a = df_a2  # Mise à jour du DF

# Pour l'analyse on garde les 50 dernières années
df_a50 = df_a[df_a["startYear"] >= 1975]


# On conserve les valeurs actrices/acteurs/directeurs de la colonne category
categories_to_keep = ["actress", "actor", "director"]
df_a50 = df_a50[df_a50["category"].isin(categories_to_keep)]

# Pour l'analyse on garde les films dont l'averagerating > 6.8
df_a50_ar6 = df_a50[df_a50["averageRating"] > 6.8]

# Pour l'analyse on garde les films dont le numVote > 80000
df_a50_ar6_nv675 = df_a50[df_a50["numVotes"] > 80000]

# Création du fichier
try:
    df_a50_ar6_nv675.to_parquet(
        "Top10acteurs", index=False
    )  # index=False est souvent une bonne pratique pour Parquet
    print("\nDataFrame 'df_a50_ar6_nv675' sauvegardé avec succès au format Parquet.")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde au format Parquet : {e}")

# ---

# --- Analyse filmographique Thème film ---

# Création du fichier
try:
    df_a50.to_parquet(
        "Duree_film", index=False
    )  # index=False est souvent une bonne pratique pour Parquet
    print("\nDataFrame 'Duree_film' sauvegardé avec succès au format Parquet.")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde au format Parquet : {e}")


# --- Recommandation ---

# Création du fichier reco_full

query = """
with ActeursParFilm as (
    select tp.tconst, group_concat(nb.primaryName, ', ') as NomsActeurs
    from title.principals.tsv as tp
    join name.basics.tsv as nb on tp.nconst = nb.nconst
    where tp.category in ('actor', 'actress')
    group by tp.tconst
    ),
    RealisateursParFilm as (
    select tp.tconst, group_concat(nb.primaryName, ', ') as NomsRealisateurs
    from title.principals.tsv as tp
    join name.basics.tsv as nb on tp.nconst = nb.nconst
    where tp.category = 'director'
    group by tp.tconst
    )
select tf.*, apf.NomsActeurs, rpf.NomsRealisateurs
from tmdb_full.csv as tf
left join ActeursParFilm as apf on tf.imdb_id = apf.tconst
left join RealisateursParFilm as rpf on tf.imdb_id = rpf.tconst
where tf.adult = False
and tf.status IN ('Released', 'In Production', 'Post Production')
and tf.runtime BETWEEN 70 AND 220
and tf.spoken_languages like '%fr%'
"""
df = con.execute(query).df()
# Suppression des colonnes qui ne serviront pas
df.drop(
    ["adult", "production_companies_country", "homepage", "video", "tagline"],
    axis=1,
    inplace=True,
)
# Remplacer des \N par None
df.replace({"\\N": None}, inplace=True)
# Supprimer les lignes où 'release_date' est nulle
df.dropna(subset=["release_date"], inplace=True)
# Remplacement des valeurs none en liste vide pour overview
df["overview"] = df["overview"].fillna("")
# Création d'une colonne décennie
# Calculez l'année, divisez par 10, prenez la partie entière, multipliez par 10
df["decennie"] = (df["release_date"].dt.year // 10) * 10
# Et on garde seulement les films à partir de 1960
df = df[df["decennie"] >= 1960]


# On crée une colonne qui comprend les noms et prénoms collés
# Fonction pour transformer une liste de noms
def transformer_noms(liste_noms_str):
    if pd.isna(liste_noms_str) or not liste_noms_str.strip():
        return None  # Ou une chaîne vide, selon ce que vous préférez pour les valeurs manquantes
    # Séparer la chaîne en noms individuels par la virgule
    noms_individuels = [nom.strip() for nom in liste_noms_str.split(",")]
    # Transformer chaque nom (remplacer les espaces par des underscores)
    noms_colles = [nom.replace(" ", "_") for nom in noms_individuels]
    # Rejoindre les noms transformés avec une virgule et un espace
    return ", ".join(noms_colles)


# Appliquer la fonction aux colonnes 'NomsActeurs' et 'NomsRealisateurs'
df["NomsActeurs_colle"] = df["NomsActeurs"].apply(transformer_noms)
df["NomsRealisateurs_colle"] = df["NomsRealisateurs"].apply(transformer_noms)


# Fonction pour nettoyer et joindre les genres
def nettoyer_genre(genre_str):
    if pd.isna(genre_str) or not genre_str.strip():
        return None  # Ou une chaîne vide si vous préférez
    # Évaluer la chaîne comme une liste Python (si elle est au format '[genre1, genre2]')
    try:
        genre_list = ast.literal_eval(genre_str)
    except (ValueError, SyntaxError):
        # Si ce n'est pas une chaîne de liste valide, traitez-la comme une chaîne simple
        # Par exemple, si c'est juste 'Comedy' sans crochets
        genre_list = [genre_str.strip()]
    # Assurez-vous que c'est bien une liste
    if not isinstance(genre_list, list):
        genre_list = [
            str(genre_list).strip()
        ]  # Convertir en liste si ce n'était pas une liste
    # Nettoyer chaque genre (supprimer les espaces) et joindre
    # Vous pouvez ajouter .replace(' ', '_') si vous voulez coller les mots dans un même genre (ex: 'Science Fiction' -> 'Science_Fiction')
    # Mais d'habitude les genres sont des mots simples ou des paires.
    genres_propres = [
        g.strip().replace(" ", "_") for g in genre_list if g.strip()
    ]  # Optionnel: coller les mots dans le genre
    return ", ".join(genres_propres) if genres_propres else None


# Appliquer la fonction à la colonne 'genre'
df["genre_propre"] = df["genres"].apply(nettoyer_genre)


# Fonction pour nettoyer et joindre les noms de compagnies de production
def nettoyer_compagnies(compagnies_str):
    if pd.isna(compagnies_str) or not compagnies_str.strip():
        return None  # Retourne None pour les valeurs manquantes/vides
    try:
        # Tente d'évaluer la chaîne comme une liste Python
        compagnies_list = ast.literal_eval(compagnies_str)
    except (ValueError, SyntaxError):
        # Si ce n'est pas une chaîne de liste valide, la traiter comme une chaîne simple
        compagnies_list = [compagnies_str.strip()]
    # S'assurer que le résultat est bien une liste
    if not isinstance(compagnies_list, list):
        compagnies_list = [
            str(compagnies_list).strip()
        ]  # Convertir en liste si ce n'était pas une liste
    # Nettoyer chaque nom de compagnie (supprimer les espaces) et joindre
    # Nous allons aussi remplacer les espaces par des underscores dans les noms de compagnies si elles ont plusieurs mots
    compagnies_propres = [
        c.strip().replace(" ", "_") for c in compagnies_list if c.strip()
    ]
    return ", ".join(compagnies_propres) if compagnies_propres else None


# Appliquer la fonction à la colonne 'production_companies_name'
df["production_companies_name_propre"] = df["production_companies_name"].apply(
    nettoyer_compagnies
)
# Remplacement des valeurs none en liste vide pour production_compagniers_name
df["production_companies_name_propre"] = df["production_companies_name_propre"].fillna(
    ""
)
# Remplacement des valeurs none en liste vide pour NomsActeurs_colle
df["NomsActeurs_colle"] = df["NomsActeurs_colle"].fillna("")
# Remplacement des valeurs none en liste vide pour NomsRealisateurs_colle
df["NomsRealisateurs_colle"] = df["NomsRealisateurs_colle"].fillna("")
# Remplacement des valeurs none en liste vide pour genre_propre
df["genre_propre"] = df["genre_propre"].fillna("")
# Convertir 'decennie' en chaîne de caractères, car on ne peut concaténer que des chaînes
df["decennie"] = df["decennie"].astype(str)
# Créer la nouvelle colonne combinée
# Nous allons ajouter des séparateurs (par exemple, un espace ou un point-virgule) pour la lisibilité
df["colonne_combine"] = (
    df["overview"]
    + " "
    + df["genre_propre"]
    + " "
    + df["decennie"]
    + " "
    + df["NomsRealisateurs_colle"]
    + " "
    + df["NomsActeurs_colle"]
    + " "
    + df["production_companies_name_propre"]
)
df = df.reset_index(drop=True)

# Création du fichier reco
try:
    df.to_parquet(
        "reco", index=False
    )  # index=False est souvent une bonne pratique pour Parquet
    print("\nDataFrame 'reco' sauvegardé avec succès au format Parquet.")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde au format Parquet : {e}")

# Créer un nouveau DataFrame avec uniquement la colonne 'colonne_combine'
df_combined_text = df[["colonne_combine"]]

try:
    df_combined_text.to_parquet(
        "reco_combinee", index=False
    )  # index=False est souvent une bonne pratique pour Parquet
    print("\nDataFrame 'reco_combinee' sauvegardé avec succès au format Parquet.")
except Exception as e:
    print(f"\nErreur lors de la sauvegarde au format Parquet : {e}")


con.close()
