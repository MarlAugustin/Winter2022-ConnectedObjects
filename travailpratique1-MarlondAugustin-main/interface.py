from cgitb import enable
from http.client import NO_CONTENT
from lib2to3.pytree import convert
from tkinter import *
import tkinter as tk
from pydoc import text
from tkinter import messagebox
from gpiozero import Button as btn
from gpiozero import LED
import json
from tokenize import String
from threading import Thread

#variable
fichier=("questions.json")
partieDebuter=False
reponse=""
rep=""
bonneReponse=""
i=0
nbBonneReponse=0
nbPoint=0
ledA=LED(6)
ledB=LED(21)
ledC=LED(22)
buttonA=btn(24)
buttonB=btn(23)
buttonC=btn(12)
#création de la fenetre
class Interface:
    def __init__(self,fenetre):
        self.fenetre=fenetre
        fenetre.title("Jeu questionnaire")
        fenetre.geometry('650x450')
        fenetre.resizable(0,0)


        self.frame=Frame(fenetre)
        self.frame.pack(side=TOP)
        self.frmBtn=Frame(fenetre)
        self.frmBtn.pack()
        self.frmTxt=Frame(fenetre)
        self.frmTxt.pack()
        #le string var ne fonctionne pas
        self.pointage_var=tk.StringVar()
        self.pointage_var.set("NA")

        #ajout du label pointage
        self.lbl_pointage=Label( self.frame,text="Pointage: ")
        self.lbl_pointage.grid(column=1, row=0)
        #ajout du label nbPoint
        self.lbl_nbPoint=Label( self.frame,textvariable=self.pointage_var)
        self.lbl_nbPoint.grid(column=2, row=0)
        #ajout de l'etiquette participant
        self.ety_participant=Entry( self.frame)
        self.ety_participant.grid(column=0, row=0)
        #Bouton  débuter partie
        self.btn_Debuter=Button( self.frmBtn,text="Débuter la partie")
        self.btn_Debuter['command']=self.btn_debut_partie_clicked
        self.btn_Debuter.pack(side = LEFT)
        #Bouton  question suivante
        self.btn_suivant=Button( self.frmBtn,text="Question suivante")
        self.btn_suivant['command']=self.btn_question_suivante_clicked
        self.btn_suivant.pack(side = RIGHT)
        #Barre de défilement
        self.defil_bar=Scrollbar( self.frmTxt)
        self.defil_bar.pack(side = RIGHT,fill = Y)
        #zone de texte
        self.txt_question=Text( self.frmTxt, yscrollcommand = self.defil_bar.set)
        self.txt_question.pack() 
        #affichage de la fenetre
        self.defil_bar.config( command =  self.txt_question.yview )

    def lecture_fichier(self):
        #On s'assure que l'usager ne puisse plus changer son nom
        self.ety_participant.config(state=DISABLED)
        #lecture du fichier json
        with open(fichier, "r", encoding="utf-8") as fichier_json:
            #envoyer les données dans une liste
            listeQuestions = json.load(fichier_json)
            global i
            global bonneReponse
            global reponse,rep
            reponse=""
            # élément de la liste > dictionnaire
            quiz_dict = listeQuestions[i]
            #Question
            question=quiz_dict["q"]
            self.btn_suivant.config(state=DISABLED)
            self.txt_question.config(state=NORMAL)
            self.txt_question.insert(END,(str(i+1)+") "+question+"\n"))
            #ChoixPossible
            repA=quiz_dict["a"]
            repB=quiz_dict["b"]
            repC=quiz_dict["c"]
            bonneReponse=quiz_dict["rep"]
            nbPointAGagner=quiz_dict["pts"]
            #Insertion des questions
            self.txt_question.insert(END,("<a> "+repA+"\n"))
            self.txt_question.insert(END,("<b> "+repB+"\n"))
            self.txt_question.insert(END,("<c> "+repC+"\n"))
            self.txt_question['state']=DISABLED
            #Les lumières fonctionne, mais il y a une erreur le texte s'affiche seulement lorsque le bouton est pressé
            t=Thread(target=self.allumageLed)
            t.start()
            i+=1
    def clear_Text(self):
            #efface les données du champ de texte lorsqu'on change de participants et on ferme les lumières
           ledA.off()
           ledB.off()
           ledC.off()
           self.txt_question.config(state=NORMAL)
           self.txt_question.delete(1.0,END)
    def reponseValide(self):
            #On clignote la bonne réponse et on annonce au joueur s'il a choisi la bonne réponse
            global bonneReponse,rep
            global nbPoint,nbBonneReponse
            self.txt_question.config(state=NORMAL)
            if rep==bonneReponse:
                    if rep=="a":
                        ledA.blink()
                    elif rep=="b":
                        ledB.blink()
                    elif rep=="c":
                        ledC.blink()
                    nbBonneReponse=nbBonneReponse+1
                    nbPoint=nbPoint+2
                    self.pointage_var.set(str(nbPoint))
                    self.txt_question.insert(END,("\n"+"Vous avez choisi "+bonneReponse+". Bonne réponse!"))
            else:
                    ledA.off()
                    ledB.off()
                    ledC.off()
                    if bonneReponse=="a":
                        ledA.blink()
                    elif bonneReponse=="b":
                        ledB.blink()
                    elif bonneReponse=="c":
                        ledC.blink()
                    self.txt_question.insert(END,("\n"+"Vous avez choisi "+rep+". Mauvaise réponse! La bonne réponse est "+bonneReponse))
            self.txt_question.config(state=DISABLED)
            self.btn_suivant.config(state=NORMAL)

    def btn_debut_partie_clicked(self):
            #On s'assure que l'usager à son nom et on affiche la première question
            global partieDebuter
            global i
            if partieDebuter==FALSE and self.ety_participant.get()!="":
                i=0
                self.lecture_fichier()
                partieDebuter=True
                self.btn_Debuter.config(state=DISABLED)
            #Si le participant ne mets pas son nom on affiche une erreur
            elif self.ety_participant.get()=="":
                messagebox.showerror("Champ vide","Nom incompatible")

    def allumageLed(self):
                #Cette méthode sert à donner une valeur à réponse selon le bouton presser par l'usager
                global rep
                rep=""
                #devrais-je faire une situation si l'usager clicke sur question suivante?
                while rep=="":
                    if buttonA.is_pressed:
                        rep="a"
                        ledA.on()
                        self.reponseValide()
                    elif buttonB.is_pressed:
                        rep="b"
                        ledB.on()
                        self.reponseValide()
                    elif buttonC.is_pressed:
                        rep="c"
                        ledC.on()
                        self.reponseValide()
                global reponse
                reponse=rep

    def btn_question_suivante_clicked(self):
            #je devrai effacer le contenu de txt_question et je devrai ajouter une nouvelle question
            #et ajouter des points si l'usager a mis une bonne réponse
            self.clear_Text()
            global i,nbBonneReponse,nbPoint
            global partieDebuter
        #lecture du fichier json
            if(i<10 and partieDebuter==True):
                self.lecture_fichier()
            elif i==10: 
                messagebox.showinfo("Résultat ",(self.ety_participant.get()+", vous avez "+str(nbBonneReponse)+" sur 10"))
                self.ety_participant.config(state=NORMAL)
                self.btn_Debuter.config(state=NORMAL)
                self.pointage_var.set("NA")
                self.ety_participant.delete(0,END)
                self.ety_participant.insert(0,"")
                partieDebuter=False
                nbBonneReponse=0
                nbPoint=0
                i=0

            elif partieDebuter!=True:
                 messagebox.showerror("Partie non débuté ","Vous n'avez pas débuter la partie")

        
if __name__=="__main__":
    root=tk.Tk()
    app=Interface(root)
    root.mainloop()
