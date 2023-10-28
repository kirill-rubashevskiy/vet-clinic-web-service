import random
import uvicorn
from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException


description = """
The FastAPI web service for a vet clinic, developed as a DevOps course assignment during study at 
[HSE University Master’s Programme Machine Learning and Data-Intensive Systems](https://www.hse.ru/en/ma/mlds/).

## Dogs

You can search for all dogs or dogs of certain kind or pk, update information about dogs and add new dogs.

## Timestamps

You can add new timestamps.
"""


tags_metadata = [
    {
        "name": "dogs",
        "description": "Operations with dogs.",
    },
    {
        "name": "timestamps",
        "description": "Operations with timestamps.",
    },
]


app = FastAPI(
    title="VetClinicApp🐕🏥",
    description=description,
    version='1.0',
    openapi_tags=tags_metadata,
    contact={
        "name": "Kirill Rubashevskiy",
        "url": "https://github.com/kirill-rubashevskiy",
        "email": "kirill.rubashevskiy@gmail.com"
    }
)


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk:   int
    kind: DogType


class Timestamp(BaseModel):
    id:        int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get("/")
async def root():
    patient = random.choice(list(dogs_db.values()))
    return {"message": f"Welcome to the Vet Clinic Web Service. Patient of the day is {patient.kind} {patient.name}"}


@app.post("/post",
          response_model=Timestamp,
          summary="Get Post",
          tags=["timestamps"])
async def get_post(timestamp: Timestamp):
    if timestamp.id in [existing_timestamp.id for existing_timestamp in post_db]:
        raise HTTPException(status_code=409, detail="this id already exists")
    post_db.append(timestamp)
    return timestamp


@app.get("/dog",
         response_model=list[Dog],
         summary="Get Dogs",
         tags=["dogs"])
async def get_dogs(kind: DogType = None):
    if kind:
        res = [dog for dog in dogs_db.values() if dog.kind == kind]
    else:
        res = [dog for dog in dogs_db.values()]

    return res


@app.post("/dog",
          response_model=Dog,
          summary="Create Dog",
          tags=["dogs"])
async def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=409, detail="this pk already exists")
    dogs_db[dog.pk] = dog
    return dog


@app.get("/dog/{pk}",
         response_model=Dog,
         summary="Get Dog By PK",
         tags=["dogs"])
async def get_dog_by_pk(pk: int):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="this pk not found")
    return dogs_db[pk]


@app.patch("/dog/{pk}",
           response_model=Dog,
           summary="Update Dog",
           tags=["dogs"])
async def update_dog(pk: int, dog: Dog):
    if pk not in dogs_db:
        raise HTTPException(status_code=404, detail="this pk not found")
    dogs_db[pk] = dog
    return dog


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
