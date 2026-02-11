import sqlite3

DB_PATH = "meals.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cuisine TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            instructions TEXT NOT NULL,
            calories INTEGER DEFAULT 0,
            fat REAL DEFAULT 0.0,
            carbs REAL DEFAULT 0.0,
            protein REAL DEFAULT 0.0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            recipe_id INTEGER,
            ingredient_id INTEGER,
            quantity TEXT,
            FOREIGN KEY (recipe_id) REFERENCES recipes(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
            PRIMARY KEY (recipe_id, ingredient_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_recipe(name, cuisine, meal_type, ingredients_list, instructions, nutrition, reference_image_path="reference_images/"):
    """Add recipe with reference image path"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO recipes (name, cuisine, meal_type, instructions, calories, fat, carbs, protein, reference_image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name, cuisine, meal_type, instructions,
        nutrition['calories'], nutrition['fat'], 
        nutrition['carbs'], nutrition['protein'],
        reference_image_path  # NEW: Reference image path
    ))
    recipe_id = cursor.lastrowid
    
    for ing in ingredients_list:
        if ':' in ing:
            ing_name, quantity = ing.split(':', 1)
        else:
            ing_name, quantity = ing, ""
        
        cursor.execute("INSERT OR IGNORE INTO ingredients (name) VALUES (?)", (ing_name.lower(),))
        cursor.execute("SELECT id FROM ingredients WHERE name = ?", (ing_name.lower(),))
        ingredient_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT OR IGNORE INTO recipe_ingredients (recipe_id, ingredient_id, quantity) VALUES (?, ?, ?)",
            (recipe_id, ingredient_id, quantity.strip())
        )
    
    conn.commit()
    conn.close()
    return recipe_id

def get_all_recipes_with_ingredients():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.id, r.name, r.cuisine, r.meal_type, r.instructions,
               r.calories, r.fat, r.carbs, r.protein,
               GROUP_CONCAT(i.name || ':' || ri.quantity, ', ') as ingredients
        FROM recipes r
        LEFT JOIN recipe_ingredients ri ON r.id = ri.recipe_id
        LEFT JOIN ingredients i ON ri.ingredient_id = i.id
        GROUP BY r.id
    ''')
    
    recipes = []
    for row in cursor.fetchall():
        ingredients = []
        if row[9]:
            for item in row[9].split(', '):
                if ':' in item:
                    name, qty = item.split(':', 1)
                    ingredients.append({"name": name, "quantity": qty})
                else:
                    ingredients.append({"name": item, "quantity": ""})
        
        recipes.append({
            "id": row[0],
            "name": row[1],
            "cuisine": row[2],
            "meal_type": row[3],
            "instructions": row[4],
            "nutrition": {
                "calories": row[5],
                "fat": row[6],
                "carbs": row[7],
                "protein": row[8]
            },
            "ingredients": ingredients
        })
    
    conn.close()
    return recipes