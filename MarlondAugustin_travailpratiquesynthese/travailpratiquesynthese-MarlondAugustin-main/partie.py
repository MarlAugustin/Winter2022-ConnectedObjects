import gestionnaireBd as bd
class partie:
    'classe pour la création dune partie'
    #Je devrai créer un id pour trier
    def __init__(self,nomJoueur,DateHeure,nbPoint):
        self.nomJoueur=nomJoueur
        self.Date=DateHeure
        self.nbPoint=nbPoint  
    def getNPoint(self):
        return self.nbPoint
    def afficherEvenement(self):
        return(self.nomJoueur,", Date : "+ self.Date +", Nombre de points: "+ str(self.nbPoint))
    def __repr__(self):
        return self.nbPoint
    def getNomJoueur(self):
        return self.nomJoueur
    def getDate(self):
        return self.Date