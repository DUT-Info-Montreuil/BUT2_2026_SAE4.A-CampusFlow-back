from datetime import datetime
from pydantic import BaseModel, field_validator, Field


class AdresseDTO(BaseModel):
    ville: str = Field(min_length=2)
    codePostal: int


class EvenementDTO(BaseModel):
    intitule: str = Field(min_length=2)
    lieu: AdresseDTO
    date: datetime


class FormationDTO(BaseModel):
    intitule: str = Field(min_length=2)