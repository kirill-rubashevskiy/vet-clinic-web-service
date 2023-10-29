from enum import Enum
from pydantic import BaseModel


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    kind: DogType
    pk: int

    class Config:
        from_attributes = True


class Timestamp(BaseModel):
    timestamp: int
    id: int

    class Config:
        from_attributes = True
