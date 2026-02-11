import os
import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub

# Try to load model - fallback if TensorFlow not available
try:
    MODEL_URL = "https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4"
    model = hub.KerasLayer(MODEL_URL, input_shape=(224, 224, 3))
    TF_AVAILABLE = True
    print("TensorFlow model loaded successfully")
except Exception as e:
    TF_AVAILABLE = False
    print(f"TensorFlow not available (grading will be simulated): {e}")

class ImageGrader:
    def __init__(self, reference_images_dir="reference_images"):
        self.ref_dir = reference_images_dir
        os.makedirs(self.ref_dir, exist_ok=True)
        
        # Pre-load reference features if TensorFlow available
        self.reference_features = {}
        if TF_AVAILABLE:
            self._load_reference_features()
    
    def _load_reference_features(self):
        """Extract features from all reference images"""
        for fname in os.listdir(self.ref_dir):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(self.ref_dir, fname)
                try:
                    features = self._extract_features(img_path)
                    dish_name = os.path.splitext(fname)[0].replace("_", " ").title()
                    self.reference_features[dish_name] = features
                except Exception as e:
                    print(f"Skipping {fname}: {e}")
    
    def _preprocess_image(self, img_path):
        """Resize and normalize image for MobileNetV2"""
        img = Image.open(img_path).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img).astype(np.float32) / 255.0
        return np.expand_dims(img_array, axis=0)
    
    def _extract_features(self, img_path):
        """Extract 1280-dim feature vector using MobileNetV2"""
        img_tensor = self._preprocess_image(img_path)
        features = model(img_tensor)
        return np.array(features[0])
    
    def grade_photo(self, user_image_path, expected_dish=None):
        """
        REAL ML: Compares user photo to reference images using feature similarity
        Returns score 0-100 based on cosine similarity
        """
        if not TF_AVAILABLE:
            return self._simulate_grade(user_image_path, expected_dish)
        
        try:
            # Extract features from user image
            user_features = self._extract_features(user_image_path)
            
            if expected_dish and expected_dish in self.reference_features:
                # Compare to specific dish
                ref_features = self.reference_features[expected_dish]
                similarity = self._cosine_similarity(user_features, ref_features)
                score = min(100, similarity * 110)
                feedback = self._generate_feedback(score, expected_dish)
                return {"score": round(score, 1), "feedback": feedback, "dish": expected_dish}
            
            # Compare to all reference dishes
            best_score = 0
            best_dish = "Unknown"
            
            for dish_name, ref_features in self.reference_features.items():
                similarity = self._cosine_similarity(user_features, ref_features)
                if similarity > best_score:
                    best_score = similarity
                    best_dish = dish_name
            
            score = min(100, best_score * 110)
            feedback = self._generate_feedback(score, best_dish)
            return {"score": round(score, 1), "feedback": feedback, "dish": best_dish}
        
        except Exception as e:
            return {"error": f"Grading failed: {str(e)}"}
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two feature vectors"""
        dot = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot / (norm1 * norm2 + 1e-8)
    
    def _generate_feedback(self, score, dish_name):
        if score >= 90:
            return f"Perfect {dish_name}! Restaurant quality!"
        elif score >= 75:
            return f"Great {dish_name}! Minor plating improvements needed."
        elif score >= 60:
            return f"Edible {dish_name}. Work on presentation and color balance."
        else:
            return f"Needs work. Doesn't closely resemble {dish_name}."
    
    def _simulate_grade(self, img_path, expected_dish):
        """Fallback when TensorFlow not available"""
        import random
        base = random.randint(65, 92)
        if expected_dish and "perfect" in expected_dish.lower():
            base = min(100, base + 8)
        return {
            "score": base,
            "feedback": "SIMULATED GRADE (install TensorFlow for real ML grading)",
            "dish": expected_dish or "Unknown Dish"
        }