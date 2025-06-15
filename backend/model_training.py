"""
AI Model Training Script for Diet Planner
Trains machine learning models for personalized meal recommendations
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pickle
import json
import os
from datetime import datetime

class DietModelTrainer:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.model_dir = 'models/trained'
        self.data_dir = 'data'
        
        # Ensure directories exist
        os.makedirs(self.model_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
    
    def generate_synthetic_data(self, n_samples=5000):
        """Generate synthetic training data based on medical guidelines"""
        print("Generating synthetic training data...")
        
        np.random.seed(42)
        
        # Generate user profiles
        data = []
        
        for i in range(n_samples):
            # Basic demographics
            age = np.random.randint(18, 80)
            gender = np.random.choice(['male', 'female'])
            height = np.random.normal(170 if gender == 'male' else 160, 10)
            weight = np.random.normal(75 if gender == 'male' else 65, 15)
            
            # Calculate BMI
            bmi = weight / ((height/100) ** 2)
            
            # Health conditions based on realistic prevalence
            conditions = []
            if bmi > 30:
                conditions.append('obesity')
            if age > 45 and np.random.random() < 0.3:
                conditions.append('diabetes')
            if age > 50 and np.random.random() < 0.4:
                conditions.append('heart_disease')
            if age > 40 and np.random.random() < 0.35:
                conditions.append('hypertension')
            
            # Vital signs
            systolic_bp = np.random.normal(120, 20)
            diastolic_bp = np.random.normal(80, 10)
            blood_sugar = np.random.normal(100, 20)
            
            # Adjust vitals based on conditions
            if 'hypertension' in conditions:
                systolic_bp += np.random.normal(20, 10)
                diastolic_bp += np.random.normal(10, 5)
            
            if 'diabetes' in conditions:
                blood_sugar += np.random.normal(50, 20)
            
            # Activity level
            activity_level = np.random.choice(['sedentary', 'light', 'moderate', 'active'])
            
            # Calculate daily calorie needs
            if gender == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
            activity_multipliers = {
                'sedentary': 1.2, 'light': 1.375, 
                'moderate': 1.55, 'active': 1.725
            }
            daily_calories = bmr * activity_multipliers[activity_level]
            
            # Generate meal preferences based on conditions
            meal_preferences = self.generate_meal_preferences(conditions, bmi, age)
            
            data.append({
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'bmi': bmi,
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'blood_sugar': blood_sugar,
                'activity_level': activity_level,
                'daily_calories': daily_calories,
                'conditions': ','.join(conditions),
                'meal_preference': meal_preferences
            })
        
        df = pd.DataFrame(data)
        
        # Save synthetic data
        df.to_csv(f'{self.data_dir}/synthetic_training_data.csv', index=False)
        print(f"Generated {len(df)} synthetic training samples")
        
        return df
    
    def generate_meal_preferences(self, conditions, bmi, age):
        """Generate appropriate meal preferences based on health profile"""
        preferences = []
        
        # Base preferences
        if bmi > 25:
            preferences.extend(['low_calorie', 'high_protein', 'high_fiber'])
        
        # Condition-specific preferences
        if 'diabetes' in conditions:
            preferences.extend(['low_carb', 'complex_carbs', 'high_fiber'])
        
        if 'heart_disease' in conditions:
            preferences.extend(['low_sodium', 'omega3_rich', 'mediterranean'])
        
        if 'hypertension' in conditions:
            preferences.extend(['low_sodium', 'dash_diet', 'potassium_rich'])
        
        if 'obesity' in conditions:
            preferences.extend(['portion_controlled', 'low_calorie', 'high_protein'])
        
        # Age-based preferences
        if age > 60:
            preferences.extend(['calcium_rich', 'vitamin_d_rich'])
        
        # Return most relevant preference
        if preferences:
            return np.random.choice(preferences)
        else:
            return 'balanced'
    
    def prepare_features(self, df):
        """Prepare features for machine learning"""
        print("Preparing features...")
        
        # Create feature matrix
        features = []
        
        # Numerical features
        numerical_cols = ['age', 'height', 'weight', 'bmi', 'systolic_bp', 
                         'diastolic_bp', 'blood_sugar', 'daily_calories']
        
        for col in numerical_cols:
            features.append(df[col].values)
        
        # Encode categorical features
        # Gender
        gender_encoder = LabelEncoder()
        gender_encoded = gender_encoder.fit_transform(df['gender'])
        features.append(gender_encoded)
        self.encoders['gender'] = gender_encoder
        
        # Activity level
        activity_encoder = LabelEncoder()
        activity_encoded = activity_encoder.fit_transform(df['activity_level'])
        features.append(activity_encoded)
        self.encoders['activity'] = activity_encoder
        
        # Health conditions (binary encoding)
        condition_types = ['diabetes', 'heart_disease', 'hypertension', 'obesity']
        for condition in condition_types:
            condition_feature = df['conditions'].str.contains(condition, na=False).astype(int)
            features.append(condition_feature.values)
        
        # Combine all features
        X = np.column_stack(features)
        
        # Target variable (meal preferences)
        preference_encoder = LabelEncoder()
        y = preference_encoder.fit_transform(df['meal_preference'])
        self.encoders['meal_preference'] = preference_encoder
        
        print(f"Feature matrix shape: {X.shape}")
        print(f"Target classes: {preference_encoder.classes_}")
        
        return X, y
    
    def train_models(self, X, y):
  
        print("Training machine learning models...")

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['main'] = scaler

        # Initialize models
        rf_model = RandomForestClassifier(
    n_estimators=300,          # More trees = better generalization
    max_depth=None,            # Let trees grow fully
    min_samples_split=5,       # Avoid overfitting on small splits
    min_samples_leaf=3,        # Require more samples at leaf
    max_features='sqrt',       # Feature bagging for diversity
    class_weight='balanced',   # Handle class imbalance
    random_state=42,
    n_jobs=-1                  # Use all cores for training
)
        gb_model = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=6,
            random_state=42
        )

        models = {
            'random_forest': rf_model,
            'gradient_boosting': gb_model
        }

        best_model = None
        best_score = 0

        for name, model in models.items():
            print(f"Training {name.replace('_', ' ').title()}...")

            model.fit(X_train_scaled, y_train)

            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            y_pred = model.predict(X_test_scaled)
            test_accuracy = accuracy_score(y_test, y_pred)

            print(f"\n{name.upper()} Results:")
            print(f"CV Score: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
            print(f"Test Accuracy: {test_accuracy:.3f}")

            # Conditional selection
            if name == 'gradient_boosting':
                if test_accuracy >= 0.7:
                    print("Gradient Boosting meets accuracy threshold (>= 0.7).")
                    if test_accuracy > best_score:
                        best_model = model
                        best_score = test_accuracy
                        self.models['best'] = model
                else:
                    print("Gradient Boosting rejected: accuracy < 0.7")
            else:
                if test_accuracy > best_score:
                    best_model = model
                    best_score = test_accuracy
                    self.models['best'] = model

        print(f"\nBest model accuracy: {best_score:.3f}")

        # Feature importance (if RF is selected)
        if isinstance(best_model, RandomForestClassifier):
            feature_names = (
                ['age', 'height', 'weight', 'bmi', 'systolic_bp',
                'diastolic_bp', 'blood_sugar', 'daily_calories',
                'gender', 'activity_level'] +
                ['diabetes', 'heart_disease', 'hypertension', 'obesity']
            )

            importances = best_model.feature_importances_
            feature_importance = list(zip(feature_names, importances))
            feature_importance.sort(key=lambda x: x[1], reverse=True)

            print("\nTop 5 Feature Importances:")
            for feature, importance in feature_importance[:5]:
                print(f"{feature}: {importance:.3f}")

        return best_model, X_test_scaled, y_test

    
    def save_models(self):
        """Save trained models and encoders"""
        print("Saving models...")
        
        # Save main model
        if 'best' in self.models:
            with open(f'{self.model_dir}/diet_model.pkl', 'wb') as f:
                pickle.dump(self.models['best'], f)
        
        # Save scaler
        if 'main' in self.scalers:
            with open(f'{self.model_dir}/scaler.pkl', 'wb') as f:
                pickle.dump(self.scalers['main'], f)
        
        # Save encoders
        with open(f'{self.model_dir}/encoders.pkl', 'wb') as f:
            pickle.dump(self.encoders, f)
        
        # Save model metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'model_type': 'RandomForestClassifier',
            'feature_count': len(self.encoders),
            'classes': self.encoders['meal_preference'].classes_.tolist()
        }
        
        with open(f'{self.model_dir}/model_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Models saved successfully!")
    
    def create_nutrition_rules(self):
        """Create evidence-based nutrition rules"""
        print("Creating nutrition rules database...")
        
        # Medical guidelines from WHO, ADA, AHA
        nutrition_rules = {
            "macronutrient_ratios": {
                "balanced": {"carbs": 0.50, "protein": 0.20, "fat": 0.30},
                "low_carb": {"carbs": 0.30, "protein": 0.30, "fat": 0.40},
                "high_protein": {"carbs": 0.40, "protein": 0.35, "fat": 0.25},
                "mediterranean": {"carbs": 0.45, "protein": 0.20, "fat": 0.35}
            },
            "daily_limits": {
                "sodium_mg": {
                    "normal": 2300,
                    "hypertension": 1500,
                    "heart_disease": 2000
                },
                "sugar_g": {
                    "normal": 50,
                    "diabetes": 25,
                    "obesity": 30
                },
                "fiber_g": {
                    "minimum": 25,
                    "diabetes": 35,
                    "heart_disease": 30
                }
            },
            "meal_timing": {
                "diabetes": {
                    "meals_per_day": 6,
                    "carb_distribution": "even",
                    "max_carbs_per_meal": 45
                },
                "obesity": {
                    "meals_per_day": 5,
                    "largest_meal": "breakfast",
                    "evening_cutoff": "19:00"
                }
            },
            "food_groups": {
                "diabetes_friendly": [
                    "non-starchy vegetables", "lean proteins", "whole grains",
                    "legumes", "nuts", "seeds", "low-fat dairy"
                ],
                "heart_healthy": [
                    "fatty fish", "olive oil", "nuts", "whole grains",
                    "fruits", "vegetables", "legumes"
                ],
                "hypertension_friendly": [
                    "leafy greens", "berries", "bananas", "beets",
                    "oats", "garlic", "low-sodium foods"
                ]
            }
        }
        
        with open(f'{self.data_dir}/nutrition_rules.json', 'w') as f:
            json.dump(nutrition_rules, f, indent=2)
        
        print("Nutrition rules created!")
    
    def run_full_training(self):
        """Run complete model training pipeline"""
        print("Starting full AI model training pipeline...")
        print("=" * 50)
        
        # Generate synthetic data
        df = self.generate_synthetic_data()
        
        # Prepare features
        X, y = self.prepare_features(df)
        
        # Train models
        best_model, X_test, y_test = self.train_models(X, y)
        
        # Save everything
        self.save_models()
        
        # Create nutrition rules
        self.create_nutrition_rules()
        
        print("\n" + "=" * 50)
        print("Training completed successfully!")
        print(f"Models saved to: {self.model_dir}")
        print(f"Data saved to: {self.data_dir}")
        
        return best_model

def main():
    """Main training function"""
    trainer = DietModelTrainer()
    model = trainer.run_full_training()
    
    print("\nTo use the trained model:")
    print("1. Start the Flask app: python app.py")
    print("2. The model will automatically load and provide AI-powered recommendations")
    print("3. Retrain anytime by running: python model_training.py")

if __name__ == "__main__":
    main()