from flask import Flask, request, jsonify
from flask_cors import CORS
from database import get_patient_profile
import pandas as pd


app = Flask(__name__)
CORS(app)

# Load medicine dataset
try:
    medicine_data = pd.read_csv("data/medicines.csv")
except:
    medicine_data = pd.DataFrame([
        {"medicine": "Paracetamol", "used_for": "fever", "avoid_for": "none"},
        {"medicine": "Cetirizine", "used_for": "allergy", "avoid_for": "none"},
        {"medicine": "ORS", "used_for": "vomiting", "avoid_for": "none"},
        {"medicine": "Ibuprofen", "used_for": "pain", "avoid_for": "pregnancy"}
    ])

# -----------------------------
# ROOT ROUTE
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "AI Healthcare Assistant API is running"
    })

# -----------------------------
# HEALTH CHECK ROUTE
# -----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "service": "AI Healthcare Assistant",
        "version": "1.0"
    })

# -----------------------------
# TRIAGE SCORING FUNCTION
# -----------------------------
def calculate_triage_score(data):

    score = 0

    temperature = data.get("temperature", 98)
    duration = data.get("duration_days", 0)
    pain = data.get("pain_level", 0)
    vomiting = data.get("vomiting_count", 0)

    if temperature >= 101:
        score += 20

    if duration >= 3:
        score += 20

    if pain >= 5:
        score += 20

    if vomiting >= 3:
        score += 20

    return score

# -----------------------------
# ANALYZE SYMPTOMS
# -----------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json

    symptom = data.get("symptom", "").lower()

    triage_score = calculate_triage_score(data)

    if triage_score >= 60:
        severity = "high"
        recommendation = "Consult a doctor immediately"
        medicines = []
    elif triage_score >= 30:
        severity = "medium"
        recommendation = "Medicine recommended"
        medicines = medicine_data[medicine_data["used_for"] == symptom].to_dict(orient="records")
    else:
        severity = "low"
        recommendation = "Rest and basic medication"
        medicines = medicine_data[medicine_data["used_for"] == symptom].to_dict(orient="records")

    response = {
        "symptom": symptom,
        "triage_score": triage_score,
        "severity": severity,
        "recommendation": recommendation,
        "medicines": medicines
    }

    return jsonify(response)

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
