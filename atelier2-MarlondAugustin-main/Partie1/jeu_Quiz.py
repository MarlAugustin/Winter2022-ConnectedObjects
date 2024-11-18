import json, os,time
from tracemalloc import stop
from moduleAtelier2 import Participant

print("|----------------------------------------------------------|")
print("|          Atelier 2 - Quiz 4B5 - Simon Deschenes          |")
print("|----------------------------------------------------------|")
print("| Choisissez la bonne réponse pour chaque question (a/b/c) |")
print("| q pour quitter                                           |")
print("|----------------------------------------------------------|")
print("")
nomParticipant=input(" Entrez votre nom: ")
fichier="Partie1/questions.json"
nbBonneReponse=0
nbPoints=0
listeReponseUsager=list()
import moduleAtelier2 as me 
#ouverture du fichier
if os.path.exists(fichier):
    
    #lecture du fichier json
    with open(fichier, "r", encoding="utf-8") as fichier_json:
        #envoyer les données dans une liste
        listeQuestions = json.load(fichier_json)
        for i in range(len(listeQuestions)):
            
            # élément de la liste > dictionnaire
            quiz_dict = listeQuestions[i]
            #Question
            question=quiz_dict["q"]
            print((i+1),") ",question)
            #ChoixPossible
            repA=quiz_dict["a"]
            repB=quiz_dict["b"]
            repC=quiz_dict["c"]
            bonneReponse=quiz_dict["rep"]
            nbPointAGagner=quiz_dict["pts"]
            print("<a> ",repA)
            print("<b> ",repB)
            print("<C> ",repC)
            print("")
            reponseUsager=input(" Entrez l'option (a/b/c) ou q pour quitter : ")
            reponseUsager=reponseUsager.lower()
            if(reponseUsager !="a" and reponseUsager !="b" and reponseUsager !="c" and reponseUsager !="q"):
                #Tant que l'usager n'inscrit pas a,b,c ou q on lui force à écrire une des lettres, ça peut être en majuscule ou minuscule
                while reponseUsager !="a" or reponseUsager !="b" or reponseUsager !="c" or reponseUsager !="q":
                    print("Vous n'avez pas mis une option prévue")
                    reponseUsager=input(" Entrez l'option (a/b/c) ou q pour quitter : ")
                    reponseUsager=reponseUsager.lower()
                    if(reponseUsager =="a" or reponseUsager =="b" or reponseUsager =="c" or reponseUsager =="q"):
                       break
            if(reponseUsager =="a" or reponseUsager =="b" or reponseUsager =="c"):
                #Maintenant on s'assure si l'usager a écrit la bonne réponse ou non, ensuite on inscrit sa réponse dans un tableau qu'on utilisera
                #pour enregistrer ses réponses
                            if(reponseUsager!=bonneReponse):
                                print("Mauvaise réponse. La bonne réponse est ",bonneReponse)
                            elif(reponseUsager==bonneReponse):
                                print("Bonne réponse !")
                                nbBonneReponse=nbBonneReponse+1
                                nbPoints=nbPoints+nbPointAGagner
                            print()  
                            listeReponseUsager.append(quiz_dict[reponseUsager])
                            time.sleep(1)
            elif(reponseUsager =="q"):
                #On fermer le programme lorsque l'usager choisi Q
                exit()
#On crée le participant et on procède 
participant = me.Participant(nomParticipant, listeReponseUsager,nbBonneReponse,nbPoints)
fichierEcriture = "Partie1/participants.json"
if os.path.exists(fichierEcriture):
    #ouverture du fichier participants
    with open(fichierEcriture, encoding='utf-8') as fic_json :
        #charger les données json existantes
        donnees = json.load(fic_json)
              
        #ajout du nouveau participant dans la variable json
        donnees.append(participant.__dict__)
# si le fichier n'existe pas        
else:
    donnees = list()
    donnees.append(participant.__dict__) # ajout du nouveau participant dans la liste
    
# ecriture les données dans le fichier json
with open(fichierEcriture, "w", encoding="utf-8") as fic_json:
    json.dump(donnees, fic_json, indent=4, ensure_ascii=False, sort_keys=True)            
                    







        