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


class VisiteurShortDictDTO(BaseModel): # Utilisé pour l'endpoint GET /visiteurs
    id: int
    nom: str
    prenom: str
    bac: BacDTO
    ville: str


class VisiteurLongDictDTO(BaseModel): # Utilisé pour l'endpoint GET /visiteurs/{visiteurID}
    id: int
    nom: str
    prenom: str
    bac: BacDTO
    adresse: AdresseDTO
    options: OptionsDTO | None = None
    email: str | None = None
    telephone: str = None
    formation_actuelle: FormationActuelleDTO | None = None
