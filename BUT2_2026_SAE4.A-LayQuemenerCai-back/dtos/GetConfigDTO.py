from pydantic import BaseModel, field_validator, Field
from dtos.CreerConfigDTO import *


class EvenementDictDTO(BaseModel):
    id: int
    intitule: str
    lieu: AdresseDTO
    date: datetime


class FormationDictDTO(BaseModel):
    id: int
    intitule: str
