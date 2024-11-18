from msilib.schema import ListBox
from posixpath import split
from pydoc import text
import re
from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
from turtle import bgcolor, left
import os,json

#Variable
pointage=""
NbReponse=""
listeParticipants=list()
listeReponsesParticipants=list()
listeBonnesReponsesParticipants=list()
listePointageParticipants=list()
bonneReponse=["Raspberry Pi","Python","Visual Studio Code","#","strip","len('bonjour')","majuscule=('bonjour').upper()",
                  "minuscule=('BONSOIR').lower()","isNum=('32').isnumeric()","Github"]
#méthode
def btn_Importation_clicked():
   #Lorsqu'on clique sur le bouton on appelle la méthode qui ajoute 
   btn_Importation_Paticipants()
def btn_Importation_Paticipants():
   #cette méthode permet d'importer les participants
   fichier="Partie1/participants.json"
   if os.path.exists(fichier):
       #lecture du fichier json
      with open(fichier, "r", encoding="utf-8") as fichier_json:
         #envoyer les données dans une liste
         listeParticipants = json.load(fichier_json)
         #On ajoute les données dans différentes listes 
         for i in range(len(listeParticipants)):
            participant_dict = listeParticipants[i]
            listeReponsesParticipants.append(participant_dict["listeReponses"])
            nom=participant_dict["nomParticipant"]
            listeBonnesReponsesParticipants.append(participant_dict["nb_bonnesrep"])
            listePointageParticipants.append(participant_dict["pointage"])
            lst_participants.insert(END,nom)
            #lst_participants.select_set(0)
   else:
      messagebox.showerror("Il n'y a pas de participant","Vous devez d'abord jouer à jeu_Quiz")
      exit()
def clear_Text():
   #efface les données du champ de texte lorsqu'on change de participants
   txt_reponseParticipants.delete(1.0,END)
def changer_Contenu_lbl(pointage,NbReponse):
   #On change la valeur du label
      NbReponse_var.set(" Nombre de bonnes réponses: "+NbReponse)
      pointage_var.set(" Pointage: "+pointage)

#méthode sur le clic d'un élément de la liste
def lst_participant_onSelect(evt):
   #On trouve l'index sélectionner. Ensuite on appelle la méthode clear_Text et
   # pour finir on ajoute une réponse de participants à la fois. on fait un saut de ligne pour que les données soit lisibles
   # les états permet de faire que le txt soit readonly ou non
    index = int(lst_participants.curselection()[0])
    txt_reponseParticipants.config(state=NORMAL)
    clear_Text()    
   #On cherche dans la liste de point ainsi que dans la liste de reponse ce que le participant a inscrit et on l'affiche
    pointsParticipant=listePointageParticipants.__getitem__(index)
    NbReponseParticipant=listeBonnesReponsesParticipants.__getitem__(index)
    pointage=str(pointsParticipant)
    NbReponse=str(NbReponseParticipant)
    changer_Contenu_lbl(pointage,NbReponse)
    for i in listeReponsesParticipants.__getitem__(index):
       if bonneReponse.__contains__(i):
          txt_reponseParticipants.insert(END,i,'vert')
       else: 
          txt_reponseParticipants.insert(END,i,'rouge')
       txt_reponseParticipants.insert(END, '\n')
    txt_reponseParticipants.config(state=DISABLED)

    
    
#création de la fenetre
fenetre=Tk()
fenetre.title("Atelier 2 - Quiz 4B5")
fenetre.geometry('600x450')

frame=Frame(fenetre)
frame.pack(side=TOP)

pointage_var=StringVar()
NbReponse_var=StringVar()

#ajout du label lbl_participantSelectionne
lbl_participantSelectionne=Label(frame,text=" Résultats Quiz 4B5 - Marlond Augustin")
lbl_participantSelectionne.grid(column=0, row=1)

#ajout du label pointage
lbl_pointage=Label(frame,textvariable=pointage_var)
lbl_pointage.grid(column=0, row=2)

#ajout du label nbBonneReponse
lbl_nbBonneReponse=Label(frame,textvariable=NbReponse_var)
lbl_nbBonneReponse.grid(column=0, row=3)
#ajout du listBox participant
frm_milieu=Frame(fenetre)
frm_milieu.pack()
lst_participants=Listbox(frm_milieu,width=40,height=20)
lst_participants.pack(side=LEFT)
#gestion de L'evenement lst_participant_onSelect
lst_participants.bind("<<ListboxSelect>>", lst_participant_onSelect)

#ajout du text 
txt_reponseParticipants=Text(frm_milieu,width=30,height=20)
#tag config permet dans cette situation de donner une couleur différente au texte
txt_reponseParticipants.tag_config("vert",foreground="green")
txt_reponseParticipants.tag_config("rouge",foreground="red")
txt_reponseParticipants.pack(side=RIGHT)

#ajout du bouton importer
frame_btn=Frame(fenetre)
frame_btn.pack(side=BOTTOM, fill=BOTH)
btn_importer=Button(frame_btn,text="Importer résultats",command=btn_Importation_clicked,bg='white')
btn_importer.pack(fill=BOTH)

#affichage de la fenetre
fenetre.mainloop()