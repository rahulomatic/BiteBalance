from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Database configuration
DATABASE = 'diet_planner.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User profiles table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            weight REAL,
            height REAL,
            activity_level TEXT,
            medical_conditions TEXT,
            dietary_preferences TEXT,
            allergies TEXT,
            dislikes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Diet plans table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS diet_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_date DATE NOT NULL,
            breakfast TEXT NOT NULL,
            lunch TEXT NOT NULL,
            dinner TEXT NOT NULL,
            snacks TEXT,
            total_calories INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Diet recommendation engine using rule-based logic
import random

class DietRecommendationEngine:
    def __init__(self):
        self.foods = {
            'breakfast': {
                'diabetic_friendly': [
                    {'name': 'Steel-cut oats with chia seeds and berries', 'type': 'vegan'},
                    {'name': 'Besan chilla with mixed vegetables', 'type': 'vegan'},
                    {'name': 'Multigrain toast with avocado and boiled egg', 'type': 'eggetarian'},
                    {'name': 'Quinoa porridge with nuts', 'type': 'vegan'},
                    {'name': 'Moong dal dosa with coconut chutney (no sugar)', 'type': 'vegan'},
                    {'name': 'Low-fat paneer and spinach wrap', 'type': 'vegetarian'}
                ],
                'heart_healthy': [
                    {'name': 'Oats with ground flaxseed and almond milk', 'type': 'vegan'},
                    {'name': 'Vegetable upma with minimal oil', 'type': 'vegan'},
                    {'name': 'Ragi porridge with banana', 'type': 'vegan'},
                    {'name': 'Sprouted moong salad with lemon dressing', 'type': 'vegan'},
                    {'name': 'Boiled egg whites and fruit bowl', 'type': 'eggetarian'},
                    {'name': 'Whole wheat toast with almond butter', 'type': 'vegan'}
                ],
                'general': [
                    {'name': 'Idli with sambhar', 'type': 'vegan'},
                    {'name': 'Vegetable poha', 'type': 'vegan'},
                    {'name': 'Vegetable paratha with curd', 'type': 'vegetarian'},
                    {'name': 'Masala omelet with toast', 'type': 'eggetarian'},
                    {'name': 'Boiled egg and banana smoothie', 'type': 'eggetarian'}
                ]
            },
            'lunch': {
                'diabetic_friendly': [
                    {'name': 'Brown rice with rajma and salad', 'type': 'vegan'},
                    {'name': 'Whole wheat roti with methi dal and sautéed spinach', 'type': 'vegan'},
                    {'name': 'Grilled tofu with stir-fried veggies', 'type': 'vegan'},
                    {'name': 'Vegetable quinoa bowl with chickpeas', 'type': 'vegan'},
                    {'name': 'Grilled salmon with greens', 'type': 'non_vegetarian'}
                ],
                'heart_healthy': [
                    {'name': 'Barley and lentil soup with whole grain roll', 'type': 'vegan'},
                    {'name': 'Mixed veg curry with jowar roti', 'type': 'vegan'},
                    {'name': 'Low-oil rajma chawal with cucumber raita', 'type': 'vegetarian'},
                    {'name': 'Grilled chicken breast with sautéed vegetables', 'type': 'non_vegetarian'},
                    {'name': 'Tofu stir-fry with brown rice', 'type': 'vegan'}
                ],
                'general': [
                    {'name': 'Rice with dal and vegetables', 'type': 'vegan'},
                    {'name': 'Roti with paneer bhurji', 'type': 'vegetarian'},
                    {'name': 'Chicken curry with roti', 'type': 'non_vegetarian'},
                    {'name': 'Fish fry with rice and cucumber salad', 'type': 'non_vegetarian'},
                    {'name': 'Vegetable biryani', 'type': 'vegetarian'}
                ]
            },
            'dinner': {
                'diabetic_friendly': [
                    {'name': 'Lentil soup with mixed greens', 'type': 'vegan'},
                    {'name': 'Quinoa salad with tofu and seeds', 'type': 'vegan'},
                    {'name': 'Vegetable stew with millets', 'type': 'vegan'},
                    {'name': 'Stir-fried broccoli with paneer', 'type': 'vegetarian'},
                    {'name': 'Grilled chicken breast with lettuce wrap', 'type': 'non_vegetarian'}
                ],
                'heart_healthy': [
                    {'name': 'Vegetable khichdi with flaxseed tadka', 'type': 'vegan'},
                    {'name': 'Clear vegetable soup and whole wheat toast', 'type': 'vegan'},
                    {'name': 'Palak tofu curry with phulka', 'type': 'vegan'},
                    {'name': 'Grilled fish with steamed veggies', 'type': 'non_vegetarian'},
                    {'name': 'Chicken stew with ragi roti', 'type': 'non_vegetarian'}
                ],
                'general': [
                    {'name': 'Roti with mixed vegetable sabzi', 'type': 'vegan'},
                    {'name': 'Pulao with raita', 'type': 'vegetarian'},
                    {'name': 'Dal and chapati', 'type': 'vegan'},
                    {'name': 'Fish curry with brown rice', 'type': 'non_vegetarian'},
                    {'name': 'Chicken and vegetable soup with toast', 'type': 'non_vegetarian'}
                ]
            },
            'snacks': {
                'diabetic_friendly': [
                    {'name': 'Roasted chana or fox nuts', 'type': 'vegan'},
                    {'name': 'Apple slices with peanut butter (no sugar added)', 'type': 'vegan'},
                    {'name': 'Greek yogurt (unsweetened) with flaxseed', 'type': 'vegetarian'},
                    {'name': 'Boiled egg whites', 'type': 'eggetarian'},
                    {'name': 'Cucumber and tomato slices with hummus', 'type': 'vegan'},
                    {'name': 'Grilled chicken strips with herbs', 'type': 'non_vegetarian'},
                    {'name': 'Tuna salad with lemon and olive oil', 'type': 'non_vegetarian'}
                ],
                'heart_healthy': [
                    {'name': 'Fresh fruit bowl with chia', 'type': 'vegan'},
                    {'name': 'Air-popped popcorn with herbs', 'type': 'vegan'},
                    {'name': 'Low-fat yogurt with ground flaxseed', 'type': 'vegetarian'},
                    {'name': 'Mixed nuts (unsalted, limited quantity)', 'type': 'vegan'},
                    {'name': 'Carrot sticks with hummus', 'type': 'vegan'},
                    {'name': 'Grilled salmon bites with lime zest', 'type': 'non_vegetarian'},
                    {'name': 'Boiled egg with black pepper and herbs', 'type': 'eggetarian'}
                ],
                'general': [
                    {'name': 'Banana and nuts smoothie', 'type': 'vegetarian'},
                    {'name': 'Vegetable sandwich (whole wheat bread)', 'type': 'vegetarian'},
                    {'name': 'Bhel puri (with puffed rice and veggies)', 'type': 'vegan'},
                    {'name': 'Lassi (low sugar)', 'type': 'vegetarian'},
                    {'name': 'Boiled corn with lemon and spices', 'type': 'vegan'},
                    {'name': 'Chicken sausage slices with mustard dip', 'type': 'non_vegetarian'},
                    {'name': 'Deviled eggs (light mayo, spices)', 'type': 'eggetarian'}
                ]
            }
        }

    def generate_plan(self, profile):
        conditions = profile.get('medical_conditions', '').lower().strip()
        dietary_pref = profile.get('dietary_preferences', 'vegetarian').lower().strip()

        if 'diabetes' in conditions:
            category = 'diabetic_friendly'
        elif 'hypertension' in conditions or 'heart' in conditions:
            category = 'heart_healthy'
        else:
            category = 'general'

        def filter_foods(food_list, diet_type):
            types = {
                'vegan': ['vegan'],
                'vegetarian': ['vegan', 'vegetarian'],
                'eggetarian': ['eggetarian'],
                'non_vegetarian': ['non_vegetarian', 'eggetarian']
            }.get(diet_type, ['non_vegetarian', 'eggetarian'])
            return [item['name'] for item in food_list if item['type'] in types]

        plan = {
            'breakfast': random.choice(filter_foods(self.foods['breakfast'][category], dietary_pref)) or 'Oats with fruits',
            'lunch': random.choice(filter_foods(self.foods['lunch'][category], dietary_pref)) or 'Dal rice with vegetables',
            'dinner': random.choice(filter_foods(self.foods['dinner'][category], dietary_pref)) or 'Roti with vegetables',
            'snacks': random.choice(filter_foods(self.foods['snacks'][category], dietary_pref)) or 'Fresh fruits'
        }

        calories = 1800
        if 'diabetes' in conditions:
            calories = 1500
        elif 'hypertension' in conditions:
            calories = 1600

        if profile.get('age', 0) > 50:
            calories -= 100
        if profile.get('gender', '').lower() == 'male':
            calories += 200

        plan['total_calories'] = calories
        plan['notes'] = self._generate_notes(conditions, dietary_pref)
        return plan

    def _generate_notes(self, conditions, dietary_pref):
        notes = []
        if 'diabetes' in conditions:
            notes += ["• Avoid sugar and refined carbs", "• Include high-fiber foods", "• Eat small frequent meals"]
        if 'hypertension' in conditions or 'heart' in conditions:
            notes += ["• Limit salt intake", "• Include omega-3 rich foods", "• Avoid processed foods"]
        if 'vegetarian' in dietary_pref:
            notes += ["• Ensure adequate protein from legumes and dairy", "• Include B12 and iron-rich foods"]
        elif 'eggetarian' in dietary_pref:
            notes += ["• Eggs are a great protein source", "• Avoid frying eggs; boil or poach instead"]
        notes += ["• Drink plenty of water", "• Exercise regularly"]
        return '\n'.join(notes)

