# Mealer
Mealer created for the python final project at the university

Smart Recipe Matching - TF-IDF algorithm matches your ingredients to 20+ authentic recipes from 4 cuisines (Kazakh, Italian, French, American)
AI Food Grading - MobileNetV2(tensorflow) analyzes your cooking photos and provides instant feedback
Nutrition Visualization - Interactive charts showing calories, protein, carbs, and fat after the meal was generated
Filter Options - Filter by cuisine type, cooking style, and dietary preferences (vegan)
Responsive UI - Works seamlessly on mobile, tablet, and desktop devices

1. Meal Recommender (TF-IDF + Cosine Similarity)
Analyzes ingredient lists using TF-IDF vectorization
Matches user ingredients to recipe database using cosine similarity
Returns top recommendations with match percentage scores
Handles empty inputs and provides meaningful fallbacks
2. Image Grader (MobileNetV2)
Compares user food photos against reference dish images
Uses feature extraction and cosine similarity for grading
Provides human-readable feedback ("Perfect Manti!", "Needs work...")
Fallback simulation mode when TensorFlow unavailable (ensures app never crashes)

Steps to run the Mealer:
1: Download the zip and unzip it in a accurate folder;
2: In bash to in specific directory where Mealer was download;
3: Run the command "pip intall -r requirements.txt";
4: Run the command "python app.py" and the url will appear as 127.0.0.0/8000;
5: Open the link via control+click.

Architecture of mealer:
App/
│
├── .venv/                     
├── __pycache__/               
│
├── reference_images/          
├── uploads/                   
├── templates/                 
│   ├── index.html
│   ├── result.html
│   └── grade.html
│
├── app.py                     
├── database.py                
├── init_db.py                 
├── image_grader.py            
├── meal_recommender.py        
│
├── meals.db                   
│
├── requirements.txt           
├── README.md                  
├── LICENSE                    
└── .gitignore                 
