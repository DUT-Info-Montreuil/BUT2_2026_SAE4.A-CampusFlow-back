from datetime import datetime
from pydantic import BaseModel, field_validator, Field


class BacDTO(BaseModel):
    intitule: str = Field(min_length=2)
    matiere1: str | None = None
    matiere2: str | None = None
    annee: int


class AdresseDTO(BaseModel):
    ville: str = Field(min_length=2)
    codePostal: int


class OptionsDTO(BaseModel):
    handicap: bool = False
    reorientation: bool = False
    immersion: bool = False


class FormationActuelleDTO(BaseModel):
    intitule: str = Field(min_length=2)
    niveau_etudes: str = Field(min_length=5)


class FormationViseeDTO(BaseModel):
        intitule: str = Field(min_length=2)
        niveau_etudes: str = Field(min_length=5)


class VisiteurCreerDTO(BaseModel):
        nom: str = Field(min_length=2)
        prenom: str = Field(min_length=2)
        date_naissance: datetime
        bac: BacDTO
        adresse: AdresseDTO
        email: str | None = None
        telephone: str = Field(min_length=10, max_length=10, default=None)
        options: OptionsDTO | None = None
        formation_actuelle: FormationActuelleDTO | None = None
