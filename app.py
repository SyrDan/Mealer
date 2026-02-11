from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import sqlite3
import secrets
from database import init_db
from meal_recommender import MealRecommender
from image_grader import ImageGrader

# Initialize
init_db()
app = FastAPI(title="Food Recipe Generator")
recommender = MealRecommender()
grader = ImageGrader()

# Setup templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

def ensure_database_populated():
    conn = sqlite3.connect("meals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM recipes")
    count = cursor.fetchone()[0]
    conn.close()
    
    if count == 0:
        print(" Database empty! Populating with sample recipes...")
        from init_db import populate_sample_data
        populate_sample_data()
    else:
        print(f" Database already populated ({count} recipes)")

ensure_database_populated()

app = FastAPI(title="SmartMeal Planner")
recommender = MealRecommender()  # Will now find recipes
grader = ImageGrader()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page - input ingredients with cuisine and style filters"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_meal(
    request: Request,
    cuisine: str = Form(None),
    style: str = Form(None),
    ingredients: str = Form(""),
    vegan: bool = Form(False)
):
    """Generate meal based on ingredients with filters"""
    # Validate input
    if not ingredients or ingredients.strip() == "":
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Product list is empty"}
        )
    
    # Parse ingredients
    user_ingredients = [ing.strip().lower() for ing in ingredients.split(",") if ing.strip()]
    
    # Get recommendations
    recommendations = recommender.recommend(user_ingredients, top_n=10)
    
    # Apply cuisine filter
    if cuisine and cuisine != "any":
        recommendations = [r for r in recommendations if r["recipe"]["cuisine"].lower() == cuisine.lower()]
    
    # Apply vegan filter (simple check)
    if vegan:
        non_vegan_keywords = ["chicken", "beef", "pork", "lamb", "fish", "shrimp", "egg", "cheese", "milk", "butter", "cream", "yogurt"]
        filtered = []
        for rec in recommendations:
            recipe_ingredients = " ".join([ing["name"].lower() for ing in rec["recipe"]["ingredients"]])
            if not any(keyword in recipe_ingredients for keyword in non_vegan_keywords):
                filtered.append(rec)
        recommendations = filtered
    
    if not recommendations:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request, 
                "error": "No matching recipes found. Try adjusting filters or adding more ingredients.",
                "cuisine": cuisine,
                "style": style,
                "ingredients": ingredients,
                "vegan": vegan
            }
        )
    
    # Return best match
    best_recipe = recommendations[0]["recipe"]
    
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "recipe": best_recipe,
            "ingredients": ingredients,
            "cuisine": cuisine,
            "style": style,
            "vegan": vegan,
            "match_score": round(recommendations[0]["match_percentage"], 1)
        }
    )

@app.get("/grade/{recipe_id}", response_class=HTMLResponse)
async def grade_page(request: Request, recipe_id: int, dish_name: str):
    """Photo upload page with auto-filled dish name"""
    conn = sqlite3.connect("meals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM recipes WHERE id = ?", (recipe_id,))
    result = cursor.fetchone()
    conn.close()
    
    dish_name = result[0] if result else "Unknown Dish"
    return templates.TemplateResponse(
        "grade.html",
        {
            "request": request, 
            "recipe_id": recipe_id,
            "dish_name": dish_name  # Auto-filled from recipe
        }
    )

@app.post("/grade/{recipe_id}")
async def upload_photo(
    request: Request,
    recipe_id: int,
    photo: UploadFile = File(...),
    dish_name: str = Form(...)
):
    """Upload and grade photo"""
    # Create uploads directory
    os.makedirs("uploads", exist_ok=True)
    
    # Save file
    file_extension = os.path.splitext(photo.filename)[1]
    safe_filename = f"{secrets.token_hex(8)}{file_extension}"
    file_path = os.path.join("uploads", safe_filename)
    
    with open(file_path, "wb") as f:
        f.write(await photo.read())
    
    conn = sqlite3.connect("meals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM recipes WHERE id = ?", (recipe_id,))
    result = cursor.fetchone()
    conn.close()
    
    correct_dish_name = result[0] if result else "Unknown Dish"
    # Grade photo
    grade_result = grader.grade_photo(file_path, dish_name)
    
    return templates.TemplateResponse(
        "grade.html",
        {
            "request": request,
            "recipe_id": recipe_id,
            "dish_name": dish_name,
            "result": grade_result
        }
    )
