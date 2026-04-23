from flask import Flask, request, jsonify
from flask_cors import CORS

from symptom_engine import SymptomEngine
from triage_engine import TriageEngine
from medicine_filter import MedicineFilter
from doctor_locator import DoctorLocator
from database import get_patient_profile

app = Flask(__name__)
CORS(app)

symptom_engine = SymptomEngine()
triage_engine = TriageEngine()
medicine_filter = MedicineFilter()
doctor_locator = DoctorLocator()


@app.route("/")
def home():
    return jsonify({
        "message": "AI Healthcare Assistant API is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "service": "AI Healthcare Assistant",
        "version": "1.1"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.json

        symptom = data.get("symptom", "").lower()
        temperature = data.get("temperature", 98)
        duration_days = data.get("duration_days", 1)
        pain_level = data.get("pain_level", 1)
        vomiting_count = data.get("vomiting_count", 0)
        age = data.get("age", 25)

        patient_name = data.get("name", "")

        # -------------------------
        # GET PATIENT PROFILE
        # -------------------------
        patient_profile = get_patient_profile(patient_name)

        # -------------------------
        # TRIAGE SCORING
        # -------------------------
        triage_score = triage_engine.calculate_score(
            symptom,
            temperature,
            duration_days,
            pain_level,
            vomiting_count
        )

        severity = triage_engine.get_severity(triage_score)

        # -------------------------
        # MEDICINE RECOMMENDATION
        # -------------------------
        medicines = medicine_filter.get_medicines(symptom)

        # -------------------------
        # DOCTOR SUGGESTION
        # -------------------------
        doctors = []
        if severity == "high":
            doctors = doctor_locator.find_doctors(symptom)

        response = {
            "patient_profile": patient_profile,
            "symptom": symptom,
            "triage_score": triage_score,
            "severity": severity,
            "recommendation": "Medicine recommended",
            "medicines": medicines,
            "recommended_doctors": doctors
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
