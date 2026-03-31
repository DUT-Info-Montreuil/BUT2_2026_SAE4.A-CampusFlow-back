from pydantic import BaseModel, field_validator, Field
from dtos.CreerVisiteursDTO import *


class VisiteurShortDictDTO(BaseModel):  # Utilisé pour l'endpoint GET /visiteurs
    id: int
    nom: str
    prenom: str
    bac: BacDTO
    adresse: AdresseDTO


class VisiteurLongDictDTO(BaseModel):  # Utilisé pour l'endpoint GET /visiteurs/{visiteurID}
    id: int
    nom: str
    prenom: str
    bac: BacDTO
    lycee: LyceeDTO
    adresse: AdresseDTO
    options: OptionsDTO | None = None
    email: str | None = None
    telephone: str | None = None
    formation_actuelle: FormationActuelleDTO | None = None
