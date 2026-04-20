from flask import Flask, request, jsonify
from flask_cors import CORS

from symptom_engine import SymptomEngine
from medicine_filter import MedicineFilter
from doctor_locator import DoctorLocator

app = Flask(__name__)
CORS(app)

# Initialize modules
symptom_engine = SymptomEngine()
medicine_filter = MedicineFilter()
doctor_locator = DoctorLocator()


# Home route
@app.route("/")
def home():
    return "AI Healthcare Assistant API Running"


# Analyze symptom route
@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    # Safety check
    if not data or "symptom" not in data:
        return jsonify({"error": "No symptom provided"}), 400

    symptom = data["symptom"]

    results = symptom_engine.analyze_symptom(symptom)

    # If symptom not found
    if not results:
        return jsonify({
            "message": "Sorry, we are currently not working on this symptom yet."
        })

    response = []

    for result in results:

        entry = {
            "condition": result["condition"],
            "severity": result["severity"]
        }

        # For mild/medium → suggest medicines
        if result["severity"] in ["low", "medium"]:
            entry["medicines"] = medicine_filter.recommend_medicine(symptom)

        # For high → suggest doctors
        if result["severity"] == "high":
            entry["doctors"] = doctor_locator.get_doctors()

        response.append(entry)

    return jsonify(response)


# Run server (IMPORTANT for Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
