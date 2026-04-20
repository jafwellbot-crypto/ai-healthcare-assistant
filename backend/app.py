from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.symptom_engine import SymptomEngine
from backend.medicine_filter import MedicineFilter
from backend.doctor_locator import DoctorLocator
from backend.triage_engine import TriageEngine

app = Flask(__name__)
CORS(app)

# Initialize engines
symptom_engine = SymptomEngine()
medicine_filter = MedicineFilter()
doctor_locator = DoctorLocator()
triage_engine = TriageEngine()


# Home route
@app.route("/")
def home():
    return "AI Healthcare Assistant API Running"


# Analyze symptom
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    symptom = data.get("symptom")

    if not symptom:
        return jsonify({"error": "No symptom provided"}), 400

    # Optional medical parameters
    duration_days = data.get("duration_days", 1)
    temperature = data.get("temperature", 98)
    pain_level = data.get("pain_level", 3)
    vomiting_count = data.get("vomiting_count", 0)
    age = data.get("age", 30)

    # Calculate triage score
    score = triage_engine.calculate_score(
        symptom,
        duration_days,
        temperature,
        pain_level,
        vomiting_count,
        age
    )

    severity = triage_engine.classify_severity(score)

    # Determine recommendation
    recommendation = {}

    if severity == "low":

        recommendation["advice"] = "Mild condition. Rest and monitor symptoms."
        recommendation["medicines"] = medicine_filter.recommend_medicine(symptom)

    elif severity == "medium":

        recommendation["advice"] = "Moderate condition. Medicines recommended."
        recommendation["medicines"] = medicine_filter.recommend_medicine(symptom)

    else:

        recommendation["advice"] = "Severe symptoms detected. Please consult a doctor."
        recommendation["doctors"] = doctor_locator.get_doctors()

    return jsonify({
        "symptom": symptom,
        "triage_score": score,
        "severity": severity,
        "recommendation": recommendation
    })


# Run server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
