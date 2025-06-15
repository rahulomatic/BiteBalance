import json
import os
import random

class MealDatabase:
    """Database of meals with nutritional information"""
    
    def __init__(self):
        self.meals_path = 'data/meals_database.json'
        self.load_meals_database()
    
    def load_meals_database(self):
        """Load meals database from file"""
        try:
            if os.path.exists(self.meals_path):
                with open(self.meals_path, 'r') as f:
                    self.meals_db = json.load(f)
            else:
                self.meals_db = self.create_default_meals_database()
                self.save_meals_database()
        except Exception as e:
            print(f"Error loading meals database: {e}")
            self.meals_db = self.create_default_meals_database()
    
    def create_default_meals_database(self):
        """Create comprehensive meals database with nutritional info"""
        return {
            "breakfast": [
                {
                    "id": "b001",
                    "name": "Steel Cut Oatmeal with Berries",
                    "ingredients": ["steel cut oats", "blueberries", "strawberries", "almonds", "cinnamon"],
                    "nutrition": {
                        "calories": 320,
                        "protein": 12,
                        "carbs": 58,
                        "fat": 8,
                        "fiber": 10,
                        "sodium": 5,
                        "sugar": 15
                    },
                    "health_conditions": ["diabetes", "heart_disease", "obesity"],
                    "prep_time": 15,
                    "difficulty": "easy",
                    "instructions": [
                        "Cook steel cut oats according to package directions",
                        "Top with fresh berries and sliced almonds",
                        "Sprinkle with cinnamon"
                    ]
                },
                {
                    "id": "b002",
                    "name": "Greek Yogurt Parfait",
                    "ingredients": ["greek yogurt", "granola", "honey", "mixed berries"],
                    "nutrition": {
                        "calories": 280,
                        "protein": 20,
                        "carbs": 35,
                        "fat": 6,
                        "fiber": 5,
                        "sodium": 80,
                        "sugar": 25
                    },
                    "health_conditions": ["obesity", "heart_disease"],
                    "prep_time": 5,
                    "difficulty": "easy",
                    "instructions": [
                        "Layer Greek yogurt in a bowl",
                        "Add granola and berries",
                        "Drizzle with honey"
                    ]
                },
                {
                    "id": "b003",
                    "name": "Avocado Toast with Eggs",
                    "ingredients": ["whole grain bread", "avocado", "eggs", "tomato", "lime"],
                    "nutrition": {
                        "calories": 380,
                        "protein": 18,
                        "carbs": 30,
                        "fat": 22,
                        "fiber": 12,
                        "sodium": 320,
                        "sugar": 3
                    },
                    "health_conditions": ["heart_disease", "obesity"],
                    "prep_time": 10,
                    "difficulty": "easy",
                    "instructions": [
                        "Toast whole grain bread",
                        "Mash avocado with lime juice",
                        "Top with sliced tomato and poached egg"
                    ]
                }
            ],
            "lunch": [
                {
                    "id": "l001",
                    "name": "Quinoa Buddha Bowl",
                    "ingredients": ["quinoa", "chickpeas", "kale", "sweet potato", "tahini", "lemon"],
                    "nutrition": {
                        "calories": 450,
                        "protein": 18,
                        "carbs": 65,
                        "fat": 15,
                        "fiber": 12,
                        "sodium": 280,
                        "sugar": 8
                    },
                    "health_conditions": ["diabetes", "heart_disease", "hypertension"],
                    "prep_time": 25,
                    "difficulty": "medium",
                    "instructions": [
                        "Cook quinoa and roast sweet potato",
                        "Massage kale with lemon juice",
                        "Combine with chickpeas and tahini dressing"
                    ]
                },
                {
                    "id": "l002",
                    "name": "Grilled Salmon Salad",
                    "ingredients": ["salmon", "mixed greens", "cucumber", "tomatoes", "olive oil", "balsamic vinegar"],
                    "nutrition": {
                        "calories": 420,
                        "protein": 35,
                        "carbs": 15,
                        "fat": 25,
                        "fiber": 6,
                        "sodium": 180,
                        "sugar": 10
                    },
                    "health_conditions": ["heart_disease", "hypertension", "obesity"],
                    "prep_time": 20,
                    "difficulty": "medium",
                    "instructions": [
                        "Grill salmon with herbs",
                        "Prepare salad with mixed greens and vegetables",
                        "Dress with olive oil and balsamic vinegar"
                    ]
                },
                {
                    "id": "l003",
                    "name": "Lentil Vegetable Soup",
                    "ingredients": ["red lentils", "carrots", "celery", "onion", "garlic", "vegetable broth"],
                    "nutrition": {
                        "calories": 320,
                        "protein": 18,
                        "carbs": 55,
                        "fat": 2,
                        "fiber": 16,
                        "sodium": 480,
                        "sugar": 8
                    },
                    "health_conditions": ["diabetes", "obesity", "heart_disease"],
                    "prep_time": 30,
                    "difficulty": "easy",
                    "instructions": [
                        "Sauté vegetables in a large pot",
                        "Add lentils and broth, simmer 20 minutes",
                        "Season with herbs and spices"
                    ]
                }
            ],
            "dinner": [
                {
                    "id": "d001",
                    "name": "Herb-Crusted Chicken with Vegetables",
                    "ingredients": ["chicken breast", "broccoli", "carrots", "herbs", "olive oil"],
                    "nutrition": {
                        "calories": 380,
                        "protein": 42,
                        "carbs": 20,
                        "fat": 14,
                        "fiber": 8,
                        "sodium": 220,
                        "sugar": 10
                    },
                    "health_conditions": ["obesity", "diabetes", "heart_disease"],
                    "prep_time": 35,
                    "difficulty": "medium",
                    "instructions": [
                        "Season chicken with herbs",
                        "Bake chicken and roast vegetables",
                        "Serve with steamed broccoli"
                    ]
                },
                {
                    "id": "d002",
                    "name": "Baked Cod with Sweet Potato",
                    "ingredients": ["cod fillet", "sweet potato", "asparagus", "lemon", "garlic"],
                    "nutrition": {
                        "calories": 350,
                        "protein": 30,
                        "carbs": 35,
                        "fat": 8,
                        "fiber": 6,
                        "sodium": 180,
                        "sugar": 12
                    },
                    "health_conditions": ["heart_disease", "hypertension", "diabetes"],
                    "prep_time": 30,
                    "difficulty": "easy",
                    "instructions": [
                        "Bake sweet potato until tender",
                        "Season cod with lemon and garlic",
                        "Steam asparagus until crisp-tender"
                    ]
                },
                {
                    "id": "d003",
                    "name": "Tofu Stir-Fry with Brown Rice",
                    "ingredients": ["firm tofu", "brown rice", "bell peppers", "snap peas", "ginger", "soy sauce"],
                    "nutrition": {
                        "calories": 390,
                        "protein": 20,
                        "carbs": 50,
                        "fat": 12,
                        "fiber": 8,
                        "sodium": 580,
                        "sugar": 8
                    },
                    "health_conditions": ["heart_disease", "obesity"],
                    "prep_time": 25,
                    "difficulty": "medium",
                    "instructions": [
                        "Cook brown rice",
                        "Stir-fry tofu until golden",
                        "Add vegetables and sauce, cook until tender"
                    ]
                }
            ],
            "snacks": [
                {
                    "id": "s001",
                    "name": "Apple with Almond Butter",
                    "ingredients": ["apple", "almond butter"],
                    "nutrition": {
                        "calories": 190,
                        "protein": 6,
                        "carbs": 25,
                        "fat": 8,
                        "fiber": 6,
                        "sodium": 2,
                        "sugar": 19
                    },
                    "health_conditions": ["diabetes", "heart_disease", "obesity"],
                    "prep_time": 2,
                    "difficulty": "easy",
                    "instructions": [
                        "Slice apple",
                        "Serve with 2 tablespoons almond butter"
                    ]
                },
                {
                    "id": "s002",
                    "name": "Hummus with Vegetables",
                    "ingredients": ["hummus", "carrots", "cucumber", "bell peppers"],
                    "nutrition": {
                        "calories": 150,
                        "protein": 6,
                        "carbs": 18,
                        "fat": 6,
                        "fiber": 6,
                        "sodium": 240,
                        "sugar": 8
                    },
                    "health_conditions": ["hypertension", "diabetes", "obesity"],
                    "prep_time": 5,
                    "difficulty": "easy",
                    "instructions": [
                        "Cut vegetables into sticks",
                        "Serve with 1/4 cup hummus"
                    ]
                }
            ]
        }
    
    def save_meals_database(self):
        """Save meals database to file"""
        os.makedirs('data', exist_ok=True)
        with open(self.meals_path, 'w') as f:
            json.dump(self.meals_db, f, indent=2)
    
    def get_meal_suggestions(self, meal_type, user_data):
        """Get meal suggestions based on user's health conditions"""
        try:
            meals = self.meals_db.get(meal_type, [])
            user_conditions = user_data.get('conditions', [])
            
            # Filter meals based on health conditions
            suitable_meals = []
            for meal in meals:
                meal_conditions = meal.get('health_conditions', [])
                
                # Check if meal is suitable for user's conditions
                if not user_conditions:  # No specific conditions
                    suitable_meals.append(meal)
                else:
                    # Meal is suitable if it addresses any of user's conditions
                    if any(condition in meal_conditions for condition in user_conditions):
                        suitable_meals.append(meal)
            
            # If no specific matches, return all meals for the type
            if not suitable_meals:
                suitable_meals = meals
            
            # Return up to 3 random suggestions
            return random.sample(suitable_meals, min(3, len(suitable_meals)))
            
        except Exception as e:
            print(f"Error getting meal suggestions: {e}")
            return []
    
    def get_nutrition_info(self, meal_id):
        """Get detailed nutrition information for a specific meal"""
        try:
            for meal_type, meals in self.meals_db.items():
                for meal in meals:
                    if meal['id'] == meal_id:
                        return meal
            return None
        except Exception as e:
            print(f"Error getting nutrition info: {e}")
            return None
    
    def search_meals(self, query, meal_type=None):
        """Search meals by name or ingredients"""
        try:
            results = []
            query = query.lower()
            
            meal_types = [meal_type] if meal_type else self.meals_db.keys()
            
            for mtype in meal_types:
                meals = self.meals_db.get(mtype, [])
                for meal in meals:
                    # Search in name
                    if query in meal['name'].lower():
                        results.append(meal)
                        continue
                    
                    # Search in ingredients
                    if any(query in ingredient.lower() for ingredient in meal['ingredients']):
                        results.append(meal)
            
            return results
        except Exception as e:
            print(f"Error searching meals: {e}")
            return []
    
    def get_meals_by_condition(self, condition):
        """Get all meals suitable for a specific health condition"""
        try:
            suitable_meals = []
            
            for meal_type, meals in self.meals_db.items():
                for meal in meals:
                    if condition in meal.get('health_conditions', []):
                        meal['meal_type'] = meal_type
                        suitable_meals.append(meal)
            
            return suitable_meals
        except Exception as e:
            print(f"Error getting meals by condition: {e}")
            return []
    
    def calculate_daily_nutrition(self, selected_meals):
        """Calculate total nutrition for selected meals"""
        try:
            total_nutrition = {
                'calories': 0,
                'protein': 0,
                'carbs': 0,
                'fat': 0,
                'fiber': 0,
                'sodium': 0,
                'sugar': 0
            }
            
            for meal in selected_meals:
                nutrition = meal.get('nutrition', {})
                for nutrient in total_nutrition:
                    total_nutrition[nutrient] += nutrition.get(nutrient, 0)
            
            return total_nutrition
        except Exception as e:
            print(f"Error calculating daily nutrition: {e}")
            return total_nutrition