import csv
import os


class DoctorLocator:

    def __init__(self):
        self.doctors = []
        self.load_data()

    def load_data(self):

        # Get backend folder path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        # Path to backend/data/doctors_raipur.csv
        data_path = os.path.join(BASE_DIR, "data", "doctors_raipur.csv")

        if not os.path.exists(data_path):
            raise Exception(f"doctors_raipur.csv not found at {data_path}")

        with open(data_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.doctors.append(row)

    def find_doctors(self, symptom):

        results = []

        for doctor in self.doctors:

            if symptom.lower() in doctor["specialization"].lower():

                results.append({
                    "name": doctor["name"],
                    "hospital": doctor["hospital"],
                    "specialization": doctor["specialization"]
                })

        return results
