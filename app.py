import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini API client
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

# Helper function to read recipes from JSON
def load_recipes():
    try:
        with open('recipes.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Helper function to save recipe to JSON
def save_recipe(new_recipe):
    recipes = load_recipes()
    if not any(r['name'].lower() == new_recipe['name'].lower() for r in recipes):
        recipes.append(new_recipe)
        with open('recipes.json', 'w') as file:
            json.dump(recipes, file, indent=4)

# Function to search recipes based on user ingredients (with 50% match threshold)
def find_local_recipes(user_ingredients):
    recipes = load_recipes()
    matching_recipes = []
    user_ingredients = [i.strip().lower() for i in user_ingredients]
    
    for recipe in recipes:
        recipe_ingredients = [i.lower() for i in recipe['ingredients']]
        
        # User enter chesina ingredients, database recipes indicators matches overlap checking
        matches = set(user_ingredients).intersection(set(recipe_ingredients))
        
        if len(matches) > 0:
            # Match calculation based on recipe ingredients total size
            match_percentage = (len(matches) / len(recipe_ingredients)) * 100
            
            # CRITICAL THRESHOLD: Meeru enter chesina matches lo 50% kante ekkuva database values database size update lo match unteనే success local card count format loading chestundi
            if match_percentage >= 50.0:
                matching_recipes.append({
                    "recipe": recipe,
                    "match_percentage": round(match_percentage, 1),
                    "matched_ingredients": list(matches)
                })
            
    matching_recipes.sort(key=lambda x: x['match_percentage'], reverse=True)
    return matching_recipes

# AI Recipe Generator using new Client
def generate_ai_recipe(ingredients_list):
    if not client:
        print("API Key setup error. Please check your .env file.")
        return None
        
    ingredients_str = ", ".join(ingredients_list)
    prompt = f"""
    You are a professional chef. Create a delicious, logical recipe that can be made using these ingredients: {ingredients_str}.
    You can assume standard pantry items like salt, pepper, oil, and water are available.
    
    CRITICAL: You MUST respond ONLY with a raw JSON object and nothing else. No markdown formatting, no ```json wrappers.
    JSON structure:
    {{
        "name": "Creative Recipe Name",
        "ingredients": ["list", "of", "ingredients", "actually", "used"],
        "instructions": ["Step 1 direction", "Step 2 direction", "Step 3 direction"],
        "substitutions": {{
            "optional_ingredient_to_replace": "suggested_alternative"
        }}
    }}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        text = response.text.strip()
        
        # Clean potential markdown wrappers if Gemini returns them
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        recipe_data = json.loads(text.strip())
        save_recipe(recipe_data)
        return recipe_data
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    data = request.get_json()
    user_input = data.get('ingredients', '')
    
    if not user_input:
        return jsonify({"error": "Please provide ingredients."}), 400
        
    ingredients_list = [i.strip().lower() for i in user_input.split(',') if i.strip()]
    matched = find_local_recipes(ingredients_list)
    
    if matched:
        return jsonify({
            "source": "local",
            "recipes": matched
        })
    else:
        print("No local recipes match threshold. Calling Gemini AI...")
        ai_recipe = generate_ai_recipe(ingredients_list)
        if ai_recipe:
            return jsonify({
                "source": "ai",
                "recipes": [{
                    "recipe": ai_recipe,
                    "match_percentage": 100.0,
                    "matched_ingredients": ingredients_list
                }]
            })
        else:
            return jsonify({"error": "Could not generate recipe. Please try again with different ingredients."}), 500

if __name__ == '__main__':
    app.run(debug=True)