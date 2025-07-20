from fastapi import FastAPI
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