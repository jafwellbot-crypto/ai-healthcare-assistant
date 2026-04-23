import pandas as pd

# -----------------------------
# LOAD MEDICINE DATA
# -----------------------------
def load_medicines():
    try:
        medicines = pd.read_csv("data/medicines.csv")
        return medicines
    except Exception as e:
        print("Error loading medicines:", e)
        return pd.DataFrame()

# -----------------------------
# LOAD DOCTOR DATA
# -----------------------------
def load_doctors():
    try:
        doctors = pd.read_csv("data/doctors_raipur.csv")
        return doctors
    except Exception as e:
        print("Error loading doctors:", e)
        return pd.DataFrame()

# -----------------------------
# LOAD SYMPTOMS DATA
# -----------------------------
def load_symptoms():
    try:
        symptoms = pd.read_csv("data/symptoms.csv")
        return symptoms
    except Exception as e:
        print("Error loading symptoms:", e)
        return pd.DataFrame()

# -----------------------------
# LOAD PATIENT PROFILES
# -----------------------------
def load_patients():
    try:
        patients = pd.read_csv("data/patients.csv")
        return patients
    except Exception as e:
        print("Error loading patients:", e)
        return pd.DataFrame()

# -----------------------------
# GET SPECIFIC PATIENT PROFILE
# -----------------------------
def get_patient_profile(name):

    try:
        patients = load_patients()

        patient = patients[patients["name"].str.lower() == name.lower()]

        if patient.empty:
            return None

        return patient.iloc[0].to_dict()

    except Exception as e:
        print("Error fetching patient:", e)
        return None
