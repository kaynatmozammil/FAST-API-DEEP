from fastapi import FastAPI ,Path ,HTTPException,Query
import json
app = FastAPI()

def load_date():
    with open('patients.json','r') as file:
        data = json.load(file)

    return data
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "This is a Patient Management System API. "
    "It allows you to manage patient records, appointments, and medical history.    "}

@app.get("/view")
def view():
    data = load_date()

    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id:str = Path(...,description="ID of the patient in the DB ",example="P001")):
    # load all the patient
    data = load_date()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException (status_code=404,detail='Patient not found')

@app.get("/sort")
def sort_patient(sort_by:str = Query(..., description= "Sort on the basis of Height Weight or BMI "),order_by:str = Query('asc' , description="Sort in ASC or DESC order ") ):
    valid_fields = ['height','weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 , detail=f'Invalid field select from {valid_fields}')
    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc or desc ')
    
    data=load_date()

    sort_order = True if order_by =='desc' else False
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0 ),reverse=sort_order)

    return sorted_data
