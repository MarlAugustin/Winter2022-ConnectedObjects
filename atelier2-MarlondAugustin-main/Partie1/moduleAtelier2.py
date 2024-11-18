class Participant:
    'classe pour la création dun participant'
    def __init__(self,nomParticipant,listeReponses,nb_bonnesrep,pointage):
        self.nomParticipant=nomParticipant
        self.listeReponses=listeReponses
        self.nb_bonnesrep=nb_bonnesrep
        self.pointage=pointage  
    def __repr__(self):
        return self.nomParticipant
    def afficherParticipant(self):
        print("Nom participant:  "+self.nomParticipant+", listes réponse : "+ self.listeReponses +", Nb bonnes reponse :"+self.nb_bonnesrep+" , Programme: "+self.pointage)
      