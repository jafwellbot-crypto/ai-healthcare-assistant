from symptom_engine import SymptomEngine
from medicine_filter import MedicineFilter
from doctor_locator import DoctorLocator

def main():

    symptom_engine = SymptomEngine()
    medicine_filter = MedicineFilter()
    doctor_locator = DoctorLocator()

    print("AI Healthcare Assistant")
    print("------------------------")

    symptom = input("Enter your symptom: ")

    results = symptom_engine.analyze_symptom(symptom)

    if not results:
        print("Sorry, we are currently not working on this symptom yet.")
        return

    for result in results:

        print("\nPossible Condition:", result["condition"])
        print("Severity Level:", result["severity"])

        if result["severity"] == "low" or result["severity"] == "medium":

            medicines = medicine_filter.recommend_medicine(symptom)

            if medicines:
                print("\nSuggested Medicines:")

                for med in medicines:
                    print("-", med["medicine"], "(Avoid for:", med["avoid_for"], ")")

        if result["severity"] == "high":

            print("\nThis may require doctor consultation.")
            print("\nDoctors you can consult:")

            doctors = doctor_locator.get_doctors()

            for doc in doctors:
                print(
                    doc["name"],
                    "-",
                    doc["specialization"],
                    "(",
                    doc["hospital"],
                    ")"
                )

if __name__ == "__main__":
    main()
