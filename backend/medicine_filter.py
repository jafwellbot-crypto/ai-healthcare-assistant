import pandas as pd
from database import load_medicines


class MedicineFilter:

    def __init__(self):
        self.medicines = load_medicines()

    def get_medicines(self, symptom, patient_profile=None):

        try:
            filtered = self.medicines[
                self.medicines["used_for"].str.lower() == symptom.lower()
            ]

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

            return medicines_list

        except Exception as e:
            print("Medicine filter error:", e)
            return []
