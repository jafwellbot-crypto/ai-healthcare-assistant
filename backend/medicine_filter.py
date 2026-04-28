import pandas as pd
from database import load_medicines


class MedicineFilter:

    def __init__(self):
        # Load medicines from CSV
        self.medicines = load_medicines()

        # DEBUG: Check if medicines are loaded
        print("\n----- MEDICINE DATA LOADED -----")
        print(self.medicines)
        print("--------------------------------\n")


    def get_medicines(self, symptom, patient_profile=None):

        try:
            print("Symptom received:", symptom)

            # Filter medicines based on symptom
            filtered = self.medicines[
                self.medicines["used_for"].str.lower().str.contains(symptom.lower())
            ]

            # DEBUG: Show filtered medicines
            print("\nFiltered Medicines:")
            print(filtered)
            print("-------------------\n")

            # ----------------------------
            # ALLERGY FILTER
            # ----------------------------
            if patient_profile:

                allergies = str(patient_profile.get("allergies", "")).lower()

                if allergies != "none":

                    filtered = filtered[
                        ~filtered["medicine"].str.lower().str.contains(allergies)
                    ]

            medicines_list = []

            for _, row in filtered.iterrows():
                medicines_list.append({
                    "medicine": row["medicine"],
                    "used_for": row["used_for"],
                    "avoid_for": row["avoid_for"]
                })

            print("Medicines returned to API:", medicines_list)

            return medicines_list

        except Exception as e:
            print("Medicine filter error:", e)
            return [{"medicine": "Paracetamol"}, {"medicine": "Ibuprofen"}]


