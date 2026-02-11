# meal_recommender.py - REPLACE ENTIRE FILE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from database import get_all_recipes_with_ingredients
import logging

logger = logging.getLogger(__name__)

class MealRecommender:
    def __init__(self):
        self.recipes = get_all_recipes_with_ingredients()
        
        # CRITICAL FIX: Handle empty database gracefully
        if not self.recipes or len(self.recipes) == 0:
            logger.error(" DATABASE IS EMPTY! No recipes found. Please run 'python init_db.py' first.")
            self.vectorizer = None
            self.tfidf_matrix = None
            self.corpus = []
            return
        
        # Build corpus SAFELY - extract ONLY ingredient names
        self.corpus = []
        valid_recipes = []
        
        for recipe in self.recipes:
            # Extract ingredient names only (skip empty)
            ingredients_text = " ".join([
                ing["name"].strip().lower() 
                for ing in recipe.get("ingredients", [])
                if isinstance(ing, dict) and ing.get("name", "").strip()
            ])
            
            # Skip recipes with no valid ingredients
            if ingredients_text and len(ingredients_text) > 2:
                self.corpus.append(ingredients_text)
                valid_recipes.append(recipe)
            else:
                logger.warning(f" Skipping recipe '{recipe.get('name', 'Unknown')}' - no valid ingredients")
        
        self.recipes = valid_recipes
        
        # CRITICAL FIX: Handle empty corpus AFTER filtering
        if not self.corpus or len(self.corpus) == 0:
            logger.error(" ALL RECIPES HAVE INVALID INGREDIENTS! Check database.")
            self.vectorizer = None
            self.tfidf_matrix = None
            return
        
        # Initialize TF-IDF with safe parameters
        try:
            self.vectorizer = TfidfVectorizer(
                min_df=1,           # Critical: prevent "empty vocabulary" error
                stop_words=None,    # Don't remove ingredient names
                lowercase=True,
                token_pattern=r'(?u)\b\w+\b'  # Match single words (avoid empty tokens)
            )
            self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
            logger.info(f" TF-IDF initialized with {len(self.corpus)} valid recipes")
        except Exception as e:
            logger.error(f" TF-IDF initialization failed: {str(e)}")
            self.vectorizer = None
            self.tfidf_matrix = None
    
    def recommend(self, available_ingredients, top_n=5):
        # Handle uninitialized state
        if self.vectorizer is None or self.tfidf_matrix is None:
            logger.warning(" MealRecommender not initialized - returning empty results")
            return []
        
        # Clean user input
        user_ingredients = [ing.strip().lower() for ing in available_ingredients if ing.strip()]
        if not user_ingredients:
            return []
        
        # Generate recommendations SAFELY
        try:
            user_text = " ".join(user_ingredients)
            user_vector = self.vectorizer.transform([user_text])
            similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
            
            # Get top matches
            top_indices = np.argsort(similarities)[::-1][:top_n]
            recommendations = []
            
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum relevance
                    recipe = self.recipes[idx]
                    recommendations.append({
                        "recipe": recipe,
                        "similarity_score": float(similarities[idx]),
                        "match_percentage": min(100, float(similarities[idx]) * 150)
                    })
            return recommendations
        except Exception as e:
            logger.error(f" Recommendation failed: {str(e)}")
            return []
