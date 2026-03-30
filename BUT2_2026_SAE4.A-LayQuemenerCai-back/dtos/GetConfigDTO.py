from pydantic import BaseModel, field_validator, Field
from CreerConfigDTO import *


class EvenenementDictDTO(BaseModel):
    intitule: str
    lieu: AdresseDTO
    data: datetime


class FormationDictDTO(BaseModel):
    intitule: str
    domaine: str
