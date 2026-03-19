class VisiteursDTO:
    def __init__(self, donnee: dict):
        self.visiteur = dict()
        self.visiteur["_id"] = donnee["_id"]
        self.visiteur["nom"] = donnee["nom"]
        self.visiteur["prenom"] = donnee["prenom"]
        self.visiteur["email"] = donnee["email"]
        self.visiteur["telephone"] = donnee["telephone"]
        self.visiteur["date_naissance"] = donnee["date_naissance"]
        self.visiteur["ville"] = donnee["ville"]
        self.visiteur["codePostal"] = donnee["codePostal"]
        self.visiteur["nomLycée"] = donnee["nomLycée"]
        self.visiteur["intituléBAC"] = donnee["intitulBAC"]
        if donnee["matière1"] is False:
            self.visiteur["matière1"] = donnee["matière1"]
        if donnee["matière1"] is False:
            self.visiteur["matière2"] = donnee["matière2"]
        self.visiteur["intituléActu"] = donnee["intitulActu"]
        self.visiteur["NiveauEtudeActu"] = donnee["NiveauEtudeActu"]
        self.visiteur["intituléEvent"] = donnee["intitulEvent"]
        self.visiteur["lieu"] = donnee["lieu"]
        self.visiteur["dateEvent"] = donnee["dateEvent"]
        self.visiteur["handicap"] = donnee["handicap"]
        self.visiteur["reorientation"] = donnee["reorientation"]
        self.visiteur["immersion"] = donnee["immersion"]
