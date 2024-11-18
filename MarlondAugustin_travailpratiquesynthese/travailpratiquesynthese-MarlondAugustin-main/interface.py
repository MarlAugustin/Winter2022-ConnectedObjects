from tkinter import *
import tkinter as tk
from pydoc import text
from tkinter import messagebox
from time import localtime, strftime
import time 
import random
import LCD1602
import KeypadGPIO as c
from threading import Thread
from gpiozero import LED
import partie as me
import gestionnaireBd as bd
LIGNES=4
COLONNES=3
statePartie=""
rep=""
nbPoint=0
nbManche=0
nbMancheMaximal=10
nombreAleatoire=0
reponseUsager=""
touches=['1','2','3',
         '4','5','6',
         '7','8','9',
         '*','0','#']
lignesGPIO=[5,6,13,19]
colonnesGPIO=[16,20,21]
ledA=LED(24)
ledB=LED(23)
class Interface:
    def __init__(self,fenetre):
        self.fenetre=fenetre
        fenetre.title("Trouver le nombre aleatoire")
        fenetre.geometry('800x600')

        self.frmEti=Frame(fenetre)
        self.frmEti.pack()
        self.frmBtn=Frame(fenetre)
        self.frmBtn.pack(side=TOP)
        self.frmTxt=Frame(fenetre)
        self.frmTxt.pack()
        self.frmBtnFermer=Frame(fenetre)
        self.frmBtnFermer.pack()
        #ajout du label pointage
        self.lbl_pointage=Label( self.frmEti,text="Nom participant: ")
        self.lbl_pointage.grid(column=0, row=0)
        #ajout de l'etiquette participant
        self.ety_participant=Entry(self.frmEti,width=65)
        self.ety_participant.grid(column=1, row=0)
        
        #Bouton Activation de la partie
        self.btn_Demarrer=Button( self.frmBtn,text="Commencer la partie",width=36)
        self.btn_Demarrer['command']=self.btn_Demarrer_clicked
        self.btn_Demarrer.pack(side = LEFT)
        #Bouton  de pour enregistrer la prochaine réponse
        self.btn_Suivant=Button( self.frmBtn,text="Prochain essai",width=36)
        self.btn_Suivant['command']=self.btn_Suivant_clicked
        self.btn_Suivant.pack(side = RIGHT)
        #Barre de défilement
        self.defil_bar=Scrollbar(self.frmTxt)
        self.defil_bar.pack(side = RIGHT,fill = Y)
        #zone de texte 
        self.txt_Event=Text(self.frmTxt, yscrollcommand = self.defil_bar.set,width=100)
        self.txt_Event.config(state=DISABLED)
        self.txt_Event.pack() 
        self.defil_bar.config( command =  self.txt_Event.yview )
        #Bouton pour sauvegarder la partie
        self.btn_Sauvegarde=Button(self.frmBtnFermer,text="Sauvegarder et terminer la partie")
        self.btn_Sauvegarde['command']=self.btn_Sauvegarde_clicked
        self.btn_Sauvegarde.config(state=DISABLED)
        self.btn_Sauvegarde.pack(side = LEFT)
        #Bouton pour voir le classement du joueur du code
        self.btn_Classement=Button(self.frmBtnFermer,text="Classement des joueurs")
        self.btn_Classement['command']=self.btn_Classement_clicked
        self.btn_Classement.pack(side = RIGHT)
        #Bouton pour quitter la partie
        self.btn_quitter=Button(self.frmBtnFermer,text="Quitter la partie")
        self.btn_quitter['command']=self.btn_quitter_clicked
        self.btn_quitter.pack(side = RIGHT)

    def clearChampTexte(self):
        #On efface les données contenu dans le champ de texte
        self.txt_Event.config(state=NORMAL)
        self.txt_Event.delete(1.0,END)
        self.txt_Event.config(state=DISABLED)
        self.txt_Event.update_idletasks()
    def clearChampDeSaisie(self):
        #On efface les données contenu dans le champ de texte ainsi que le champ etiquette
        self.ety_participant.config(state=NORMAL) 
        self.ety_participant.delete(0,END)
        self.clearChampTexte()
    def setup(self):
        #On initialise l'écran led et on empêche l'usager de cliquer sur le bouton
        LCD1602.init(0x27,1)
    def setup_partieNonDebuter(self):
        #On dit que la partie n'a pas débuté et qu'en conséquence on ne peut pas cliquer le bouton suivant
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"La partie n'a ")
        LCD1602.write(0,1,"pas commence") 
    def setup_bonneReponse(self):
        #On dit que l'usager a mit la bonne réponse
        global reponseUsager
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Bonne reponse")
        self.txt_Event.config(state=NORMAL)
        self.txt_Event.insert(END,(self.ety_participant.get()+" Vous avez écrit "+reponseUsager+". Vous avez eu la bonne réponse"+"\n"))
        self.txt_Event.config(state=DISABLED)
    def setup_champVide(self):
        #On dit que le champ pour entrer le nom de l'usager est vide
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Entrez votre nom")

    def setup_mauvaiseReponse(self):
        #On dit que l'usager a mit la mauvaise réponse
        global reponseUsager
        global nombreAleatoire
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Mauvaise reponse")
        self.txt_Event.config(state=NORMAL)
        self.txt_Event.insert(END,(self.ety_participant.get()+" Vous avez écrit "+reponseUsager+". La bonne réponse était "+str(nombreAleatoire)+"\n"))
        self.txt_Event.config(state=DISABLED)
    def setup_afficher(self):
        self.setup()
        LCD1602.clear()
        if nbPoint>=5:
            #On dit à l'usager qu'il doit mettre un chiffre entre 10 et 20
            LCD1602.write(0,0,"Deviner un chiffre")
            LCD1602.write(0,1,"entre 10 et 20")
        else:
            #On dit à l'usager qu'il doit mettre un chiffre entre 0 et 9
            LCD1602.write(0,0,"Deviner un chiffre")
            LCD1602.write(0,1,"entre 0 et 9")
    def setup_sauvegarder(self):
        #On dit que la partie est sauvegardée
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Votre partie est")
        LCD1602.write(0,1,"sauvegardee")
    def setup_quitter(self):
        #On dit que la partie est annulee
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Partie annulee")
    
    def affichageToucheEcran(self):
        #Cette méthode est utile pour enregistrer les réponses écrites à travers le clavier numérique.
        #Si l'usager est chanceux, on augmente la difficulté
        global reponseUsager
        global nbPoint
        clavier=c.Keypad(touches,lignesGPIO,colonnesGPIO,
                         LIGNES,COLONNES)
        clavier.setDebounceTime(50)
        nbCar=0
        if nbPoint>=5:
            while nbCar<2:
                touche=clavier.getKey()
                if(touche!=clavier.NULL):
                   reponseUsager+=touche
                   nbCar+=1
        else:
            while nbCar<1:
                touche=clavier.getKey()
                if(touche!=clavier.NULL):
                   reponseUsager+=touche
                   nbCar+=1
    def insertionPartie(self):
        #On crée une partie et on enregistre les données dans la base de donnée
        global nbPoint
        partie=me.partie(self.ety_participant.get(),str(strftime(" %d %b  %H:%M:%S %Y ", localtime())),nbPoint)
        bd.insertionPartie(self.ety_participant.get(),str(strftime(" %d %b  %H:%M:%S %Y ", localtime())),nbPoint)
        self.setup_sauvegarder()

    def numeroAleatoire(self):
        #cette méthode est utilisé pour générer un chiffre aléatoire et recevoir la réponse du joueur.
        #On l'annonce s'il a écrit une bonne ou une mauvaise réponse
        global nbManche
        global nbPoint
        global reponseUsager
        global nombreAleatoire
        if nbPoint>=5:
            nombreAleatoire = random.randint(10,20)
        else:
            nombreAleatoire = random.randint(0,9)
        self.setup_afficher()
        t=Thread(target=self.affichageToucheEcran())
        t.start()
        if reponseUsager==str(nombreAleatoire):
            nbPoint+=1
            self.setup_bonneReponse()
            ledB.off()
            ledA.blink()
        else:
            self.setup_mauvaiseReponse()
            ledA.off()
            ledB.blink()
        nombreAleatoire=0
        nbManche+=1
        reponseUsager=""

    def btn_Demarrer_clicked(self):
        """ On s'assure que l'usager écrit son nom sinon. on affiche un message sur l'écran led et l'interface
            disant que le champ est vide. Si le champ n'est pas vide, on demande à l'usager d'inscrire un numero et on rend inaccessible
            tous les boutons sauf le bouton suivant pour afficher le classement ainsi que l'etiquette d'entrée. Si On recommence on efface le champ de saisie
        """
        global statePartie
        if self.ety_participant.get()!="":
            if statePartie=="Sauvegarder":
                self.clearChampDeSaisie()
                messagebox.showinfo("Champ effacé","Entrez un nom")
                statePartie=""
            else:
                statePartie="Debuter"
                self.clearChampTexte()
                self.numeroAleatoire()
                self.ety_participant.config(state=DISABLED)
                self.btn_Demarrer.config(state=DISABLED)
                self.btn_Classement.config(state=DISABLED)
                self.btn_Sauvegarde.config(state=DISABLED)
                self.btn_Suivant.config(state=NORMAL)
        else:
            messagebox.showerror("Champ vide","Entrez votre nom")
            self.setup_champVide()

    def btn_Suivant_clicked(self):
        """Si la partie est débuter et que le nombre de manche est inférieur à 10, on appel la méthode numeroAleatoire qui indique à l'usager
            d'inscrire un chiffre variable selon sombre de point. Après 10 tour On affiche les résultats à l'usager, on rend accessible le bouton
            de sauvegarde et on disable le btnSuivant. Si la partie n'a pas débuter on affiche un message sur l'écran led et l'interface
            disant que la partie n'a pas débuté
        """
        global statePartie
        global nbPoint, nbManche  ,nbMancheMaximal      
        if statePartie=="Debuter" and nbManche<nbMancheMaximal:
            self.numeroAleatoire()
            if nbManche==10:
                statePartie="Fini"
                self.btn_Sauvegarde.config(state=NORMAL)
                self.btn_Suivant.config(state=DISABLED)
                self.txt_Event.config(state=NORMAL)
                self.txt_Event.insert(END,(self.ety_participant.get()+" vous avez eu "+str(nbPoint)+" points le "+ strftime(" %d %b  %H:%M:%S %Y ", localtime())))
                self.txt_Event.config(state=DISABLED)
        if statePartie!="Debuter" and statePartie!="Fini":
            messagebox.showerror("Partie non commencer","La partie n'a pas été débuté")
            self.setup_partieNonDebuter()

    def btn_Sauvegarde_clicked(self):
        """On s'assure que la partie est débuter si c'est le cas on rénitialise le nb de manche et de point. On rend accessible
            le bouton de démarrage, le bouton de classement et le champ d'entrée du nom du participant. On ferme les différents led.
            On ajoute les données du joueur à la base de donnée. Si la partie n'a pas débuter on affiche un message sur l'écran led et l'interface
            disant que la partie n'a pas débuté
        """
        global statePartie
        global nbPoint,nbManche
        if(statePartie=="Fini"):
            statePartie="Sauvegarder"
            self.btn_Demarrer.config(state=NORMAL)
            self.ety_participant.config(state=NORMAL)
            self.btn_Suivant.config(state=DISABLED)
            self.btn_Sauvegarde.config(state=DISABLED)
            self.btn_Classement.config(state=NORMAL)
            ledA.off()
            ledB.off()
            self.insertionPartie()
            nbPoint=0
            nbManche=0
        else:
            messagebox.showerror("Partie non commencer","La partie n'a pas été débuté")
            self.setup_partieNonDebuter()
    def btn_Classement_clicked(self):
        #on  extrait de la table de donné et on afficher le classement des différents joueurs. Classement est une liste qui contient toutes les données
        #de la base de donnée. 
        self.clearChampTexte()
        classement=bd.classementJoueurs()
        #print(len(classement))
        i=0
        self.txt_Event.config(state=NORMAL)
        for ligne in classement:
            i+=1
            self.txt_Event.insert(END,("Joueur "+str(i)+") Nom :"+ligne[1]+", Date :"+ligne[2]+", Nombre de points:"+str(ligne[3])+"\n"))
        self.txt_Event.config(state=DISABLED)
    def btn_quitter_clicked(self):
        #Ce bouton servira à quitter la partie
        global statePartie
        global nbPoint,nbManche
        global rep
        if statePartie=="Debuter" or statePartie=="Fini"or statePartie=="Sauvegarder":
            self.clearChampDeSaisie()
            self.setup_quitter()
            rep=""
            nbPoint=0
            nbManche=0
            statePartie="Quitter"
            self.btn_Demarrer.config(state=NORMAL)
            self.ety_participant.config(state=NORMAL)
            self.btn_Suivant.config(state=NORMAL)
            self.btn_Classement.config(state=NORMAL)
            ledA.off()
            ledB.off()
        else:
            messagebox.showerror("Partie non commencer","La partie n'a pas été débuté")
            

if __name__=="__main__":
    #affichage de la fenetre-
    root=tk.Tk()
    app=Interface(root)
    root.mainloop()