import streamlit as st
import pandas as pd
import joblib

# Load model and feature order
model = joblib.load("car_price_model.pkl")
features = joblib.load("features.pkl")

# Title
st.title("🚗 Car Price Prediction App")

st.write("Enter car details below:")

# -----------------------
# INPUTS
# -----------------------

car_age = st.number_input("Car Age (years)", min_value=1, max_value=20, value=5)
km_driven = st.number_input("KM Driven", min_value=0, max_value=200000, value=50000)

engine_cc = st.number_input("Engine CC", min_value=800, max_value=3000, value=1500)
mileage = st.number_input("Mileage (kmpl)", min_value=10.0, max_value=30.0, value=18.0)

# Owner (already binary feature)
owner = st.selectbox("Owner Type", ["First", "Second"])

# Fuel type
fuel = st.selectbox("Fuel Type", ["Diesel", "Petrol", "Electric"])

# Transmission
trans = st.selectbox("Transmission", ["Automatic", "Manual"])

# -----------------------
# FEATURE ENGINEERING
# -----------------------

km_per_year = km_driven / car_age if car_age > 0 else 0

# Encoding
owner_Second = 1 if owner == "Second" else 0

fuel_type_Electric = 1 if fuel == "Electric" else 0
fuel_type_Petrol = 1 if fuel == "Petrol" else 0
# Diesel = 0,0

transmission_Manual = 1 if trans == "Manual" else 0
# Automatic = 0

# -----------------------
# PREDICTION
# -----------------------

if st.button("Predict Price"):

    input_data = pd.DataFrame({
        'car_age': [car_age],
        'km_driven': [km_driven],
        'owner_Second': [owner_Second],
        'engine_cc': [engine_cc],
        'mileage_kmpl': [mileage],
        'km_per_year': [km_per_year],
        'fuel_type_Electric': [fuel_type_Electric],
        'fuel_type_Petrol': [fuel_type_Petrol],
        'transmission_Manual': [transmission_Manual]
    })

    # Ensure correct feature order
    input_data = input_data[features]

    # Prediction
    prediction = model.predict(input_data)

    st.success(f"💰 Predicted Car Price: ₹{prediction[0]:,.2f}")