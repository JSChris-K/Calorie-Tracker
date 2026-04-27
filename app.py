import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# LOAD & CLEAN DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("daily_food_nutrition_dataset.csv")

    # Clean column names (removes hidden spaces)
    df.columns = df.columns.str.strip()

    # Convert numeric columns safely
    numeric_cols = [
        "Calories (kcal)",
        "Protein (g)",
        "Carbohydrates (g)",
        "Fat (g)"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop bad rows
    df = df.dropna(subset=numeric_cols)

    # Clean Meal_Type just in case
    if "Meal_Type" in df.columns:
        df["Meal_Type"] = df["Meal_Type"].astype(str).str.strip()

    return df

df = load_data()

# ---------------------------
# USER INPUTS
# ---------------------------
st.title("Calorie & Meal Planner")

weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
height = st.number_input("Height (cm)", 120.0, 220.0, 170.0)
age = st.number_input("Age", 10, 100, 20)

gender = st.selectbox("Gender", ["Male", "Female"])

activity_dict = {
    "Sedentary": 1.2,
    "Lightly active": 1.375,
    "Moderately active": 1.55,
    "Very active": 1.725
}
activity = activity_dict[st.selectbox("Activity Level", list(activity_dict.keys()))]

goal = st.selectbox("Goal", ["Maintain", "Lose Weight", "Gain Weight"])

# ---------------------------
# DIET OPTION
# ---------------------------
st.subheader("Diet Preferences")
keto_mode = st.toggle("Keto Mode (low carbs ≤ 10g)")

# ---------------------------
# CALCULATIONS
# ---------------------------
def calculate_bmr(w, h, a, g):
    return 10*w + 6.25*h - 5*a + (5 if g == "Male" else -161)

def calculate_tdee(w, h, a, g, act):
    return calculate_bmr(w, h, a, g) * act

tdee = calculate_tdee(weight, height, age, gender, activity)

if goal == "Lose Weight":
    target_calories = tdee - 500
elif goal == "Gain Weight":
    target_calories = tdee + 500
else:
    target_calories = tdee

st.write(f"### Target Calories: {target_calories:.0f} kcal")

# ---------------------------
# FILTER DATA
# ---------------------------
filtered_df = df.copy()

# Remove extreme foods
filtered_df = filtered_df[filtered_df["Calories (kcal)"] < 800]

# Keto filter
if keto_mode:
    filtered_df = filtered_df[filtered_df["Carbohydrates (g)"] <= 10]

# ---------------------------
# MEAL BUILDER
# ---------------------------
def build_meal(df, target_cals, meal_type):
    meal_df = df[df["Meal_Type"] == meal_type]

    meal_df = meal_df.sort_values(by="Protein (g)", ascending=False)

    selected = []
    total = 0

    for _, row in meal_df.iterrows():
        if len(selected) >= 3:
            break

        if total + row["Calories (kcal)"] <= target_cals:
            selected.append(row)
            total += row["Calories (kcal)"]

    return pd.DataFrame(selected), total

# ---------------------------
# TOTAL ROW FUNCTION
# ---------------------------
def add_totals_row(df):
    if df.empty:
        return df

    totals = {
        "Food_Item": "TOTAL",
        "Calories (kcal)": df["Calories (kcal)"].sum(),
        "Protein (g)": df["Protein (g)"].sum(),
        "Carbohydrates (g)": df["Carbohydrates (g)"].sum(),
        "Fat (g)": df["Fat (g)"].sum()
    }

    return pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

# ---------------------------
# MEAL SPLIT
# ---------------------------
meal_targets = {
    "Breakfast": target_calories * 0.3,
    "Lunch": target_calories * 0.4,
    "Dinner": target_calories * 0.3
}

# ---------------------------
# DISPLAY
# ---------------------------
st.subheader("Meal Recommendations")

total_day = 0

for meal, cal_target in meal_targets.items():
    items, meal_total = build_meal(filtered_df, cal_target, meal)

    st.markdown(f"### {meal} ({cal_target:.0f} kcal target)")

    if items.empty:
        st.warning("No foods match your filters")
    else:
        display_df = items[[
            "Food_Item",
            "Calories (kcal)",
            "Protein (g)",
            "Carbohydrates (g)",
            "Fat (g)"
        ]]

        display_df = add_totals_row(display_df)

        st.dataframe(display_df, use_container_width=True)

    total_day += meal_total

st.write(f"## Estimated Daily Total: {total_day:.0f} kcal")

# ---------------------------
# WEIGHT PROJECTION
# ---------------------------
def weight_projection(weight, target_calories, tdee, weeks=12):
    weights = []
    current_weight = weight

    daily_diff = target_calories - tdee

    for _ in range(weeks):
        weekly_change = (daily_diff * 7) / 7700
        current_weight += weekly_change
        weights.append(current_weight)

    return list(range(1, weeks + 1)), weights

st.subheader("Weight Projection")

weeks, weights = weight_projection(weight, target_calories, tdee)

fig, ax = plt.subplots()
ax.plot(weeks, weights)
ax.set_xlabel("Weeks")
ax.set_ylabel("Weight (kg)")
ax.set_title("12-week prediction")

st.pyplot(fig)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.write("Estimates only. Not medical advice.")