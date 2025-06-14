import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class DietPlanner:
    def __init__(self):
        self.model_path = 'models/trained/diet_model.pkl'
        self.scaler_path = 'models/trained/scaler.pkl'
        self.meal_rules_path = 'data/meal_rules.json'
        
        self.model = None
        self.scaler = None
        self.meal_rules = {}

        self._load_model()
        self._load_meal_rules()

    # -----------------------------
    # MODEL AND RULE LOADING
    # -----------------------------
    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                print("Model and scaler loaded.")
            else:
                print("No model found. Using rule-based logic.")
        except Exception as e:
            print(f"Model loading failed: {e}")

    def _load_meal_rules(self):
        try:
            if os.path.exists(self.meal_rules_path):
                with open(self.meal_rules_path, 'r') as f:
                    self.meal_rules = json.load(f)
            else:
                self.meal_rules = self._default_meal_rules()
                self._save_meal_rules()
        except Exception as e:
            print(f"Rule loading failed: {e}")
            self.meal_rules = self._default_meal_rules()

    def _save_meal_rules(self):
        os.makedirs(os.path.dirname(self.meal_rules_path), exist_ok=True)
        with open(self.meal_rules_path, 'w') as f:
            json.dump(self.meal_rules, f, indent=2)

    def _default_meal_rules(self):
        return {
            "diabetes": {
                "carb_limit": 45,
                "fiber_min": 25,
                "sugar_limit": 25,
                "recommended_foods": ["whole grains", "lean proteins", "non-starchy vegetables", "legumes", "nuts", "seeds", "low-fat dairy"],
                "avoid_foods": ["refined sugars", "white bread", "sugary drinks", "processed foods", "high-sodium foods"]
            },
            "heart_disease": {
                "sodium_limit": 2300,
                "saturated_fat_limit": 13,
                "fiber_min": 25,
                "recommended_foods": ["fatty fish", "olive oil", "nuts", "whole grains", "fruits", "vegetables", "legumes"],
                "avoid_foods": ["trans fats", "processed meats", "high-sodium foods", "refined carbohydrates", "excessive alcohol"]
            },
            "hypertension": {
                "sodium_limit": 1500,
                "potassium_min": 3500,
                "recommended_foods": ["leafy greens", "berries", "bananas", "beets", "oats", "garlic", "fatty fish", "seeds"],
                "avoid_foods": ["processed foods", "canned soups", "deli meats", "pizza", "alcohol", "caffeine"]
            },
            "obesity": {
                "calorie_deficit": 500,
                "protein_min": 1.2,
                "recommended_foods": ["lean proteins", "vegetables", "fruits", "whole grains", "legumes", "low-fat dairy"],
                "avoid_foods": ["high-calorie drinks", "fried foods", "sweets", "processed snacks", "large portions"]
            }
        }

    # -----------------------------
    # MEAL PLANNING INTERFACE
    # -----------------------------
    def generate_meal_plan(self, user_data):
        try:
            nutrition = self._calculate_nutrition_targets(user_data)
            plan = {
                meal: self._generate_meal(meal, user_data, nutrition)
                for meal in ['breakfast', 'lunch', 'dinner', 'snacks']
            }
            plan['weekly_plan'] = self._generate_weekly_variation(user_data)
            plan['nutrition_summary'] = nutrition
            return plan
        except Exception as e:
            print(f"Failed to generate meal plan: {e}")
            return self._default_meal_plan()

    # -----------------------------
    # CORE LOGIC
    # -----------------------------
    def _calculate_nutrition_targets(self, user_data):
        base_cal = user_data.get('daily_calories', 2000)
        weight = user_data.get('weight', 70)  # kg
        conditions = user_data.get('conditions', [])
        
        targets = {
            'calories': base_cal,
            'protein': round(base_cal * 0.15 / 4),
            'carbs': round(base_cal * 0.5 / 4),
            'fat': round(base_cal * 0.35 / 9),
            'fiber': 25,
            'sodium': 2300,
            'sugar': 50
        }

        for cond in conditions:
            rules = self.meal_rules.get(cond, {})
            if cond == 'diabetes':
                targets['carbs'] = min(targets['carbs'], 135)
                targets['fiber'] = max(targets['fiber'], rules.get('fiber_min', 25))
                targets['sugar'] = min(targets['sugar'], rules.get('sugar_limit', 50))
            elif cond == 'heart_disease':
                targets['sodium'] = min(targets['sodium'], rules.get('sodium_limit', 2300))
                targets['fiber'] = max(targets['fiber'], rules.get('fiber_min', 25))
                targets['saturated_fat'] = rules.get('saturated_fat_limit', 13)
            elif cond == 'hypertension':
                targets['sodium'] = min(targets['sodium'], rules.get('sodium_limit', 2300))
                targets['potassium'] = rules.get('potassium_min', 3500)
            elif cond == 'obesity':
                targets['calories'] -= rules.get('calorie_deficit', 500)
                targets['protein'] = max(targets['protein'], round(weight * rules.get('protein_min', 1.2)))
        
        return targets

    def _generate_meal(self, meal_type, user_data, nutrition_targets):
        templates = self._get_meal_templates()
        ingredients = self._filter_meal_options(
            templates[meal_type],
            user_data.get('conditions', []),
            user_data.get('allergies', []),
            user_data.get('dietary_preferences', [])
        )
        portions = self._calculate_portions(meal_type, nutrition_targets)
        return {
            'name': f"Personalized {meal_type.title()}",
            'ingredients': ingredients,
            'portions': portions,
            'instructions': self._generate_instructions(),
            'nutrition': self._estimate_nutrition(portions),
            'health_benefits': self._get_health_benefits(user_data.get('conditions', []))
        }

    def _filter_meal_options(self, template, conditions, allergies, preferences):
        filtered = {}
        for cat, items in template.items():
            filtered[cat] = [
                item for item in items
                if not any(allergy.lower() in item.lower() for allergy in allergies)
                and not ('vegetarian' in preferences and any(m in item.lower() for m in ['chicken', 'beef', 'fish']))
                and not ('vegan' in preferences and any(v in item.lower() for v in ['eggs', 'yogurt', 'cheese', 'chicken', 'beef', 'fish']))
                and all(avoid not in item.lower() for cond in conditions for avoid in self.meal_rules.get(cond, {}).get('avoid_foods', []))
            ]
        return filtered

    def _calculate_portions(self, meal, targets):
        split = {'breakfast': 0.25, 'lunch': 0.35, 'dinner': 0.3, 'snacks': 0.1}
        factor = split[meal]
        return {
            'calories': round(targets['calories'] * factor),
            'protein': round(targets['protein'] * factor),
            'carbs': round(targets['carbs'] * factor),
            'fat': round(targets['fat'] * factor)
        }

    def _generate_instructions(self):
        return [
            "Prepare all ingredients.",
            "Cook proteins healthily (grill/bake/steam).",
            "Steam or sauté vegetables lightly.",
            "Mix ingredients and season with herbs.",
            "Serve fresh."
        ]

    def _estimate_nutrition(self, portions):
        return {
            'calories': portions['calories'],
            'protein': f"{portions['protein']}g",
            'carbohydrates': f"{portions['carbs']}g",
            'fat': f"{portions['fat']}g",
            'fiber': "8-12g",
            'sodium': "300-600mg"
        }

    def _get_health_benefits(self, conditions):
        benefits = {
            'diabetes': ["Helps stabilize blood sugar", "High fiber supports glucose control"],
            'heart_disease': ["Supports heart health", "Rich in omega-3 fats"],
            'hypertension': ["Low sodium helps BP", "High potassium supports BP control"],
            'obesity': ["Supports weight loss", "High protein improves satiety"]
        }
        return [msg for cond in conditions for msg in benefits.get(cond, [])]

    def _generate_weekly_variation(self, user_data):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return {
            day: {
                meal: self._generate_meal(meal, user_data, self._calculate_nutrition_targets(user_data))
                for meal in ['breakfast', 'lunch', 'dinner', 'snacks']
            }
            for day in days
        }

    def _get_meal_templates(self):
        return {
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
                'options': ['apple with almond butter', 'greek yogurt with berries', 'hummus with vegetables', 'nuts', 'cottage cheese with cucumber']
            }
        }

    def _default_meal_plan(self):
        return {
            'breakfast': {'name': 'Default Breakfast', 'ingredients': {}, 'nutrition': {}, 'health_benefits': []},
            'lunch': {'name': 'Default Lunch', 'ingredients': {}, 'nutrition': {}, 'health_benefits': []},
            'dinner': {'name': 'Default Dinner', 'ingredients': {}, 'nutrition': {}, 'health_benefits': []},
            'snacks': {'name': 'Default Snacks', 'ingredients': {}, 'nutrition': {}, 'health_benefits': []}
        }
