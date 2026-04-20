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

    if not data or "symptom" not in data:
        return jsonify({"error": "No
