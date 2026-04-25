class TriageEngine:

    def calculate_score(self, symptom, temperature, duration_days, pain_level, vomiting_count):

        score = 0

        # Fever based scoring
        if temperature >= 103:
            score += 40
        elif temperature >= 101:
            score += 25
        else:
            score += 10

        # Duration
        if duration_days >= 5:
            score += 20
        elif duration_days >= 3:
            score += 10

        # Pain level
        score += pain_level * 5

        # Vomiting
        score += vomiting_count * 5

        return score


    def get_severity(self, score):

        if score >= 70:
            return "emergency"

        elif score >= 40:
            return "high"

        elif score >= 20:
            return "medium"

        else:
            return "low"
