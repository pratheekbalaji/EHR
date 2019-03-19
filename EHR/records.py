from database import Database
data = Database()
def patient_details(name):
    patient = data.patient_details(name)
    patient = patient[0]
    return patient

def vitals(name):
    vitals = data.observations(name)
    return vitals

def medications(name):

    medication = data.medications(name)
    return medication

def conditions(name):
    condition = data.conditions(name)
    return condition

def allergies(name):
    allergy = data.allergies(name)
    return allergy

def  procedures(name):
    procedure = data.procedures(name)
    return procedure

