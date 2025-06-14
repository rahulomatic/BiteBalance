# HealthyDiet - Personalized Diet Planning for Chronic Health Conditions

A comprehensive Flask-based web application designed to provide personalized diet planning for individuals with chronic health conditions in India, addressing the shortage of dietitians and making nutritional guidance accessible to everyone.

## 🎯 Project Overview

HealthyDiet bridges the gap between chronic disease management and personalized nutrition by offering:
- **Condition-specific meal plans** for diabetes, hypertension, heart disease, and obesity
- **Indian cuisine focus** with authentic recipes and locally available ingredients
- **Science-based recommendations** following medical nutritional guidelines
- **User-friendly interface** accessible to all age groups

## 🚀 Features

### Core Functionality
- **User Registration & Authentication**: Secure account creation with password hashing
- **Health Profile Management**: Comprehensive health and dietary preference tracking
- **AI-Powered Diet Generation**: Rule-based meal planning system
- **Personalized Dashboard**: Overview of health status and current diet plans
- **Diet Plan History**: Track and review previous meal plans
- **Print-Friendly Plans**: Easy-to-print diet plans for offline use

### Health Conditions Supported
- Type 1 & Type 2 Diabetes
- Hypertension (High Blood Pressure)
- Heart Disease
- Obesity
- General health maintenance

### Dietary Preferences
- Vegetarian
- Non-Vegetarian
- Vegan
- Eggetarian
- Allergy and dislike management

## 🛠 Technology Stack

- **Backend**: Flask (Python 3.7+)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5.3
- **Templating**: Jinja2
- **Security**: Werkzeug password hashing, Flask sessions
- **Icons**: Bootstrap Icons
- **Styling**: Custom CSS with responsive design

## 📁 Project Structure

```
healthydiet/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── diet_planner.db       # SQLite database (auto-created)
├── README.md             # Project documentation
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template with navigation
│   ├── home.html         # Landing page
│   ├── register.html     # User registration
│   ├── login.html        # User login
│   ├── profile.html      # Health profile management
│   ├── dashboard.html    # User dashboard
│   ├── diet_plan.html    # Detailed diet plan view
│   └── plan_history.html # Diet plan history
└── static/
    └── css/
        └── style.css     # Custom styles and responsive design
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**
   ```bash
   # If using git
   git clone <repository-url>
   cd healthydiet
   
   # Or download and extract the files
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - Start by registering a new account

### First Time Setup
1. **Register**: Create a new account with username, email, and password
2. **Complete Profile**: Fill in your health information and dietary preferences
3. **Generate Plan**: Create your first personalized diet plan
4. **Follow & Track**: Use the dashboard to monitor your progress

## 📊 Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: User email address
- `password_hash`: Securely hashed password
- `created_at`: Account creation timestamp

### User Profiles Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `name`: Full name
- `age`: Age in years
- `gender`: Male/Female/Other
- `weight`: Weight in kg (optional)
- `height`: Height in cm (optional)
- `activity_level`: Physical activity level
- `medical_conditions`: Comma-separated health conditions
- `dietary_preferences`: Food preferences
- `allergies`: Food allergies
- `dislikes`: Foods to avoid

### Diet Plans Table
- `id`: Primary key
- `user_id`: Foreign key to users table
- `plan_date`: Date of plan generation
- `breakfast`: Breakfast recommendation
- `lunch`: Lunch recommendation
- `dinner`: Dinner recommendation
- `snacks`: Snack recommendations
- `total_calories`: Daily calorie target
- `notes`: Dietary guidelines and tips

## 🧠 Diet Recommendation Engine

The application uses a rule-based system to generate personalized meal plans:

### Condition-Based Logic
- **Diabetes**: High-fiber, low-sugar meals with complex carbohydrates
- **Hypertension**: Low-sodium options with heart-healthy ingredients
- **Heart Disease**: Omega-3 rich foods, minimal processed ingredients
- **Obesity**: Calorie-controlled portions with nutrient-dense foods

### Indian Cuisine Integration
- Authentic Indian recipes and ingredients
- Regional food preferences
- Seasonal availability considerations
- Cultural dietary practices

### Calorie Calculation
- Age and gender-based baseline
- Activity level adjustments
- Medical condition modifications
- Weight management goals

## 🎨 User Interface

### Design Principles
- **Medical-grade trust**: Professional, clean interface
- **Accessibility**: High contrast, readable fonts, keyboard navigation
- **Responsive**: Mobile-first design for all devices
- **Intuitive**: Clear navigation and user flows

### Key Pages
- **Landing Page**: Feature overview and registration
- **Dashboard**: Health summary and quick actions
- **Profile**: Comprehensive health information form
- **Diet Plan**: Detailed meal recommendations with timing
- **History**: Track progress over time

## 🔒 Security Features

- **Password Security**: Werkzeug password hashing
- **Session Management**: Flask secure sessions
- **Input Validation**: Server-side form validation
- **SQL Injection Protection**: Parameterized queries
- **XSS Prevention**: Template auto-escaping

## 📱 Mobile Responsiveness

- Bootstrap 5.3 responsive grid system
- Mobile-optimized navigation
- Touch-friendly interface elements
- Optimized for screens 320px and above

## 🔧 Customization

### Adding New Health Conditions
1. Update the `DietRecommendationEngine` class in `app.py`
2. Add condition-specific food recommendations
3. Update the profile form in `templates/profile.html`
4. Modify the recommendation logic

### Adding New Food Items
1. Extend the `foods` dictionary in the recommendation engine
2. Categorize by meal type and health condition
3. Include nutritional considerations

### Styling Modifications
1. Edit `static/css/style.css` for visual changes
2. Modify Bootstrap classes in templates
3. Update color schemes and typography

## 🚀 Deployment Options

### Local Development
- Run directly with `python app.py`
- Access at `http://localhost:5000`

### Production Deployment
- Use WSGI server like Gunicorn
- Configure reverse proxy (Nginx)
- Set up SSL certificates
- Use production database (PostgreSQL/MySQL)

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=your-database-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

For support and questions:
- Check the documentation
- Review the code comments
- Test with sample data
- Verify all dependencies are installed

## 🔮 Future Enhancements

- **Mobile App**: React Native or Flutter app
- **API Integration**: RESTful API for third-party access
- **Advanced Analytics**: Progress tracking and insights
- **Nutritionist Chat**: Connect with certified dietitians
- **Meal Planning**: Weekly and monthly planning
- **Shopping Lists**: Automated grocery lists
- **Recipe Database**: Detailed cooking instructions
- **Community Features**: User forums and success stories

## 📈 Impact

This application addresses a critical healthcare need in India:
- **300M+ Indians** with chronic diseases
- **Limited access** to personalized nutrition advice
- **Cultural relevance** with Indian cuisine focus
- **Free accessibility** for all economic backgrounds

---

**HealthyDiet** - Empowering healthy living through personalized nutrition for chronic disease management.