# Example usage
diet_engine = DietRecommendationEngine()

@app.route('/')
def home():
    """Home page"""
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')
        
        # Check if user exists
        conn = get_db_connection()
        existing_user = conn.execute(
            'SELECT id FROM users WHERE username = ? OR email = ?',
            (username, email)
        ).fetchone()
        
        if existing_user:
            flash('Username or email already exists', 'error')
            conn.close()
            return render_template('register.html')
        
        # Create user
        password_hash = generate_password_hash(password)
        conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('login.html')
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))



@app.route('/profile', methods=['GET', 'POST'])
def profile():
    """User profile management"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        weight = request.form.get('weight', '')
        height = request.form.get('height', '')
        activity_level = request.form['activity_level']

        # Get checkboxes for medical conditions
        conditions = []
        if request.form.get('diabetes'):
            conditions.append('Diabetes')
        if request.form.get('hypertension'):
            conditions.append('Hypertension')
        if request.form.get('heart_disease'):
            conditions.append('Heart Disease')
        if request.form.get('obesity'):
            conditions.append('Obesity')

        medical_conditions = ', '.join(conditions)
        dietary_preferences = request.form['dietary_preferences']
        allergies = request.form.get('allergies', '')
        dislikes = request.form.get('dislikes', '')

        # Validation
        if not name or not age or not gender:
            flash('Name, age, and gender are required', 'error')
            return render_template('profile.html')

        try:
            age = int(age)
            if age < 1 or age > 120:
                raise ValueError
        except ValueError:
            flash('Please enter a valid age', 'error')
            return render_template('profile.html')

        # Check if profile exists
        existing_profile = conn.execute(
            'SELECT id FROM user_profiles WHERE user_id = ?',
            (session['user_id'],)
        ).fetchone()

        if existing_profile:
            # Update existing profile
            conn.execute('''
                UPDATE user_profiles 
                SET name = ?, age = ?, gender = ?, weight = ?, height = ?, 
                    activity_level = ?, medical_conditions = ?, dietary_preferences = ?, 
                    allergies = ?, dislikes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (name, age, gender, weight, height, activity_level, 
                  medical_conditions, dietary_preferences, allergies, dislikes, session['user_id']))
        else:
            # Create new profile
            conn.execute('''
                INSERT INTO user_profiles 
                (user_id, name, age, gender, weight, height, activity_level, 
                 medical_conditions, dietary_preferences, allergies, dislikes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (session['user_id'], name, age, gender, weight, height, activity_level,
                  medical_conditions, dietary_preferences, allergies, dislikes))

        conn.commit()
        conn.close()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    # GET request - show existing profile
    profile_data = conn.execute(
        'SELECT * FROM user_profiles WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()
    conn.close()

    # Convert to dict and parse datetime fields
    if profile_data:
        profile_data = dict(profile_data)
        for field in ['created_at', 'updated_at']:
            if profile_data.get(field):
                try:
                    profile_data[field] = datetime.strptime(profile_data[field], '%Y-%m-%d')
                except ValueError:
                    profile_data[field] = datetime.strptime(profile_data[field], '%Y-%m-%d')

    # 👉 Add current time (without timezone logic)
    current_time = datetime.now().time()
    current_time_str = current_time.strftime('%I:%M:%S %p')

    return render_template('profile.html', profile=profile_data, current_time=current_time_str)




@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    profile = conn.execute(
        'SELECT * FROM user_profiles WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()
    
    latest_plan = conn.execute(
        'SELECT * FROM diet_plans WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
        (session['user_id'],)
    ).fetchone()
    
    conn.close()

    # Convert latest_plan to dict and fix created_at
    if latest_plan:
        latest_plan = dict(latest_plan)
        try:
            latest_plan['created_at'] = datetime.strptime(latest_plan['created_at'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # In case microseconds are included
            latest_plan['created_at'] = datetime.strptime(latest_plan['created_at'], '%Y-%m-%d %H:%M:%S.%f')

    return render_template('dashboard.html', profile=profile, diet_plan=latest_plan)


@app.route('/generate_plan')
def generate_plan():
    """Generate new diet plan"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    
    # Get user profile
    profile = conn.execute(
        'SELECT * FROM user_profiles WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()
    
    if not profile:
        flash('Please complete your profile first', 'error')
        conn.close()
        return redirect(url_for('profile'))
    
    # Generate diet plan
    plan = diet_engine.generate_plan(dict(profile))
    
    # Save to database
    conn.execute('''
        INSERT INTO diet_plans 
        (user_id, plan_date, breakfast, lunch, dinner, snacks, total_calories, notes)
        VALUES (?, DATE('now'), ?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], plan['breakfast'], plan['lunch'], 
          plan['dinner'], plan['snacks'], plan['total_calories'], plan['notes']))
    
    conn.commit()
    conn.close()
    
    flash('New diet plan generated successfully!', 'success')
    return redirect(url_for('view_plan'))

@app.route('/view_plan')
def view_plan():
    """View current diet plan"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    plan = conn.execute(
        'SELECT * FROM diet_plans WHERE user_id = ? ORDER BY created_at DESC LIMIT 1',
        (session['user_id'],)
    ).fetchone()

    profile = conn.execute(
        'SELECT * FROM user_profiles WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()

    conn.close()

    if not plan:
        flash('No diet plan found. Generate one first!', 'info')
        return redirect(url_for('dashboard'))

    # Convert to mutable dict and parse datetime
    plan = dict(plan)
    if isinstance(plan['created_at'], str):
        try:
            plan['created_at'] = datetime.strptime(plan['created_at'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # In case SQLite uses microseconds
            plan['created_at'] = datetime.strptime(plan['created_at'], '%Y-%m-%d %H:%M:%S.%f')

    return render_template('diet_plan.html', plan=plan, profile=profile)

@app.route('/plan_history')
def plan_history():
    """View diet plan history"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()

    # Fetch last 10 plans
    raw_plans = conn.execute(
        'SELECT * FROM diet_plans WHERE user_id = ? ORDER BY created_at DESC LIMIT 10',
        (session['user_id'],)
    ).fetchall()

    conn.close()

    # Convert to list of dicts and parse created_at
    plans = []
    for row in raw_plans:
        plan = dict(row)
        if plan.get('created_at'):
            try:
                plan['created_at'] = datetime.strptime(plan['created_at'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    plan['created_at'] = datetime.strptime(plan['created_at'], '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    plan['created_at'] = None
        plans.append(plan)

    # 👉 Add current time
    current_time = datetime.now().time()
    current_time_str = current_time.strftime('%I:%M:%S %p')

    return render_template('plan_history.html', plans=plans, current_time=current_time_str)
if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)