import json
import re
import random
from datetime import datetime
import os

class Sabbot:
    """Offline AI chatbot for diet and nutrition assistance"""
    
    def __init__(self):
        self.responses_path = 'data/chatbot_responses.json'
        self.conversation_history = []
        self.load_responses()
        
    def load_responses(self):
        """Load chatbot responses and patterns"""
        try:
            if os.path.exists(self.responses_path):
                with open(self.responses_path, 'r') as f:
                    self.responses = json.load(f)
            else:
                self.responses = self.get_default_responses()
                self.save_responses()
        except Exception as e:
            print(f"Error loading chatbot responses: {e}")
            self.responses = self.get_default_responses()
    
    def get_default_responses(self):
        """Default chatbot responses for diet and health queries"""
        return {
            "greetings": {
                "patterns": ["hello", "hi", "hey", "good morning", "good afternoon"],
                "responses": [
                    "Hello! I'm Sabbot, your personal diet assistant. How can I help you with your nutrition goals today?",
                    "Hi there! I'm here to help you with diet planning and nutrition questions. What would you like to know?",
                    "Welcome! I'm Sabbot, ready to assist you with healthy eating and meal planning. How can I help?"
                ]
            },
            "diabetes": {
                "patterns": ["diabetes", "blood sugar", "glucose", "diabetic", "insulin"],
                "responses": [
                    "For diabetes management, focus on complex carbohydrates, lean proteins, and high-fiber foods. Limit simple sugars and refined carbs.",
                    "Managing diabetes involves eating regular meals, monitoring carb intake (45g per meal), and choosing low glycemic index foods.",
                    "Key diabetes-friendly foods include: whole grains, legumes, non-starchy vegetables, lean proteins, and healthy fats like nuts and olive oil."
                ]
            },
            "heart_disease": {
                "patterns": ["heart", "cardiovascular", "cholesterol", "heart disease", "cardiac"],
                "responses": [
                    "For heart health, follow a Mediterranean-style diet rich in omega-3 fatty acids, fiber, and antioxidants. Limit saturated fats and sodium.",
                    "Heart-healthy foods include: fatty fish, olive oil, nuts, whole grains, fruits, and vegetables. Avoid trans fats and processed foods.",
                    "The DASH diet is excellent for heart health - emphasize fruits, vegetables, whole grains, and lean proteins while limiting sodium to 2300mg daily."
                ]
            },
            "hypertension": {
                "patterns": ["blood pressure", "hypertension", "high bp", "pressure"],
                "responses": [
                    "For high blood pressure, follow the DASH diet: increase potassium-rich foods, limit sodium to 1500mg daily, and eat plenty of fruits and vegetables.",
                    "Foods that help lower blood pressure include: leafy greens, berries, beets, oats, bananas, garlic, and fatty fish.",
                    "Reduce sodium by avoiding processed foods, canned soups, and restaurant meals. Use herbs and spices for flavor instead of salt."
                ]
            },
            "weight_loss": {
                "patterns": ["weight loss", "lose weight", "obesity", "overweight", "diet"],
                "responses": [
                    "For healthy weight loss, create a moderate calorie deficit (500 calories/day), focus on protein (1.2g per kg body weight), and eat plenty of vegetables.",
                    "Effective weight loss strategies: portion control, regular meals, high-protein foods, fiber-rich vegetables, and staying hydrated.",
                    "Choose nutrient-dense, low-calorie foods like vegetables, lean proteins, and whole grains. Avoid liquid calories and processed snacks."
                ]
            },
            "meal_planning": {
                "patterns": ["meal plan", "what to eat", "menu", "meals", "planning"],
                "responses": [
                    "A balanced meal should include: 1/2 plate vegetables, 1/4 plate lean protein, 1/4 plate whole grains, plus healthy fats.",
                    "Plan meals around your health conditions. Include variety, prepare in advance, and focus on whole, unprocessed foods.",
                    "Meal planning tips: batch cook proteins, prep vegetables, use herbs and spices for flavor, and keep healthy snacks available."
                ]
            },
            "nutrition": {
                "patterns": ["nutrition", "nutrients", "vitamins", "minerals", "healthy eating"],
                "responses": [
                    "Focus on getting nutrients from whole foods: colorful fruits and vegetables, lean proteins, whole grains, and healthy fats.",
                    "Key nutrients for health: fiber (25g daily), protein (0.8-1.2g per kg), omega-3 fatty acids, vitamins D and B12, and minerals like iron and calcium.",
                    "Eat a rainbow of colors to ensure diverse nutrients. Each color provides different antioxidants and phytonutrients."
                ]
            },
            "cooking": {
                "patterns": ["cooking", "recipe", "how to cook", "preparation", "cook"],
                "responses": [
                    "Healthy cooking methods: steaming, grilling, baking, sautéing with minimal oil, and roasting. Avoid deep frying.",
                    "Cooking tips: use herbs and spices instead of salt, cook vegetables until just tender, and don't overcook to preserve nutrients.",
                    "Meal prep ideas: batch cook grains and proteins, pre-cut vegetables, and prepare healthy snacks in advance."
                ]
            },
            "supplements": {
                "patterns": ["supplements", "vitamins", "pills", "supplement"],
                "responses": [
                    "Focus on getting nutrients from food first. Common supplements that may be beneficial: Vitamin D, B12 (for vegans), and omega-3 if you don't eat fish.",
                    "Consult your healthcare provider before starting supplements. Most nutrients are better absorbed from whole foods.",
                    "If you have specific deficiencies, targeted supplements may help, but a balanced diet should be your primary source of nutrients."
                ]
            },
            "exercise": {
                "patterns": ["exercise", "workout", "physical activity", "fitness"],
                "responses": [
                    "Combine diet with regular physical activity for best results. Aim for 150 minutes of moderate exercise weekly.",
                    "Exercise helps with blood sugar control, heart health, and weight management. Start slowly and gradually increase intensity.",
                    "Both cardio and strength training are important. Even a 10-minute walk after meals can help with blood sugar control."
                ]
            },
            "default": {
                "patterns": [],
                "responses": [
                    "I'm here to help with diet and nutrition questions. You can ask me about meal planning, specific health conditions, or healthy eating tips.",
                    "I can assist with diabetes, heart disease, hypertension, and weight management nutrition. What specific topic interests you?",
                    "Feel free to ask about healthy recipes, meal planning, or nutrition for your specific health needs. How can I help you today?"
                ]
            }
        }
    
    def save_responses(self):
        """Save responses to file"""
        os.makedirs('data', exist_ok=True)
        with open(self.responses_path, 'w') as f:
            json.dump(self.responses, f, indent=2)
    
    def get_response(self, user_message, user_data=None):
        """Generate response based on user message and context"""
        try:
            # Clean and normalize user message
            message = user_message.lower().strip()
            
            # Store conversation
            self.conversation_history.append({
                'user': user_message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Find matching pattern
            response_category = self.find_matching_category(message)
            
            # Get appropriate response
            if response_category:
                response = self.get_contextual_response(response_category, user_data)
            else:
                response = random.choice(self.responses['default']['responses'])
            
            # Add personalization if user data available
            if user_data:
                response = self.personalize_response(response, user_data)
            
            # Store bot response
            self.conversation_history.append({
                'bot': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            return "I'm sorry, I'm having trouble processing your request. Please try asking about diet, nutrition, or meal planning."
    
    def find_matching_category(self, message):
        """Find the best matching response category"""
        best_match = None
        max_matches = 0
        
        for category, data in self.responses.items():
            if category == 'default':
                continue
                
            patterns = data['patterns']
            matches = sum(1 for pattern in patterns if pattern in message)
            
            if matches > max_matches:
                max_matches = matches
                best_match = category
        
        return best_match
    
    def get_contextual_response(self, category, user_data):
        """Get response with context from user data"""
        responses = self.responses[category]['responses']
        base_response = random.choice(responses)
        
        # Add specific advice based on user's conditions
        if user_data and 'conditions' in user_data:
            conditions = user_data['conditions']
            
            if category == 'meal_planning' and conditions:
                if 'diabetes' in conditions:
                    base_response += " Since you have diabetes, focus on complex carbs and monitor portions."
                elif 'heart_disease' in conditions:
                    base_response += " For heart health, emphasize omega-3 rich foods and limit sodium."
                elif 'hypertension' in conditions:
                    base_response += " With high blood pressure, keep sodium under 1500mg daily."
                elif 'obesity' in conditions:
                    base_response += " For weight management, focus on portion control and high-protein foods."
        
        return base_response
    
    def personalize_response(self, response, user_data):
        """Add personalization based on user data"""
        try:
            # Add name if available
            if 'name' in user_data:
                response = f"{user_data['name']}, {response.lower()}"
            
            # Add calorie information if relevant
            if 'daily_calories' in user_data and 'calorie' in response.lower():
                calories = user_data['daily_calories']
                response += f" Based on your profile, aim for around {calories} calories daily."
            
            return response
        except:
            return response
    
    def get_meal_suggestions(self, meal_type, user_data):
        """Get specific meal suggestions"""
        suggestions = {
            'breakfast': [
                "Try oatmeal with berries and nuts",
                "Greek yogurt with fruit and granola",
                "Whole grain toast with avocado and eggs",
                "Smoothie with spinach, banana, and protein powder"
            ],
            'lunch': [
                "Quinoa salad with grilled chicken and vegetables",
                "Lentil soup with whole grain bread",
                "Salmon with brown rice and steamed broccoli",
                "Turkey and vegetable wrap with hummus"
            ],
            'dinner': [
                "Grilled fish with roasted vegetables",
                "Lean beef stir-fry with brown rice",
                "Chicken breast with sweet potato and green beans",
                "Tofu curry with quinoa and spinach"
            ],
            'snack': [
                "Apple slices with almond butter",
                "Greek yogurt with berries",
                "Handful of mixed nuts",
                "Hummus with vegetable sticks"
            ]
        }
        
        base_suggestions = suggestions.get(meal_type, suggestions['snack'])
        
        # Filter based on conditions
        if user_data and 'conditions' in user_data:
            conditions = user_data['conditions']
            filtered_suggestions = []
            
            for suggestion in base_suggestions:
                include = True
                
                # Filter for diabetes
                if 'diabetes' in conditions:
                    if any(word in suggestion.lower() for word in ['granola', 'sweet']):
                        include = False
                
                # Filter for heart disease
                if 'heart_disease' in conditions:
                    if 'beef' in suggestion.lower():
                        include = False
                
                if include:
                    filtered_suggestions.append(suggestion)
            
            return filtered_suggestions if filtered_suggestions else base_suggestions
        
        return base_suggestions
    
    def get_conversation_history(self):
        """Get recent conversation history"""
        return self.conversation_history[-10:]  # Last 10 exchanges