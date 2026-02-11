from database import init_db, add_recipe

def populate_sample_data():
    init_db()
    
    recipes = [
        # Kazakh (5 meals)
        ("Beshbarmak", "Kazakh", "Dinner", 
         ["horse meat:500g", "noodles:300g", "onion:2", "potato:3", "bay leaf:2 leaves"],
         "Boil meat until tender. Remove meat, slice. Cook noodles in meat broth. Sauté onions. Layer noodles, meat, and onions. Pour hot broth over. Serve hot.",
         {"calories": 650, "fat": 32.0, "carbs": 58.0, "protein": 42.0},
         "reference_images/beshbarmak.jpg"),
        
        ("Manti", "Kazakh", "Dinner",
         ["lamb:300g", "flour:400g", "onion:2", "garlic:3 cloves", "yogurt:200g"],
         "Make dough with flour and water. Rest 30 mins. Mix lamb with onions and garlic. Roll dough thin, cut squares. Fill with meat, fold into dumplings. Steam 30 mins. Serve with yogurt.",
         {"calories": 580, "fat": 28.0, "carbs": 52.0, "protein": 35.0},
         "reference_images/manti.jpg"),
        
        ("Kazy", "Kazakh", "Main",
         ["horse sausage:200g", "onion:1", "potato:2", "butter:30g", "salt:to taste"],
         "Slice kazy sausage. Sauté onions in butter. Add sausage and cook until golden. Serve with boiled potatoes. Garnish with fresh herbs.",
         {"calories": 420, "fat": 28.0, "carbs": 18.0, "protein": 28.0},
         "reference_images/kazy.jpg"),
        
        ("Shubat", "Kazakh", "Drink",
         ["camel milk:500ml", "salt:1 tsp", "water:100ml", "sugar:2 tbsp"],
         "Ferment camel milk for 24 hours. Add salt and mix well. Dilute with water if too thick. Add sugar to taste. Chill before serving.",
         {"calories": 120, "fat": 6.0, "carbs": 12.0, "protein": 6.0},
         "reference_images/shubat.jpg"),
        
        ("Baursaki", "Kazakh", "Side",
         ["flour:300g", "milk:150ml", "eggs:2", "yeast:7g", "vegetable oil:for frying"],
         "Mix flour, yeast, eggs, and warm milk. Knead into soft dough. Rest 1 hour. Roll and cut into small pieces. Deep fry until golden and puffy. Serve warm.",
         {"calories": 320, "fat": 14.0, "carbs": 42.0, "protein": 8.0},
         "reference_images/baursaki.jpg"),
        
        # Italian (5 meals)
        ("Spaghetti Aglio e Olio", "Italian", "Dinner", 
         ["spaghetti:200g", "garlic:4 cloves", "olive oil:3 tbsp", "red pepper flakes:1 tsp", "parsley:2 tbsp"],
         "Cook spaghetti al dente. Sauté minced garlic in olive oil until fragrant (do not brown). Add chili flakes. Toss with hot pasta, pasta water, and chopped parsley.",
         {"calories": 480, "fat": 18.5, "carbs": 68.0, "protein": 12.0},
         "reference_images/aglio_e_olio.jpg"),
        
        ("Margherita Pizza", "Italian", "Dinner",
         ["pizza dough:1 base", "tomato sauce:100g", "mozzarella:150g", "fresh basil:10 leaves", "olive oil:1 tbsp"],
         "Preheat oven to 250°C. Stretch dough. Spread sauce. Top with torn mozzarella and basil. Drizzle oil. Bake 10-12 mins until crust is golden.",
         {"calories": 650, "fat": 28.0, "carbs": 75.0, "protein": 25.0},
         "reference_images/margherita.jpg"),
        
        ("Risotto", "Italian", "Dinner",
         ["arborio rice:200g", "onion:1", "white wine:100ml", "parmesan:50g", "butter:30g", "vegetable broth:500ml"],
         "Sauté onion. Add rice, toast 2 mins. Add wine, simmer. Gradually add hot broth, stirring until absorbed. Stir in butter and parmesan.",
         {"calories": 520, "fat": 16.0, "carbs": 78.0, "protein": 14.0},
         "reference_images/risotto.jpg"),
        
        ("Tiramisu", "Italian", "Dessert",
         ["mascarpone:250g", "espresso:200ml", "ladyfingers:200g", "cocoa powder:2 tbsp", "eggs:3", "sugar:100g"],
         "Whisk egg yolks with sugar. Add mascarpone. Fold in whipped egg whites. Dip ladyfingers in espresso. Layer in dish. Dust with cocoa. Chill 4+ hours.",
         {"calories": 380, "fat": 22.0, "carbs": 38.0, "protein": 8.0},
         "reference_images/tiramisu.jpg"),
        
        ("Bruschetta", "Italian", "Appetizer",
         ["baguette:1 loaf", "tomato:2", "garlic:2 cloves", "basil:10 leaves", "olive oil:2 tbsp"],
         "Toast bread slices. Rub with garlic. Top with diced tomatoes, torn basil, olive oil, salt, and pepper.",
         {"calories": 220, "fat": 8.0, "carbs": 32.0, "protein": 5.0},
         "reference_images/bruschetta.jpg"),
        
        # French (5 meals)
        ("Coq au Vin", "French", "Dinner",
         ["chicken:800g", "red wine:500ml", "bacon:150g", "mushrooms:200g", "onion:2", "garlic:3 cloves", "thyme:1 bunch"],
         "Marinate chicken in wine overnight. Brown bacon, remove. Brown chicken in bacon fat. Sauté onions and mushrooms. Return all to pot with wine marinade. Simmer 1.5 hours until tender.",
         {"calories": 720, "fat": 38.0, "carbs": 12.0, "protein": 65.0},
         "reference_images/Coq_au_Vin.jpg"),
        
        ("Ratatouille", "French", "Side",
         ["eggplant:1", "zucchini:2", "bell pepper:2", "tomato:4", "onion:1", "garlic:3 cloves", "herbes de provence:1 tbsp"],
         "Slice all vegetables thinly. Sauté onions and garlic. Layer vegetables in spiral pattern in baking dish. Drizzle with olive oil and herbs. Bake at 180°C for 45 mins.",
         {"calories": 180, "fat": 8.0, "carbs": 25.0, "protein": 4.0},
         "reference_images/ratatouille.jpg"),
        
        ("Croissant", "French", "Breakfast",
         ["flour:500g", "butter:250g", "milk:250ml", "yeast:7g", "sugar:50g", "salt:1 tsp"],
         "Make dough with flour, milk, yeast, sugar, salt. Roll out, spread cold butter. Fold into thirds. Repeat 3 times, chilling between folds. Roll, cut triangles. Roll up, curve. Proof 2 hours. Bake at 200°C until golden.",
         {"calories": 380, "fat": 24.0, "carbs": 36.0, "protein": 7.0},
         "reference_images/Croissant.jpg"),
        
        ("Crème Brûlée", "French", "Dessert",
         ["heavy cream:500ml", "egg yolks:6", "vanilla bean:1", "sugar:100g"],
         "Heat cream with vanilla. Whisk egg yolks with sugar. Temper eggs with hot cream. Strain into ramekins. Bake in water bath at 150°C for 40 mins. Chill. Sprinkle sugar, torch until caramelized.",
         {"calories": 420, "fat": 36.0, "carbs": 22.0, "protein": 6.0},
         "reference_images/Creme_brulee.jpg"),
        
        ("French Onion Soup", "French", "Appetizer",
         ["onion:6 large", "beef broth:1L", "baguette:4 slices", "gruyere cheese:150g", "butter:50g", "thyme:1 tsp"],
         "Slice onions thinly. Melt butter, cook onions on low heat 45 mins until caramelized. Add thyme, broth. Simmer 30 mins. Ladle into bowls, top with toasted baguette and cheese. Broil until cheese melts.",
         {"calories": 320, "fat": 18.0, "carbs": 32.0, "protein": 12.0},
         "reference_images/French_Onion_Soup.jpg"),
        
        # American (5 meals)
        ("BBQ Ribs", "American", "Dinner",
         ["pork ribs:1kg", "BBQ sauce:300ml", "brown sugar:50g", "paprika:2 tbsp", "garlic powder:1 tbsp", "mustard:1 tbsp"],
         "Remove membrane from ribs. Mix dry rub ingredients. Coat ribs. Refrigerate 4 hours. Preheat smoker to 110°C. Smoke ribs 5 hours. Brush with BBQ sauce last 30 mins. Rest 15 mins before serving.",
         {"calories": 820, "fat": 52.0, "carbs": 28.0, "protein": 65.0},
         "reference_images/bbq_ribs.jpg"),
        
        ("Mac and Cheese", "American", "Side",
         ["macaroni:400g", "cheddar cheese:300g", "milk:500ml", "butter:50g", "flour:30g", "breadcrumbs:50g"],
         "Cook macaroni. Make roux with butter and flour. Add milk, whisk until thick. Add cheese, stir until melted. Mix with pasta. Top with breadcrumbs. Bake at 180°C for 25 mins until golden.",
         {"calories": 580, "fat": 28.0, "carbs": 62.0, "protein": 24.0},
         "reference_images/mac_and_cheese.jpg"),
        
        ("Buffalo Wings", "American", "Appetizer",
         ["chicken wings:1kg", "hot sauce:150ml", "butter:50g", "garlic powder:1 tsp", "flour:100g", "oil:for frying"],
         "Pat wings dry. Toss in flour. Deep fry at 190°C for 12 mins until crispy. Mix hot sauce, melted butter, garlic powder. Toss wings in sauce. Serve with celery and blue cheese dressing.",
         {"calories": 480, "fat": 32.0, "carbs": 8.0, "protein": 42.0},
         "reference_images/buffalo_wings.jpg"),
        
        ("Apple Pie", "American", "Dessert",
         ["flour:300g", "butter:200g", "apples:6", "sugar:150g", "cinnamon:2 tsp", "lemon juice:1 tbsp"],
         "Make pie dough with flour and cold butter. Chill. Peel and slice apples. Mix with sugar, cinnamon, lemon juice. Roll out dough, line pie dish. Fill with apples. Top with lattice crust. Bake at 190°C for 50 mins.",
         {"calories": 380, "fat": 18.0, "carbs": 52.0, "protein": 4.0},
         "reference_images/apple_pie.jpg"),
        
        ("Burgers", "American", "Lunch",
         ["ground beef:500g", "burger buns:4", "cheese:4 slices", "lettuce:4 leaves", "tomato:1", "onion:1", "ketchup:to taste"],
         "Mix beef with salt and pepper. Form into patties. Grill 4 mins per side for medium. Add cheese last minute. Toast buns. Assemble with lettuce, tomato, onion, and ketchup.",
         {"calories": 620, "fat": 36.0, "carbs": 42.0, "protein": 38.0},
         "reference_images/burger.jpg"),
    ]
    
    for recipe in recipes:
        add_recipe(*recipe)
    
    # VERIFY DATABASE POPULATION (Critical fix)
    import sqlite3
    conn = sqlite3.connect("meals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM recipes")
    raise Exception(f"Database initialization FAILED! Only {recipe_count} recipes found (expected 20).")
    
    print(f" Status: SUCCESS\n")

if __name__ == "__main__":
    populate_sample_data()

