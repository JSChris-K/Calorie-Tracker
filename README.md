Calorie Tracker & Meal Recommendation App

   1. Problem & User

This project is designed to help individuals estimate their daily calorie needs and receive simple meal recommendations. It is intended for users who want a quick, personalized diet plan based on basic health paramaters.


   2. Data

The dataset used is a food nutrition dataset containing common food items and their nutritional values.

a. Source: Provided dataset from Kaggle(daily_food_nutrition_dataset.csv)
b. Access date: [24 April 2026]
c. Key fields:

  - Food_Item
  - Calories (kcal)
  - Protein (g)
  - Carbohydrates (g)
  - Fat (g)
  - Meal_Type (Breakfast, Lunch, Dinner)
  
   3. Methods

The application is built using Python and Streamlit. The main steps of the program include:

a. Load and clean the dataset (handle missing values and incorrect data types)
b. Take user inputs (weight, height, age, gender, activity level)
c. Calculate BMR and TDEE using standard formulas
d. Adjust calorie targets based on user goal (maintain, lose, gain)
e. Filter foods (included optional keto mode)
f. Generate meal recommendations (max 3 items per meal) as to prevent the system recommending 20 foods at once
g. Calculate total nutritional values for each meal
h. Display a 12-week weight projection using matplotlib

  4. Key Findings

- The app can generate structured meal plans split into breakfast, lunch, and dinner
- Keto filtering significantly reduces available food options
- Calorie targets can be approximated using simple greedy selection
- Data cleaning is essential to avoid type errors and incorrect calculations

5. How to Run

- save both app.py and daily_food_nutrition_datas.csv into the same folder
- open a code editor with python installed 
- import the folder with the previous files into the code editor.
- open app.py
-  Enter into terminal to:
  
a. Install required libraries:
   pip install streamlit
   pip install streamlit pandas matplotlib

b. Run the app:
   python -mstreamlit run app.py

c. Open the local URL provided by Streamlit in your browser/Should automatically open a window in your internet browser

6. Product / Demo

Demo Video: In the GitHub Repo

7. Limitations & Next Steps

Limitations:

- Meal selection uses a simple greedy approach and may not perfectly match calorie targets
- Dataset is limited and may not include all food options
- No user authentication or saving of preferences
- Keto mode may occasionally recommend higher calorie foods

Future improvements:

- Implement optimization to better match calorie goals
- Add more diverse and larger datasets
- Improve UI/UX and add visual dashboards
- Fix bugs
- Deploy the app online for easier access
