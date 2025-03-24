from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args, **kwargs):
        if isinstance(v, ObjectId):  # Si ya es un ObjectId, lo convertimos a string
            return str(v)
        if isinstance(v, str) and ObjectId.is_valid(v):  # Si es un string válido
            return str(v)
        raise ValueError("Invalid ObjectId")

class Task(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: Optional[str] = None
    status: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}