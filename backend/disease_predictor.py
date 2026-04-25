class DiseasePredictor:

    def __init__(self):

        # simple rule-based prediction
        self.rules = {
            "fever": "Viral Infection",
            "cough": "Common Cold",
            "headache": "Migraine",
            "chest pain": "Cardiac Risk",
            "stomach pain": "Gastritis",
            "skin rash": "Allergy",
            "vomiting": "Food Poisoning"
        }

    def predict(self, symptom):

        symptom = symptom.lower()

        if symptom in self.rules:
            return self.rules[symptom]

        return "General Infection"
