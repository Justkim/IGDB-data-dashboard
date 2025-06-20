import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
from os import path


def get_recommended_games(user_input):
    games_df = pd.read_csv('data.csv')


    # # Filter games where the name appears in the title (case-insensitive)
    # matching_games = games_df[games_df['name'].str.contains(name, case=False, na=False)]
    games_df['release_year'] = pd.to_datetime(games_df['first_release_date'], unit='s').dt.year




    # print(games_df.columns)
    # print(games_df['summary'].count())
    # print(games_df[games_df['summary'].notnull()].sample(5).summary)
    # print()
    # print(games_df[games_df['storyline'].notnull()].sample(5).storyline)
    games_df = games_df.dropna(subset=['summary', 'storyline'], how='all')
    games_df['description'] = games_df['summary'].fillna('') + ' ' + games_df['storyline'].fillna('')

    plots = games_df['description'].tolist()

    # Load Sentence-BERT model (e.g., 'all-MiniLM-L6-v2' is fast and effective)
    model_name = 'all-mpnet-base-v2'
    model = SentenceTransformer(model_name)
    if path.exists('{}_plot_embeddings.npy'.format(model_name)):
        plot_embeddings = np.load('{}_plot_embeddings.npy'.format(model_name))
    else:
        plot_embeddings = model.encode(plots, show_progress_bar=True)
        np.save('{}_plot_embeddings.npy'.format(model_name), plot_embeddings)
    # User input
    user_input = input()
    user_embedding = model.encode([user_input])
    # Compute similarity
    similarity_scores = cosine_similarity(user_embedding, plot_embeddings).flatten()
    # Get top 5 recommendations\

    top_indices = similarity_scores.argsort()[-10:][::-1]
    # print(games_df.iloc[top_indices])
    recommendations = games_df.iloc[top_indices]['name'].tolist()
    # for recommendation in recommendations:
    #     if "horizon" in recommendation.lower():
    #         print("Found a match:", recommendation)
    #         print(similarity_scores[top_indices][recommendations.index(recommendation)])

    # print("Recommended games:", recommendations)

    return recommendations




    # Initialize TF-IDF vectorizer
    # vectorizer = TfidfVectorizer(stop_words='english')
    # tfidf_matrix = vectorizer.fit_transform(plots)

    # # User input
    # user_input = "I want to play as a young girl in a dystopian era"
    # user_tfidf = vectorizer.transform([user_input])

    # # Compute similarity
    # similarity_scores = cosine_similarity(user_tfidf, tfidf_matrix).flatten()

    # # Get top 5 recommendations
    # top_indices = similarity_scores.argsort()[-5:][::-1]
    # recommendations = games_df.iloc[top_indices]['name'].tolist()

    # print("Recommended games:", recommendations)