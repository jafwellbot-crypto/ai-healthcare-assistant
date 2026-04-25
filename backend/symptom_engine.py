import csv
import os


class SymptomEngine:

    def __init__(self):
        self.symptom_data = []
        self.load_data()

    def load_data(self):

        BASE_DIR = os.path.dirname(__file__)
        data_path = os.path.join(BASE_DIR, "data", "symptoms.csv")

        with open(data_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.symptom_data.append(row)

    def analyze_symptom(self, symptom):

        results = []

        for entry in self.symptom_data:

            if symptom.lower() == entry["symptom"].lower():

                results.append({
                    "condition": entry["possible_condition"],
                    "severity": entry["severity"]
                })

        return results
