from flask import Flask, render_template, request, jsonify, session
import os
from datetime import datetime
import json
from models.diet_model import DietPlanner

from utils.health_calculator import HealthCalculator
from utils.meal_database import MealDatabase

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Initialize components
diet_planner = DietPlanner()

health_calc = HealthCalculator()
meal_db = MealDatabase()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assessment')
def assessment():
    return render_template('assessment.html')

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    try:
        # Extract user data from form
        user_data = {
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'height': float(request.form.get('height')),
            'weight': float(request.form.get('weight')),
            'activity_level': request.form.get('activity_level'),
            'systolic_bp': int(request.form.get('systolic_bp', 0)),
            'diastolic_bp': int(request.form.get('diastolic_bp', 0)),
            'blood_sugar': float(request.form.get('blood_sugar', 0)),
            'conditions': request.form.getlist('conditions'),
            'allergies': request.form.get('allergies', '').split(','),
            'dietary_preferences': request.form.getlist('dietary_preferences')
        }
        
        # Calculate BMI and health metrics
        user_data['bmi'] = health_calc.calculate_bmi(user_data['height'], user_data['weight'])
        user_data['bmr'] = health_calc.calculate_bmr(user_data)
        user_data['daily_calories'] = health_calc.calculate_daily_calories(user_data)
        
        # Generate meal plan using AI model
        meal_plan = diet_planner.generate_meal_plan(user_data)
        
        # Store in session for later reference
        session['user_data'] = user_data
        session['meal_plan'] = meal_plan
        
        return render_template('meal_plan.html', 
                             user_data=user_data, 
                             meal_plan=meal_plan,
                             health_metrics=health_calc.get_health_status(user_data))
        
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/api/meal_suggestions')
def meal_suggestions():
    try:
        meal_type = request.args.get('type', 'breakfast')
        user_data = session.get('user_data', {})
        
        suggestions = meal_db.get_meal_suggestions(meal_type, user_data)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/nutrition_info/<meal_id>')
def nutrition_info(meal_id):
    try:
        nutrition = meal_db.get_nutrition_info(meal_id)
        return render_template('nutrition_modal.html', nutrition=nutrition)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    # Ensure model directories exist
    os.makedirs('models/trained', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)