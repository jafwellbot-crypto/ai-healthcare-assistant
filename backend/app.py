from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.symptom_engine import SymptomEngine
from backend.medicine_filter import MedicineFilter
from backend.doctor_locator import DoctorLocator
from backend.triage_engine import TriageEngine

app = Flask(__name__)
CORS(app)

# Initialize modules
symptom_engine = SymptomEngine()
medicine_filter = MedicineFilter()
doctor_locator = DoctorLocator()
triage_engine = TriageEngine()


# Health check route
@app.route("/", methods=["GET"])
def home():
    return "AI Healthcare Assistant API Running"


# Quick browser test route
@app.route("/quick-test/<symptom>", methods=["GET"])
def quick_test(symptom):

    score = triage_engine.calculate_score(
        symptom,
        duration_days=2,
        temperature=101,
        pain_level=4,
        vomiting_count=0,
        age=25
    )

    severity = triage_engine.classify_severity(score)

    if severity == "high":
        doctors = doctor_locator.get_doctors()

        return jsonify({
            "symptom": symptom,
            "triage_score": score,
            "severity": severity,
            "recommendation": "Consult a doctor",
            "doctors": doctors
        })

    else:
        medicines = medicine_filter.recommend_medicine(symptom)

        return jsonify({
            "symptom": symptom,
            "triage_score": score,
            "severity": severity,
            "recommendation": "Medicine recommended",
            "medicines": medicines
        })


# Main AI analysis endpoint
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    symptom = data.get("symptom")

    if not symptom:
        return jsonify({"error": "Symptom required"}), 400

    duration_days = data.get("duration_days", 1)
    temperature = data.get("temperature", 98)
    pain_level = data.get("pain_level", 3)
    vomiting_count = data.get("vomiting_count", 0)
    age = data.get("age", 30)

    score = triage_engine.calculate_score(
        symptom,
        duration_days,
        temperature,
        pain_level,
        vomiting_count,
        age
    )

    severity = triage_engine.classify_severity(score)

    if severity == "high":
        doctors = doctor_locator.get_doctors()

        return jsonify({
            "symptom": symptom,
            "triage_score": score,
            "severity": severity,
            "recommendation": "Consult a doctor immediately",
            "doctors": doctors
        })

    else:
        medicines = medicine_filter.recommend_medicine(symptom)

        return jsonify({
            "symptom": symptom,
            "triage_score": score,
            "severity": severity,
            "recommendation": "Medicine recommended",
            "medicines": medicines
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
