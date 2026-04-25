import csv
import os


class SymptomEngine:

    def __init__(self):
        self.symptom_data = []
        self.load_data()

    def load_data(self):

        # absolute path to backend folder
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # path to backend/data/symptoms.csv
        data_path = os.path.join(BASE_DIR, "data", "symptoms.csv")

        if not os.path.exists(data_path):
            raise Exception(f"symptoms.csv not found at {data_path}")

        with open(data_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.symptom_data.append(row)

    def analyze_symptom(self, symptom):

        results = []

        for entry in self.symptom_data:
            if symptom.lower() == entry["symptom"].lower():
                results.append({
                    "condition": entry.get("possible_condition", ""),
                    "severity": entry.get("severity", "")
                })

        return results
