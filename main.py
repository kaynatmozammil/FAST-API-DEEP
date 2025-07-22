from fastapi import FastAPI ,Path ,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field , computed_field
from typing import Annotated , Literal
import json
app = FastAPI()


class Patient(BaseModel):
    
    id:Annotated[str, Field(..., description='ID of patient',examples=['P001'])]
    name : Annotated[str,Field(...,description='Name of the patient' )]
    city : Annotated[str,Field(..., description='City where the patient is living ')]
    age : Annotated[int, Field(..., gt=0 , lt = 120 , description='Age of the patient')]
    gender : Annotated[Literal['male', 'female','others'],Field(..., description='Gender of the pateint')]
    height : Annotated[float, Field(..., gt=0 , description='Height of patient in mtrs')]
    weight : Annotated[float, Field(..., gt=0 , description='Weight of patient in kgs')]

    @computed_field
    @property
    def bmi(self) ->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi 
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi <25 :
            return 'Normal'
        elif self.bmi <30 :
            return 'Normal'
        else:
            return 'Obese'

def load_date():
    with open('patients.json','r') as file:
        data = json.load(file)

    return data

def save_data(data):
    with open('patients.json','w') as file:
        json.dump(data,file)
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

@app.post('/create')
def create_patient(patient:Patient):

    # load existing data
    data = load_date()
    # check if the patient already exist

    if(patient.id in data):
        raise HTTPException(status_code=400 , detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    # create success

    return JSONResponse(status_code=201 , content={'message':'patient created successfully'})
























# from fastapi import FastAPI ,Path ,HTTPException,Query
# import json
# app = FastAPI()

# def load_date():
#     with open('patients.json','r') as file:
#         data = json.load(file)

#     return data
# @app.get("/")
# def hello():
#     return {"message": "Patient Management System API"}

# @app.get("/about")
# def about():
#     return {"message": "This is a Patient Management System API. "
#     "It allows you to manage patient records, appointments, and medical history.    "}

# @app.get("/view")
# def view():
#     data = load_date()

#     return data

# @app.get("/patient/{patient_id}")
# def view_patient(patient_id:str = Path(...,description="ID of the patient in the DB ",example="P001")):
#     # load all the patient
#     data = load_date()

#     if patient_id in data:
#         return data[patient_id]
#     raise HTTPException (status_code=404,detail='Patient not found')

# @app.get("/sort")
# def sort_patient(sort_by:str = Query(..., description= "Sort on the basis of Height Weight or BMI "),order_by:str = Query('asc' , description="Sort in ASC or DESC order ") ):
#     valid_fields = ['height','weight', 'bmi']

#     if sort_by not in valid_fields:
#         raise HTTPException(status_code=400 , detail=f'Invalid field select from {valid_fields}')
#     if order_by not in ['asc','desc']:
#         raise HTTPException(status_code=400, detail='Invalid order select between asc or desc ')
    
#     data=load_date()

#     sort_order = True if order_by =='desc' else False
#     sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by, 0 ),reverse=sort_order)

#     return sorted_data
