import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import os
import json

class DietPlanner:
    def __init__(self):
        self.model_path = 'models/trained/diet_model.pkl'
        self.scaler_path = 'models/trained/scaler.pkl'
        self.meal_rules_path = 'data/meal_rules.json'
        
        # Load trained model or create default rules
        self.load_model()
        self.load_meal_rules()
        
    def load_model(self):
        """Load pre-trained model or initialize with default rules"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("Loaded trained AI model")
            else:
                print("No trained model found, using rule-based system")
                self.model = None
                self.scaler = None
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
            self.scaler = None
    
    def load_meal_rules(self):
        """Load medical guidelines and meal rules"""
        try:
            if os.path.exists(self.meal_rules_path):
                with open(self.meal_rules_path, 'r') as f:
                    self.meal_rules = json.load(f)
            else:
                # Default medical guidelines
                self.meal_rules = self.get_default_meal_rules()
                self.save_meal_rules()
        except Exception as e:
            print(f"Error loading meal rules: {e}")
            self.meal_rules = self.get_default_meal_rules()
    
    def get_default_meal_rules(self):
        """Medical guidelines based on WHO, ADA, AHA recommendations"""
        return {
            "diabetes": {
                "carb_limit": 45,  # grams per meal
                "fiber_min": 25,   # grams per day
                "sugar_limit": 25, # grams per day
                "recommended_foods": [
                    "whole grains", "lean proteins", "non-starchy vegetables",
                    "legumes", "nuts", "seeds", "low-fat dairy"
                ],
                "avoid_foods": [
                    "refined sugars", "white bread", "sugary drinks",
                    "processed foods", "high-sodium foods"
                ]
            },
            "heart_disease": {
                "sodium_limit": 2300,  # mg per day
                "saturated_fat_limit": 13,  # grams per day
                "fiber_min": 25,
                "recommended_foods": [
                    "fatty fish", "olive oil", "nuts", "whole grains",
                    "fruits", "vegetables", "legumes"
                ],
                "avoid_foods": [
                    "trans fats", "processed meats", "high-sodium foods",
                    "refined carbohydrates", "excessive alcohol"
                ]
            },
            "hypertension": {
                "sodium_limit": 1500,  # mg per day (DASH diet)
                "potassium_min": 3500,  # mg per day
                "recommended_foods": [
                    "leafy greens", "berries", "bananas", "beets",
                    "oats", "garlic", "fatty fish", "seeds"
                ],
                "avoid_foods": [
                    "processed foods", "canned soups", "deli meats",
                    "pizza", "alcohol", "caffeine"
                ]
            },
            "obesity": {
                "calorie_deficit": 500,  # calories below maintenance
                "protein_min": 1.2,  # grams per kg body weight
                "recommended_foods": [
                    "lean proteins", "vegetables", "fruits", "whole grains",
                    "legumes", "low-fat dairy"
                ],
                "avoid_foods": [
                    "high-calorie drinks", "fried foods", "sweets",
                    "processed snacks", "large portions"
                ]
            }
        }
    
    def save_meal_rules(self):
        """Save meal rules to file"""
        os.makedirs('data', exist_ok=True)
        with open(self.meal_rules_path, 'w') as f:
            json.dump(self.meal_rules, f, indent=2)
    
    def generate_meal_plan(self, user_data):
        """Generate personalized meal plan based on health conditions"""
        try:
            # Determine primary health focus
            conditions = user_data.get('conditions', [])
            
            # Calculate nutritional requirements
            nutrition_targets = self.calculate_nutrition_targets(user_data)
            
            # Generate meals for each meal type
            meal_plan = {
                'breakfast': self.generate_meal('breakfast', user_data, nutrition_targets),
                'lunch': self.generate_meal('lunch', user_data, nutrition_targets),
                'dinner': self.generate_meal('dinner', user_data, nutrition_targets),
                'snacks': self.generate_meal('snacks', user_data, nutrition_targets)
            }
            
            # Add weekly variation
            meal_plan['weekly_plan'] = self.generate_weekly_variation(meal_plan, user_data)
            
            # Add nutritional summary
            meal_plan['nutrition_summary'] = nutrition_targets
            
            return meal_plan
            
        except Exception as e:
            print(f"Error generating meal plan: {e}")
            return self.get_default_meal_plan()
    
    def calculate_nutrition_targets(self, user_data):
        """Calculate daily nutritional targets based on health conditions"""
        base_calories = user_data.get('daily_calories', 2000)
        conditions = user_data.get('conditions', [])
        
        targets = {
            'calories': base_calories,
            'protein': round(base_calories * 0.15 / 4),  # 15% of calories
            'carbs': round(base_calories * 0.50 / 4),    # 50% of calories
            'fat': round(base_calories * 0.35 / 9),      # 35% of calories
            'fiber': 25,
            'sodium': 2300,
            'sugar': 50
        }
        
        # Adjust based on conditions
        for condition in conditions:
            if condition in self.meal_rules:
                rules = self.meal_rules[condition]
                
                if condition == 'diabetes':
                    targets['carbs'] = min(targets['carbs'], 135)  # ADA recommendation
                    targets['fiber'] = max(targets['fiber'], rules['fiber_min'])
                    targets['sugar'] = min(targets['sugar'], rules['sugar_limit'])
                
                elif condition == 'heart_disease':
                    targets['sodium'] = min(targets['sodium'], rules['sodium_limit'])
                    targets['fiber'] = max(targets['fiber'], rules['fiber_min'])
                    targets['saturated_fat'] = rules['saturated_fat_limit']
                
                elif condition == 'hypertension':
                    targets['sodium'] = min(targets['sodium'], rules['sodium_limit'])
                    targets['potassium'] = rules['potassium_min']
                
                elif condition == 'obesity':
                    targets['calories'] -= rules['calorie_deficit']
                    targets['protein'] = max(targets['protein'], 
                                           user_data['weight'] * rules['protein_min'])
        
        return targets
    
    def generate_meal(self, meal_type, user_data, nutrition_targets):
        """Generate specific meal based on type and requirements"""
        conditions = user_data.get('conditions', [])
        allergies = user_data.get('allergies', [])
        preferences = user_data.get('dietary_preferences', [])
        
        # Meal templates based on medical guidelines
        meal_templates = {
            'breakfast': {
                'base': ['oatmeal', 'whole grain toast', 'greek yogurt', 'eggs'],
                'protein': ['eggs', 'greek yogurt', 'cottage cheese', 'nuts'],
                'carbs': ['oatmeal', 'whole grain bread', 'berries', 'banana'],
                'healthy_fats': ['avocado', 'nuts', 'seeds', 'olive oil']
            },
            'lunch': {
                'base': ['quinoa', 'brown rice', 'whole grain wrap', 'salad'],
                'protein': ['grilled chicken', 'salmon', 'tofu', 'legumes'],
                'vegetables': ['spinach', 'broccoli', 'bell peppers', 'tomatoes'],
                'healthy_fats': ['olive oil', 'avocado', 'nuts', 'seeds']
            },
            'dinner': {
                'base': ['quinoa', 'sweet potato', 'brown rice', 'cauliflower rice'],
                'protein': ['grilled fish', 'lean beef', 'chicken breast', 'lentils'],
                'vegetables': ['asparagus', 'brussels sprouts', 'kale', 'carrots'],
                'healthy_fats': ['olive oil', 'avocado', 'nuts']
            },
            'snacks': {
                'options': ['apple with almond butter', 'greek yogurt with berries',
                           'hummus with vegetables', 'handful of nuts',
                           'cottage cheese with cucumber']
            }
        }
        
        # Filter based on conditions and preferences
        filtered_options = self.filter_meal_options(
            meal_templates[meal_type], conditions, allergies, preferences
        )
        
        # Calculate portion sizes based on nutrition targets
        portions = self.calculate_portions(meal_type, nutrition_targets)
        
        return {
            'name': f"Personalized {meal_type.title()}",
            'ingredients': filtered_options,
            'portions': portions,
            'instructions': self.generate_instructions(filtered_options),
            'nutrition': self.estimate_nutrition(filtered_options, portions),
            'health_benefits': self.get_health_benefits(filtered_options, conditions)
        }
    
    def filter_meal_options(self, meal_template, conditions, allergies, preferences):
        """Filter meal options based on health conditions and preferences"""
        filtered = {}
        
        for category, options in meal_template.items():
            filtered[category] = []
            
            for option in options:
                # Check allergies
                if any(allergy.lower() in option.lower() for allergy in allergies):
                    continue
                
                # Check dietary preferences
                if 'vegetarian' in preferences and any(meat in option.lower() 
                    for meat in ['chicken', 'beef', 'fish', 'salmon']):
                    continue
                
                if 'vegan' in preferences and any(animal in option.lower() 
                    for animal in ['eggs', 'yogurt', 'cheese', 'chicken', 'beef', 'fish']):
                    continue
                
                # Check condition-specific restrictions
                include_option = True
                for condition in conditions:
                    if condition in self.meal_rules:
                        avoid_foods = self.meal_rules[condition]['avoid_foods']
                        if any(avoid_food in option.lower() for avoid_food in avoid_foods):
                            include_option = False
                            break
                
                if include_option:
                    filtered[category].append(option)
        
        return filtered
    
    def calculate_portions(self, meal_type, nutrition_targets):
        """Calculate appropriate portion sizes"""
        # Distribute calories across meals
        meal_calorie_distribution = {
            'breakfast': 0.25,
            'lunch': 0.35,
            'dinner': 0.30,
            'snacks': 0.10
        }
        
        meal_calories = nutrition_targets['calories'] * meal_calorie_distribution[meal_type]
        
        return {
            'calories': round(meal_calories),
            'protein': round(nutrition_targets['protein'] * meal_calorie_distribution[meal_type]),
            'carbs': round(nutrition_targets['carbs'] * meal_calorie_distribution[meal_type]),
            'fat': round(nutrition_targets['fat'] * meal_calorie_distribution[meal_type])
        }
    
    def generate_instructions(self, ingredients):
        """Generate cooking instructions"""
        instructions = [
            "1. Prepare all ingredients according to portion sizes",
            "2. Cook proteins using healthy methods (grilling, baking, steaming)",
            "3. Steam or lightly sauté vegetables with minimal oil",
            "4. Combine ingredients and season with herbs and spices",
            "5. Serve immediately while fresh"
        ]
        return instructions
    
    def estimate_nutrition(self, ingredients, portions):
        """Estimate nutritional content"""
        # Simplified nutrition estimation
        return {
            'calories': portions['calories'],
            'protein': f"{portions['protein']}g",
            'carbohydrates': f"{portions['carbs']}g",
            'fat': f"{portions['fat']}g",
            'fiber': "8-12g",
            'sodium': "300-600mg"
        }
    
    def get_health_benefits(self, ingredients, conditions):
        """Get health benefits for specific conditions"""
        benefits = []
        
        for condition in conditions:
            if condition == 'diabetes':
                benefits.append("Helps stabilize blood sugar levels")
                benefits.append("High fiber content aids glucose control")
            elif condition == 'heart_disease':
                benefits.append("Supports cardiovascular health")
                benefits.append("Rich in heart-healthy omega-3 fatty acids")
            elif condition == 'hypertension':
                benefits.append("Low sodium content helps manage blood pressure")
                benefits.append("Potassium-rich foods support healthy BP")
            elif condition == 'obesity':
                benefits.append("Balanced macronutrients support weight management")
                benefits.append("High protein content promotes satiety")
        
        return benefits
    
    def generate_weekly_variation(self, base_plan, user_data):
        """Generate 7-day meal plan with variations"""
        weekly_plan = {}
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in days:
            weekly_plan[day] = {
                'breakfast': self.generate_meal('breakfast', user_data, 
                                              self.calculate_nutrition_targets(user_data)),
                'lunch': self.generate_meal('lunch', user_data, 
                                          self.calculate_nutrition_targets(user_data)),
                'dinner': self.generate_meal('dinner', user_data, 
                                           self.calculate_nutrition_targets(user_data)),
                'snacks': self.generate_meal('snacks', user_data, 
                                           self.calculate_nutrition_targets(user_data))
            }
        
        return weekly_plan
    
    def get_default_meal_plan(self):
        """Fallback meal plan if generation fails"""
        return {
            'breakfast': {
                'name': 'Healthy Breakfast',
                'ingredients': {'base': ['oatmeal'], 'protein': ['greek yogurt']},
                'nutrition': {'calories': 300, 'protein': '15g'},
                'health_benefits': ['Provides sustained energy']
            },
            'lunch': {
                'name': 'Balanced Lunch',
                'ingredients': {'base': ['quinoa'], 'protein': ['grilled chicken']},
                'nutrition': {'calories': 450, 'protein': '25g'},
                'health_benefits': ['Complete protein source']
            },
            'dinner': {
                'name': 'Nutritious Dinner',
                'ingredients': {'base': ['brown rice'], 'protein': ['salmon']},
                'nutrition': {'calories': 400, 'protein': '30g'},
                'health_benefits': ['Rich in omega-3 fatty acids']
            },
            'snacks': {
                'name': 'Healthy Snack',
                'ingredients': {'options': ['apple with almond butter']},
                'nutrition': {'calories': 150, 'protein': '5g'},
                'health_benefits': ['Provides healthy fats and fiber']
            }
        }