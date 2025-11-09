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

    

    def _content_based_score(self, user_id, story_ids):
        """Calculate content-based recommendation scores"""
        user = self.users[self.users['user_id'] == user_id].iloc[0]

        # Get user preferences
        preferred_genres = user['preferred_genres'].split('|')
        preferred_characters = user['preferred_characters'].split('|')
        preferred_emotions = user['preferred_emotions'].split('|')
        age_range = user['age_range']
        reading_time_min = user['reading_time_min']
        reading_time_max = user['reading_time_max']

        scores = []
        for story_id in story_ids:
            story = self.stories[self.stories['story_id'] == story_id].iloc[0]
            score = 0

            # 1. Genre match (weight: 0.25)
            story_genres = story['genre'].split('|') if isinstance(story['genre'], str) else []
            genre_matches = sum(1 for genre in preferred_genres if any(g.strip().lower() in genre.lower() for g in story_genres))
            genre_score = min(genre_matches / len(preferred_genres), 1.0) * 0.25
            score += genre_score

            # 2. Character match (weight: 0.20)
            story_tags = story['tags'].lower() if isinstance(story['tags'], str) else ''
            character_matches = sum(1 for char in preferred_characters if char.lower() in story_tags)
            character_score = min(character_matches / len(preferred_characters), 1.0) * 0.20
            score += character_score

            # 3. Emotion/Theme match (weight: 0.20)
            emotion_matches = sum(1 for emotion in preferred_emotions if emotion.lower() in story_tags)
            emotion_score = min(emotion_matches / len(preferred_emotions), 1.0) * 0.20
            score += emotion_score

            # 4. Age appropriateness (weight: 0.20)
            age_match = story['age_range'] == age_range
            if age_match:
                score += 0.20
            else:
                # Partial match for adjacent age ranges
                score += 0.10

            # 5. Reading time match (weight: 0.10)
            reading_time = story['reading_time_minutes']
            if reading_time_min <= reading_time <= reading_time_max:
                score += 0.10
            elif abs(reading_time - reading_time_min) <= 2 or abs(reading_time - reading_time_max) <= 2:
                score += 0.05

            # 6. Popularity boost (weight: 0.05)
            score += story['popularity_score'] * 0.05

            scores.append(score)

        return np.array(scores)

    def _collaborative_score(self, user_id, story_ids):
        """Calculate collaborative filtering scores"""
        if user_id not in self.user_similarity_df.index:
            return np.zeros(len(story_ids))

        # Find similar users
        similar_users = self.user_similarity_df[user_id].sort_values(ascending=False)[1:11]  # Top 10 similar users

        if len(similar_users) == 0:
            return np.zeros(len(story_ids))

        scores = []
        for story_id in story_ids:
            # Average interaction score from similar users
            if story_id in self.user_item_matrix.columns:
                similar_user_scores = self.user_item_matrix.loc[similar_users.index, story_id]
                weighted_score = (similar_user_scores * similar_users.values).sum() / similar_users.sum()
                scores.append(weighted_score)
            else:
                scores.append(0)

        return np.array(scores)

    def _behavioral_score(self, user_id, story_ids):
        """Calculate scores based on user behavior patterns"""
        user_history = self.history[self.history['user_id'] == user_id]

        if len(user_history) == 0:
            return np.zeros(len(story_ids))

        # Analyze user's reading patterns
        avg_completion_rate = user_history['reading_progress'].mean() / 100
        like_rate = user_history['liked'].mean()
        # Get stories user has engaged with
        highly_engaged_stories = user_history[
            (user_history['completed'] == True) &
            (user_history['liked'] == True)
        ]['story_id'].tolist()

        scores = []
        for story_id in story_ids:
            score = 0

            # Similar to previously liked stories (genre/tag similarity)
            if len(highly_engaged_stories) > 0:
                story = self.stories[self.stories['story_id'] == story_id].iloc[0]
                story_genres = set(story['genre'].split('|')) if isinstance(story['genre'], str) else set()
                story_tags = set(story['tags'].lower().split(',')) if isinstance(story['tags'], str) else set()

                for engaged_story_id in highly_engaged_stories[:5]:  # Check top 5
                    if engaged_story_id in self.stories['story_id'].values:
                        engaged_story = self.stories[self.stories['story_id'] == engaged_story_id].iloc[0]
                        engaged_genres = set(engaged_story['genre'].split('|')) if isinstance(engaged_story['genre'], str) else set()
                        engaged_tags = set(engaged_story['tags'].lower().split(',')) if isinstance(engaged_story['tags'], str) else set()

                        # Genre overlap
                        genre_overlap = len(story_genres.intersection(engaged_genres)) / max(len(story_genres), 1)
                        score += genre_overlap * 0.15

                        # Tag overlap
                        tag_overlap = len(story_tags.intersection(engaged_tags)) / max(len(story_tags), 1)
                        score += tag_overlap * 0.10

            # Boost based on user's engagement level
            score += avg_completion_rate * 0.10
            score += like_rate * 0.10

            scores.append(min(score, 1.0))  # Cap at 1.0

        return np.array(scores)

    def _filter_already_read(self, user_id, story_ids):
        """Remove stories user has already completed"""
        user_history = self.history[
            (self.history['user_id'] == user_id) &
            (self.history['completed'] == True)
        ]
        completed_stories = set(user_history['story_id'].tolist())

        return [sid for sid in story_ids if sid not in completed_stories]

    def recommend_stories(self, user_id, n_recommendations=10, exclude_read=True):
        """
        Generate personalized story recommendations

        Args:
            user_id: User ID
            n_recommendations: Number of recommendations to return
            exclude_read: Whether to exclude already read stories

        Returns:
            DataFrame with recommended stories and scores
        """
        # Get all available stories
        all_story_ids = self.stories['story_id'].tolist()

        # Filter out already read stories if requested
        if exclude_read:
            candidate_stories = self._filter_already_read(user_id, all_story_ids)
        else:
            candidate_stories = all_story_ids

        if len(candidate_stories) == 0:
            print(f"User {user_id} has read all available stories!")
            candidate_stories = all_story_ids  # Fall back to all stories

        # Calculate scores from different approaches
        content_scores = self._content_based_score(user_id, candidate_stories)
        collab_scores = self._collaborative_score(user_id, candidate_stories)
        behavioral_scores = self._behavioral_score(user_id, candidate_stories)

        # Combine scores with weights
        # Content: 45%, Collaborative: 30%, Behavioral: 25%
        final_scores = (
            content_scores * 0.45 +
            collab_scores * 0.30 +
            behavioral_scores * 0.25
        )
        # Create recommendations dataframe
        recommendations = pd.DataFrame({
            'story_id': candidate_stories,
            'recommendation_score': final_scores,
            'content_score': content_scores,
            'collaborative_score': collab_scores,
            'behavioral_score': behavioral_scores
        })

        # Merge with story details
        recommendations = recommendations.merge(
            self.stories[['story_id', 'title', 'genre', 'tags', 'reading_time', 'age_range',
                         'views', 'likes', 'image_url', 'url']],
            on='story_id',
            how='left'
        )

        # Sort by recommendation score
        recommendations = recommendations.sort_values('recommendation_score', ascending=False).head(n_recommendations)
        return recommendations