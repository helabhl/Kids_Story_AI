# recommendation_system.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

class StoryRecommendationSystem:
    def __init__(self, stories_df, users_df, history_df):
        self.stories = stories_df.copy()
        self.users = users_df.copy()
        self.history = history_df.copy()
        self._preprocess_data()
        self._build_user_item_matrix()
        self._calculate_user_similarity()

    def _preprocess_data(self):
        if 'reading_time' in self.stories.columns and self.stories['reading_time'].dtype == 'object':
            self.stories['reading_time_minutes'] = self.stories['reading_time'].str.extract('(\d+)').astype(float)
        else:
            self.stories['reading_time_minutes'] = self.stories.get('reading_time', pd.Series(0))

        scaler = MinMaxScaler()
        self.stories['views_normalized'] = scaler.fit_transform(self.stories[['views']].fillna(0))
        self.stories['likes_normalized'] = scaler.fit_transform(self.stories[['likes']].fillna(0))
        self.stories['popularity_score'] = (self.stories['views_normalized'] * 0.4 +
                                            self.stories['likes_normalized'] * 0.6)

    def _build_user_item_matrix(self):
        self.history['liked'] = self.history['liked'].fillna(False)
        self.history['rating'] = self.history['rating'].fillna(3)
        self.history['reading_progress'] = self.history['reading_progress'].fillna(0)

        self.history['interaction_score'] = (
            (self.history['reading_progress'] / 100) * 0.3 +
            self.history['liked'].astype(float) * 0.3 +
            (self.history['rating'] / 5) * 0.2 +
            self.history['completed'].astype(float) * 0.2
        )

        self.user_item_matrix = self.history.pivot_table(
            index='user_id', columns='story_id', values='interaction_score', fill_value=0
        )

    def _calculate_user_similarity(self):
        if len(self.user_item_matrix) > 1:
            sim = cosine_similarity(self.user_item_matrix)
            self.user_similarity_df = pd.DataFrame(sim, index=self.user_item_matrix.index, columns=self.user_item_matrix.index)
        else:
            self.user_similarity_df = pd.DataFrame()

    # ... (toutes les autres méthodes de ta classe, copiez-les ici sans modification majeure) ...

    def recommend_stories(self, user_id, n_recommendations=10, exclude_read=True):
        # implémentation identique à la tienne, mais ajoute vérification user exists
        if user_id not in self.users['user_id'].values:
            raise ValueError(f"User {user_id} not found")
        # ... le reste de la logique ...
        # Retourner un DataFrame
        # Pour l'exemple simplifié, retournons les top n par popularity
        df = self.stories.sort_values('popularity_score', ascending=False).head(n_recommendations)
        return df[['story_id','title','genre','tags','reading_time','age_range','views','likes','image_url','url']]
