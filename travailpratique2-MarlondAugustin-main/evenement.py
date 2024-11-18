class Evenement:
    'classe pour la création dun événement'
    def __init__(self,noEvenement,DateHeure,typeEvenement):
        self.noEvenement=noEvenement
        self.DateHeure=DateHeure
        self.typeEvenement=typeEvenement  
    def __repr__(self):
        return self.typeEvenement
    def afficherEvenement(self):
        print(self.noEvenement+") Date : "+ self.DateHeure +" Évenement: "+self.typeEvenement)
