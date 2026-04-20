import csv

class DoctorLocator:

    def __init__(self):
        self.doctors = []
        self.load_data()

    def load_data(self):
        with open("data/doctors_raipur.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.doctors.append(row)

    def get_doctors(self):
        return self.doctors
