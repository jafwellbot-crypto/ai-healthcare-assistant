from flask import Flask, request, jsonify
from flask_cors import CORS

from symptom_engine import SymptomEngine
from triage_engine import TriageEngine
from medicine_filter import MedicineFilter
from doctor_locator import DoctorLocator
from database import get_patient_profile
from disease_predictor import DiseasePredictor

app = Flask(__name__)
CORS(app)

# Initialize engines
symptom_engine = SymptomEngine()
triage_engine = TriageEngine()
medicine_filter = MedicineFilter()
doctor_locator = DoctorLocator()
disease_predictor = DiseasePredictor()


@app.route("/")
def home():
    return jsonify({
        "message": "AI Healthcare Assistant API is running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "running",
        "service": "AI Healthcare Assistant"
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.json

        # -----------------------
        # USER INPUT
        # -----------------------

        patient_name = data.get("name", "")
        symptom = data.get("symptom", "").lower()
        temperature = data.get("temperature", 98)
        duration_days = data.get("duration_days", 1)
        pain_level = data.get("pain_level", 1)
        vomiting_count = data.get("vomiting_count", 0)

        # -----------------------
        # LOAD PATIENT PROFILE
        # -----------------------

        patient_profile = get_patient_profile(patient_name)

        # -----------------------
        # DISEASE PREDICTION
        # -----------------------

        predicted_disease = disease_predictor.predict(symptom)

        # -----------------------
        # TRIAGE SCORING
        # -----------------------

        triage_score = triage_engine.calculate_score(
            symptom,
            temperature,
            duration_days,
            pain_level,
            vomiting_count
        )

        severity = triage_engine.get_severity(triage_score)

        # -----------------------
        # MEDICINE FILTER
        # -----------------------

        medicines = medicine_filter.get_medicines(
            symptom,
            patient_profile
        )

        # -----------------------
        # DOCTOR RECOMMENDATION
        # -----------------------

        doctors = []

        if severity in ["high", "emergency"]:
            doctors = doctor_locator.find_doctors(symptom)

        # -----------------------
        # RESPONSE
        # -----------------------

        response = {
            "patient_profile": patient_profile,
            "symptom": symptom,
            "predicted_disease": predicted_disease,
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
