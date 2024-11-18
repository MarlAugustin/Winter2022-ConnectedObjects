from tkinter import *
import tkinter as tk
from pydoc import text
from tkinter import messagebox
from time import localtime, strftime
from gpiozero import MotionSensor,LED
from gpiozero import DistanceSensor
import evenement as me
import time 
import LCD1602
from threading import Thread
#création de la fenetre
nbEssaie=0
nbEvent=1
codeValide=False
codeDactivation=30981
journalEvent=list()
state=""
detection=False
ledA=LED(6)
ledB=LED(22)
pir=MotionSensor(12)
class Interface:
    def __init__(self,fenetre):
        self.fenetre=fenetre
        fenetre.title("Système d'alarme")
        fenetre.geometry('700x500')
        fenetre.resizable(0,0)

        self.frmBtn=Frame(fenetre)
        self.frmBtn.pack(side=TOP)
        self.frmTxt=Frame(fenetre)
        self.frmTxt.pack()
        self.frmEti=Frame(fenetre)
        self.frmEti.pack()

        #Bouton Activation système
        self.btn_Activer=Button( self.frmBtn,text="Activation système",width=34)
        self.btn_Activer['command']=self.btn_Activer_clicked
        self.btn_Activer.pack(side = LEFT)
        #Bouton  de désactivation
        self.btn_Desactiver=Button( self.frmBtn,text="Désactivation système",width=33)
        self.btn_Desactiver['command']=self.btn_Desactiver_clicked
        self.btn_Desactiver.pack(side = RIGHT)
        #Barre de défilement
        self.defil_bar=Scrollbar( self.frmTxt)
        self.defil_bar.pack(side = RIGHT,fill = Y)
        #zone de texte
        self.txt_Event=Text( self.frmTxt, yscrollcommand = self.defil_bar.set)
        self.txt_Event.config(state=DISABLED)
        self.txt_Event.pack() 
        self.defil_bar.config( command =  self.txt_Event.yview )
         #ajout de l'etiquette code
        self.ety_code=Entry(self.frmEti,width=60)
        self.ety_code.insert(0,"Code d'accès")
        self.ety_code.config(state=DISABLED)
        self.ety_code.pack(side = LEFT)

        #Bouton validation du code
        self.btn_ValiderCode=Button( self.frmEti,text="Valider code")
        self.btn_ValiderCode['command']=self.btn_ValiderCode_clicked
        self.btn_ValiderCode.config(state=DISABLED)
        self.btn_ValiderCode.pack(side = RIGHT)
        
       
    def setup(self):
        #On initialise l'écran led et on empêche l'usager de cliquer sur le bouton
        LCD1602.init(0x27,1)
        self.btn_ValiderCode.config(state=DISABLED)
    def setup_valide(self):
        #On dit que l'usager a mit le bon code 
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Acces valide")
    def setup_invalide(self):
        #On dit que l'usager a mit un code incorrect
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Acces invalide")
        LCD1602.write(1,1,"Recommencer")
    def setup_bloquer(self):
        #On appele cette méthode pour indiquer que l'usager à mis 3 réponse incorrect et qu'il ne peut plus mettre de réponse
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Acces bloquer")
    def setup_clear(self):
        #on efface ce qui est écrit sur le l'écran LCD
        LCD1602.init(0x27,1)
        LCD1602.clear()
    def setup_notifier(self):
        #On appel cette méthode pour dire qu'une personne a été détecté et qu'elle devrait mettre un code
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Entrez le code")
        LCD1602.write(1,1,"d'activation")
    def setup_desactiver(self):
        #On appel cette méthode lorsque l'usager clique sur le bouton desactiver
        self.setup()
        LCD1602.clear()
        LCD1602.write(0,0,"Systeme")
        LCD1602.write(1,1,"desactiver")
    def detection(self):
        #On utilise cette méthode pour détecter une personne
        global state
        global detection
        if state=="activer" and detection==False:
            pir.wait_for_motion()
            if(pir.value!=0):
                self.setup_notifier()
                detection=True
                self.btn_ValiderCode.config(state=NORMAL)
    def appelThread(self):
        #On appel cette méthode pour créer un thread qui sert à détecter le mouvement
        t=Thread(target=self.detection())
        t.start()

    def btn_Activer_clicked(self):
        #On ajoute au texte l'heure que le système est activer et on rend la modification possible
        # pour le bouton de validation et le champ pour remplir le code
        global state
        global nbEssaie
        global detection
        global nbEvent
        global journalEvent
        detection=False
        nbEssaie=0
        ledA.on()
        ledB.off()
        state="activer"
        self.setup_clear()
        self.txt_Event.config(state=NORMAL)
        self.txt_Event.insert(END,(strftime("%a, %b %d  %H:%M:%S %Y ", localtime())+": Activation du système"+"\n"))
        self.txt_Event.update_idletasks()
        self.txt_Event.config(state=DISABLED)
        self.ety_code.config(state=NORMAL)
        self.btn_ValiderCode.config(state=NORMAL)

        event=me.Evenement(nbEvent,strftime("%a, %b %d  %H:%M:%S %Y ", localtime()),"Activation du sytème d'alarme")
        journalEvent.append(event)
        nbEvent+=1
        self.btn_Desactiver.config(state=DISABLED)
        self.appelThread()
        
        

    def btn_Desactiver_clicked(self):
        #On ajoute au texte l'heure que le système est désactiver et on disable le bouton de validation et le champ pour remplir le code
        #On ferme la lumière vert et on allume la rouge. On réinitialise le nombre d'essaie
        global state
        global detection
        detection=True
        state="desactiver"
        self.txt_Event.config(state=NORMAL)
        self.txt_Event.insert(END,(strftime("%a, %b %d  %H:%M:%S %Y ", localtime())+": Désactivation du système"+"\n"))
        self.txt_Event.config(state=DISABLED)
        self.ety_code.config(state=DISABLED)
        self.btn_ValiderCode.config(state=DISABLED)
        self.setup_desactiver()
        global nbEssaie
        nbEssaie=0
        ledA.off()
        ledB.on()

    def btn_ValiderCode_clicked(self):
        #cette méthode sert à savoir si l'usager a mit le bon code ou non
        global nbEvent,nbEssaie
        global journalEvent
        global codeValide
        global detection
        codeValide=False
        self.txt_Event.config(state=NORMAL)
        try:
            #Permet de convertir la chaine de string en entier et si la valeur est équivalente au code d'activation, c'est un codeValide
            if(int(self.ety_code.get())==codeDactivation):
                codeValide=True
        except:
            pass
              
        if nbEssaie<3 and nbEssaie>=0 :
            if(codeValide==True):
                #On donne accès au bouton désactiver, on fait clignoter la ledA . On insère du texte dans dans txt_event
                #On appelle setup_valide qui écrit que l'accès est valide
                self.setup_valide()
                event=me.Evenement(nbEvent,strftime("%a, %b %d  %H:%M:%S %Y ", localtime()),"Accès valide du sytème d'alarme")
                self.txt_Event.insert(END,(strftime("%a, %b %d  %H:%M:%S %Y ", localtime())+": Accès valide"+"\n"))
                ledA.blink()
                time.sleep(3)   
                self.btn_Desactiver.config(state=NORMAL)
                ledA.on()
                detection=True
            if(codeValide==False):
                #On appelle setup_valide qui écrit que l'accès est invalide
                detection=False
                self.setup_invalide()
                event=me.Evenement(nbEvent,strftime("%a, %b %d  %H:%M:%S %Y ", localtime()),"Accès invalide du sytème d'alarme")
                self.txt_Event.insert(END,(strftime("%a, %b %d  %H:%M:%S %Y ", localtime())+": Accès invalide"+"\n"))
                self.txt_Event.update_idletasks()
            journalEvent.append(event)
            nbEvent+=1
            nbEssaie+=1
            self.appelThread()
        if(nbEssaie==3 and codeValide==False):
            #On indique que le code soit bloquer et que tous les champs sont bloqués
            #On allume aussi la lumière rouge
            self.setup_bloquer()
            ledB.on()
            ledA.off()
            self.ety_code.config(state=DISABLED)
            self.btn_ValiderCode.config(state=DISABLED)
            self.btn_Activer.config(state=DISABLED)
            self.txt_Event.config(state=DISABLED)
            ledB.blink()
        self.ety_code.delete(0,END)

if __name__=="__main__":
    #affichage de la fenetre
    root=tk.Tk()
    app=Interface(root)
    root.mainloop()
