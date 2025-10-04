import json

from fastapi import FastAPI, Path, HTTPException


app = FastAPI()

# Open Json file
def load_data():
    with open("patient.json", "r") as f:
        data = json.load(f)
    return data

@app.get("/")
def home():
    return {"message": "Patient Management System API."}

@app.get("/about")
def about():
    return {"message": "A Fully functional API to manage your patient records."}

@app.get("/view")
def patient_list():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient_details(patient_id: str = Path(..., description="Id of the patient in the DB", example="P001")):
    # Load all patient data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient Not Found")