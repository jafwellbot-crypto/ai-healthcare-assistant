import csv

class MedicineFilter:

    def __init__(self):
        self.medicine_data = []
        self.load_data()

    def load_data(self):
        with open("data/medicines.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.medicine_data.append(row)

    def recommend_medicine(self, symptom):
        medicines = []

        for entry in self.medicine_data:
            if symptom.lower() in entry["used_for"].lower():
                medicines.append(entry)

        return medicines
