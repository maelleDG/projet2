import pandas as pd
import nltk

nltk.download("popular")
nltk.download("stopwords")
nltk.download("punkt_tab")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
from sklearn.feature_extraction.text import CountVectorizer

# Import NN
from sklearn.neighbors import NearestNeighbors
import streamlit as st
import joblib


# Instanciation du Stemmer et chargement du set des stopwords anglais.
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))

# Ajout de mots personnalisés aux stopwords.
mots_supplementaires = [
    "film",
    "movie",
    "production",
    "story",
    "character",
    "director",
    "acteur",
    "actrice",
    "réalisateur",
    "série",
    "tv",
    "show",
    "overview",
    "tagline",
    "genre",
    "compagnie",
    "name",
    "décennie",
    "dans",
    "avec",
    "pour",
    "qui",
    "ce",
    "cette",
    "son",
    "sa",
    "ses",
    "sur",
]
stop_words.update(mots_supplementaires)


# Fonction pour convertir le texte en minuscules.
def lower_case(text: str) -> str:
    return text.lower()


# Fonction pour supprimer les balises HTML du texte.
def remove_html_tags(text: str) -> str:
    return re.sub(r"<.*?>", "", text)


# Fonction pour supprimer les stopwords du texte.
def remove_stopwords(text: str) -> str:
    return " ".join([word for word in text.split() if word not in stop_words])


# Fonction pour supprimer les caractères spéciaux du texte.
def remove_special_char(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text)


# Fonction pour appliquer le stemmer sur le texte.
def stem(text: str) -> str:
    return " ".join([stemmer.stem(word) for word in text.split()])


# Fonction principale qui applique toutes les transformations sur le texte.
def main_clean(review: str) -> str:
    review = lower_case(review)
    review = remove_html_tags(review)
    review = remove_special_char(review)
    review = remove_stopwords(review)
    review = stem(review)
    return review


# Définition des chemins de sauvegarde des modèles
VECTORIZER_PATH = "count_vectorizer.joblib"
NEIGHBORS_MODEL_PATH = "nearest_neighbors_model.joblib"
CLEANED_TEXT_PATH = "cleaned_text_series.joblib"

reco_combinee = pd.read_parquet("reco_combinee")

# On applique la fonction sur la colonne colonne_combine
reco_combinee["colonne_combine"] = reco_combinee["colonne_combine"].apply(main_clean)

# Récupère la série de texte nettoyé.
X = reco_combinee["colonne_combine"]

# Instancie et entraîne le modèle CountVectorizer.
count_vectorizer = CountVectorizer()
X_count = count_vectorizer.fit_transform(X)

# Crée une instance de NearestNeighbors avec 30 voisins et la métrique cosinus.
neigh = NearestNeighbors(n_neighbors=30, metric="cosine")
# Entraîne le modèle NN sur les données vectorisées.
neigh.fit(X_count)

_, indices = neigh.kneighbors(X_count)

joblib.dump(indices, "carto.pkl")
print("Tableau sauvegardé avec succès sous 'carto.pkl'")
