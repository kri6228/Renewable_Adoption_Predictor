import streamlit as st
import joblib
import numpy as np

# Load your trained model
model = joblib.load("Renewable_Energy_Adoption_model.pkl")

st.set_page_config(page_title="Renewable Adoption Predictor", layout="centered")

st.title("🌱 Renewable Energy Adoption Predictor")
st.write("Predict whether renewable energy adoption will be **HIGH or LOW** based on key factors.")

# Input fields
carbon_emissions = st.number_input("Carbon Emissions", min_value=0.0, step=1.0)
energy_output = st.number_input("Energy Output", min_value=0.0, step=1.0)
renewability_index = st.number_input("Renewability Index", min_value=0.0, max_value=1.0, step=0.01)
cost_efficiency = st.number_input("Cost Efficiency", min_value=0.0, max_value=1.0, step=0.01)

if st.button("Predict Adoption"):
    input_features = np.array([[
        carbon_emissions,
        energy_output,
        renewability_index,
        cost_efficiency
    ]])

    prediction = model.predict(input_features)[0]
    confidence = model.predict_proba(input_features)[0][1] * 100

    if prediction == 1:
        st.success(f"✅ HIGH Adoption (Confidence: {confidence:.2f}%)")
    else:
        st.error(f"❌ LOW Adoption (Confidence: {confidence:.2f}%)")

    st.subheader("🔎 Input Values Used")
    st.write(f"Carbon Emissions: {carbon_emissions}")
    st.write(f"Energy Output: {energy_output}")
    st.write(f"Renewability Index: {renewability_index}")
    st.write(f"Cost Efficiency: {cost_efficiency}")
