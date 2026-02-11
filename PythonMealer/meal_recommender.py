from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from database import get_all_recipes_with_ingredients

class MealRecommender:
    def __init__(self):
        self.recipes = get_all_recipes_with_ingredients()
        self.vectorizer = TfidfVectorizer()
        
        # Create corpus from ingredient names only
        corpus = [" ".join([ing["name"] for ing in r["ingredients"]]) for r in self.recipes]
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
    
    def recommend(self, available_ingredients, top_n=5):
        """
        ML: Finds recipes with most similar ingredient profiles
        using TF-IDF + Cosine Similarity
        """
        # Convert user ingredients to TF-IDF vector
        user_text = " ".join(available_ingredients)
        user_vector = self.vectorizer.transform([user_text])
        
        # Calculate similarity scores
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        # Get top N matches
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Minimum relevance threshold
                recipe = self.recipes[idx]
                recommendations.append({
                    "recipe": recipe,
                    "similarity_score": float(similarities[idx]),
                    "match_percentage": min(100, float(similarities[idx]) * 100 * 1.5)
                })
        
        return recommendations