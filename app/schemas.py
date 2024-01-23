from enum import Enum
from pydantic import BaseModel


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

    class Config:
        from_attributes = True


class Timestamp(BaseModel):
    id: int
    timestamp: int

    class Config:
        from_attributes = True
