from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json


app = FastAPI()

class Patient(BaseModel):
    
    id: Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name:Annotated[str,Field(...,description='Name of the patient')]
    city:Annotated[str,Field(...,description='City where patient living')]
    age:Annotated[int,Field(...,description='age of the patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='gender of the patient')]
    height:Annotated[float,Field(..., gt=0, description='Height of the patient in mtrs')]
    weight:Annotated[float,Field(...,gt=0 ,description='Weight of the pationt in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'UnderWeight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):

    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age:Annotated[Optional[int],Field(default=None,gt=0)]
    gender:Annotated[Optional[Literal['male','female']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight:Annotated[Optional[float],Field(Field(default=None,gt=0))]


def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "A fully functional FastAPI to manage your patient records."}

@app.get("/time")
def time():
    from datetime import datetime
    return {"current_time": datetime.now().isoformat()}


@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str):

    data = load_data()

    if patient_id in data:
        return data[patient_id]
    return {"error": "Patient not found"}

@app.post('/create')
def create_patient(patient:Patient):
    
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists')
    
    data[patient.id] = patient.model_dump(exclude=['id'])

    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update: PatientUpdate):
    
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset= True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})