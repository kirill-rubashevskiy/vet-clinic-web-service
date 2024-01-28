import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import schemas
import crud

from database import get_db


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


@app.get("/")
def root():
    return {"message": f"Welcome to the Vet Clinic Web Service"}


@app.post("/post",
          response_model=schemas.Timestamp,
          summary="Get Post",
          tags=["timestamps"])
def get_post(timestamp: schemas.Timestamp, db: Session = Depends(get_db)):
    db_timestamp = crud.get_timestamp(db=db, timestamp_id=timestamp.id)
    if db_timestamp is not None:
        raise HTTPException(status_code=409, detail="Timestamp with this id already exists")
    return crud.create_timestamp(db=db, timestamp=timestamp)


@app.get("/dog",
         response_model=list[schemas.Dog],
         summary="Get Dogs",
         tags=["dogs"])
def get_dogs(kind: schemas.DogType = None, db: Session = Depends(get_db)):
    dogs = crud.get_dogs(db=db, kind=kind)
    return dogs


@app.post("/dog",
          response_model=schemas.Dog,
          summary="Create Dog",
          tags=["dogs"])
def create_dog(dog: schemas.Dog, db: Session = Depends(get_db)):
    db_dog = crud.get_dog(db=db, dog_pk=dog.pk)
    if db_dog is not None:
        raise HTTPException(status_code=409, detail=f"Dog with pk {str(dog.pk)} already exists")
    return crud.create_dog(db=db, dog=dog)


@app.get("/dog/{pk}",
         response_model=schemas.Dog,
         summary="Get Dog By PK",
         tags=["dogs"])
def get_dog_by_pk(pk: int, db: Session = Depends(get_db)):
    db_dog = crud.get_dog(db=db, dog_pk=pk)
    if db_dog is None:
        raise HTTPException(status_code=404, detail=f"Dog with pk {str(pk)} is not found")
    return db_dog


@app.patch("/dog/{pk}",
           response_model=schemas.Dog,
           summary="Update Dog",
           tags=["dogs"])
def update_dog(pk: int, dog: schemas.Dog, db: Session = Depends(get_db)):
    db_dog = crud.get_dog(db=db, dog_pk=pk)
    if db_dog is None:
        raise HTTPException(status_code=404, detail="Dog not found")
    db_dog = crud.get_dog(db=db, dog_pk=dog.pk)
    if pk != dog.pk and db_dog is not None:
        raise HTTPException(status_code=409, detail="Dog with pk you try to assign already exists")
    return crud.update_dog(db=db, dog=dog)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5555)
