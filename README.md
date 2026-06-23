# 🍳 Recipe Preparation Agent

A smart recipe recommendation web application built using **Python, Flask, and Google Gemini API**. The application suggests recipes based on user-provided ingredients, provides ingredient substitutions, and dynamically generates new recipes using AI if no local database match is found.

---

## 🚀 Key Features

*   **Intelligent Local Retrieval:** Search algorithm that matches user ingredients with recipes stored in a local JSON database.
*   **50% Match Threshold Logic:** If a local recipe matches 50% or more of the required ingredients, it is loaded from the database to save API costs and reduce latency.
*   **AI Chef Recipe Generator:** If no local match reaches the 50% threshold, the backend calls the Google Gemini API (`gemini-2.0-flash`) to dynamically generate a complete recipe.
*   **Automated Caching:** Newly generated AI recipes are structured as JSON and appended back to the local database, allowing offline retrieval next time.
*   **Ingredient Substitutions:** Recommends alternative ingredients for missing items.
*   **Modern Glassmorphism UI:** Features a responsive, animated dark-mode interface built with CSS variables and blur effects.

---

## 📂 Project Structure

```text
recipe-agent/
│
├── app.py                  # Flask Backend logic & API Integrations
├── recipes.json            # Local JSON database (cached recipes)
├── .env.example            # Environment variables template
├── templates/
│   └── index.html          # Web interface layout & dynamic JavaScript
├── static/
│   └── style.css           # Glassmorphic responsive styling
└── README.md               # Setup & Documentation
🛠️ Step-by-Step Installation & Setup (For New Laptop)
Follow these steps to set up and run this project on a new machine:

1. Clone the Repository
Clone the project repository using Git:

bash


git clone https://github.com/YASHBalaji-7/recipe-agent.git
cd recipe-agent
2. Create a Virtual Environment
Initialize a clean Python virtual environment to avoid package conflicts:

bash


python -m venv venv
3. Activate the Virtual Environment
Windows (PowerShell):
powershell


venv\Scripts\Activate.ps1
Windows (Command Prompt):
cmd


venv\Scripts\activate.bat
macOS / Linux:
source venv/bin/activate
4. Install Dependencies
Install all required libraries using pip:
pip install Flask google-genai python-dotenv
5. Setup your API Key
The application requires a Google Gemini API Key to generate new recipes.

Get a free API Key from Google AI Studio.
Copy the .env.example file and rename it to .env:
copy .env.example .env
Open the newly created .env file and paste your API Key:
GEMINI_API_KEY=your_actual_gemini_api_key_here
6. Run the Application
Start the Flask local development server:
python app.py
7. Access in Browser
Open your browser and navigate to:
http://127.0.0.1:5000