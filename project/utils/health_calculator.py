import math

class HealthCalculator:
    """Calculate health metrics and BMI classifications"""
    
    def calculate_bmi(self, height_cm, weight_kg):
        """Calculate BMI from height (cm) and weight (kg)"""
        try:
            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)
            return round(bmi, 1)
        except:
            return 0
    
    def get_bmi_category(self, bmi):
        """Get BMI category based on WHO classification"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def calculate_bmr(self, user_data):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        try:
            weight = user_data['weight']
            height = user_data['height']
            age = user_data['age']
            gender = user_data['gender']
            
            if gender.lower() == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161
            
            return round(bmr)
        except:
            return 1500  # Default fallback
    
    def calculate_daily_calories(self, user_data):
        """Calculate daily calorie needs based on activity level"""
        bmr = self.calculate_bmr(user_data)
        activity_level = user_data.get('activity_level', 'moderate')
        
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.55)
        daily_calories = bmr * multiplier
        
        return round(daily_calories)
    
    def get_blood_pressure_category(self, systolic, diastolic):
        """Categorize blood pressure based on AHA guidelines"""
        if systolic < 120 and diastolic < 80:
            return "Normal"
        elif systolic < 130 and diastolic < 80:
            return "Elevated"
        elif systolic < 140 or diastolic < 90:
            return "Stage 1 Hypertension"
        elif systolic < 180 or diastolic < 120:
            return "Stage 2 Hypertension"
        else:
            return "Hypertensive Crisis"
    
    def get_blood_sugar_category(self, blood_sugar, test_type='fasting'):
        """Categorize blood sugar levels"""
        if test_type == 'fasting':
            if blood_sugar < 100:
                return "Normal"
            elif blood_sugar < 126:
                return "Prediabetes"
            else:
                return "Diabetes"
        elif test_type == 'random':
            if blood_sugar < 140:
                return "Normal"
            elif blood_sugar < 200:
                return "Prediabetes"
            else:
                return "Diabetes"
        
        return "Unknown"
    
    def calculate_ideal_weight_range(self, height_cm, gender):
        """Calculate ideal weight range using BMI 18.5-24.9"""
        height_m = height_cm / 100
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 24.9 * (height_m ** 2)
        
        return {
            'min': round(min_weight, 1),
            'max': round(max_weight, 1)
        }
    
    def get_health_status(self, user_data):
        """Get comprehensive health status assessment"""
        try:
            bmi = user_data.get('bmi', 0)
            systolic = user_data.get('systolic_bp', 0)
            diastolic = user_data.get('diastolic_bp', 0)
            blood_sugar = user_data.get('blood_sugar', 0)
            
            status = {
                'bmi': {
                    'value': bmi,
                    'category': self.get_bmi_category(bmi),
                    'status': 'normal' if 18.5 <= bmi < 25 else 'attention'
                },
                'blood_pressure': {
                    'systolic': systolic,
                    'diastolic': diastolic,
                    'category': self.get_blood_pressure_category(systolic, diastolic),
                    'status': 'normal' if systolic < 120 and diastolic < 80 else 'attention'
                },
                'blood_sugar': {
                    'value': blood_sugar,
                    'category': self.get_blood_sugar_category(blood_sugar),
                    'status': 'normal' if blood_sugar < 100 else 'attention'
                },
                'ideal_weight': self.calculate_ideal_weight_range(
                    user_data.get('height', 170), 
                    user_data.get('gender', 'female')
                )
            }
            
            # Overall health score
            normal_count = sum(1 for metric in status.values() 
                             if isinstance(metric, dict) and metric.get('status') == 'normal')
            status['overall_score'] = f"{normal_count}/3"
            
            return status
            
        except Exception as e:
            return self.get_default_health_status()
    
    def get_default_health_status(self):
        """Default health status if calculation fails"""
        return {
            'bmi': {'value': 0, 'category': 'Unknown', 'status': 'unknown'},
            'blood_pressure': {'category': 'Unknown', 'status': 'unknown'},
            'blood_sugar': {'category': 'Unknown', 'status': 'unknown'},
            'overall_score': '0/3'
        }
    
    def get_health_recommendations(self, user_data):
        """Get personalized health recommendations"""
        recommendations = []
        health_status = self.get_health_status(user_data)
        
        # BMI recommendations
        bmi_status = health_status['bmi']['status']
        if bmi_status == 'attention':
            bmi_category = health_status['bmi']['category']
            if bmi_category == 'Overweight' or bmi_category == 'Obese':
                recommendations.append("Consider a calorie-controlled diet for healthy weight loss")
            elif bmi_category == 'Underweight':
                recommendations.append("Focus on nutrient-dense, calorie-rich foods to gain weight healthily")
        
        # Blood pressure recommendations
        bp_status = health_status['blood_pressure']['status']
        if bp_status == 'attention':
            recommendations.append("Follow a low-sodium DASH diet to help manage blood pressure")
            recommendations.append("Increase potassium-rich foods like bananas, spinach, and beans")
        
        # Blood sugar recommendations
        bs_status = health_status['blood_sugar']['status']
        if bs_status == 'attention':
            recommendations.append("Monitor carbohydrate intake and choose complex carbs")
            recommendations.append("Include high-fiber foods to help stabilize blood sugar")
        
        # General recommendations
        recommendations.extend([
            "Aim for at least 150 minutes of moderate exercise per week",
            "Stay hydrated with 8-10 glasses of water daily",
            "Include a variety of colorful fruits and vegetables in your diet"
        ])
        
        return recommendations