
from flask import Flask, render_template, request # type: ignore
import joblib
import numpy as np

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# ✅ Load the CORRECT model file
model = joblib.load("Renewable_Energy_Adoption_model.pkl")

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/", methods=["GET"])
def home():
    return {
        "message": "Renewable Adoption Predictor API is running",
        "usage": "Send a POST request to /predict with JSON data"
    }

@app.route("/predict", methods=["POST"])
def predict():
    try:
        c = request.form.get("carbon_emissions", "")
        e = request.form.get("energy_output", "")
        r = request.form.get("renewability_index", "")
        ce = request.form.get("cost_efficiency", "")

        if c == "" or e == "" or r == "" or ce == "":
            return render_template("index.html",
                                   result="⚠️ Please fill all fields before predicting.")

        carbon_emissions = float(c)
        energy_output = float(e)
        renewability_index = float(r)
        cost_efficiency = float(ce)

        input_features = np.array([[
            carbon_emissions,
            energy_output,
            renewability_index,
            cost_efficiency
        ]])

        prediction = model.predict(input_features)[0]
        proba = model.predict_proba(input_features)[0][1] * 100

        output = "HIGH Adoption ✅" if prediction == 1 else "LOW Adoption ❌"

        return render_template(
            "index.html",
            result=output,
            confidence=f"{proba:.2f}%",
            carbon_emissions=carbon_emissions,
            energy_output=energy_output,
            renewability_index=renewability_index,
            cost_efficiency=cost_efficiency,
        )

    except Exception as e:
        return render_template("index.html", result=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False) 