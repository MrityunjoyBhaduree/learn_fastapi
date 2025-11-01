import json

from fastapi import FastAPI, Path, HTTPException, Query


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

@app.get("/sort")
def sort_patients(sort_by: str = Query(
    ..., description="Sort on the basis of height, weight or bmi"),
    order: str = Query("", description="Sort in asc or desc order")):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field select from{valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order select between 'asc', 'desc'")
    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_order = sorted(data.values(), key=lambda x:x.get(sort_by, 0),
                          reverse=sort_order)
    return sorted_order