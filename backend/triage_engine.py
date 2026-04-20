class TriageEngine:

    def calculate_score(self, symptom, duration_days, temperature, pain_level, vomiting_count, age):

        score = 0

        # Fever logic
        if symptom == "fever":
            if temperature >= 103:
                score += 40
            elif temperature >= 101:
                score += 25
            else:
                score += 10

        # Vomiting logic
        if symptom == "vomiting":
            if vomiting_count >= 6:
                score += 35
            elif vomiting_count >= 3:
                score += 20
            else:
                score += 10

        # Pain logic
        if pain_level >= 8:
            score += 30
        elif pain_level >= 5:
            score += 20
        else:
            score += 10

        # Duration logic
        if duration_days >= 5:
            score += 25
        elif duration_days >= 2:
            score += 15

        # Age risk factor
        if age >= 60:
            score += 20
        elif age <= 10:
            score += 15

        return min(score, 100)


    def classify_severity(self, score):

        if score <= 30:
            return "low"

        elif score <= 60:
            return "medium"

        else:
            return "high"
