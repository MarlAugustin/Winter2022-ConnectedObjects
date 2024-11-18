#Déclaration des variables
ChoixUsager=""
decalage=""
msgACrypter=""
msgADecrypter=""
texte=""
listLettre=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
reponsePossible=['O','N']
messageDecaler=""
reponseAutreMessage="O"
#debut du code
while(reponseAutreMessage=="O"):
    ChoixUsager=input("crypter ou décrypter un message (Choix C ou D) ? ")
    if ChoixUsager.upper()!= 'D'or  ChoixUsager.upper()!= 'C':
        while(ChoixUsager!='D' or ChoixUsager!='C'):
            print("Vous avez écrit une lettre différente de C ou D")   
            ChoixUsager=input("crypter ou décrypter un message (Choix C ou D) ? ")
            if(ChoixUsager=='D' or ChoixUsager=='C'):
                break
    if ChoixUsager.upper()== 'C':
        decalage=input("Entrez le code de décalage (entre 0 et 25): ")
        nbDecalage=int(decalage)
        if nbDecalage>=0 and nbDecalage<=25:
            pass
        else:
            while(nbDecalage<0 or nbDecalage>25):
                print("Vous avez inscrit une valeur suppérieur à 25 ou inférieur à zéro")
                decalage=input("Entrez le code de décalage (entre 0 et 25): ")
                nbDecalage=int(decalage)
           
        msgACrypter=input("Entrez votre message à crypter:")
        texte=msgACrypter
        print("Texte: ",texte)
        nb=0
        "Le but est de trouver l'index de la lettre et d'ensuite la décaler et ajouter cette valeur dans le string"
        while nb<len(texte):
            #indexChar permet de retourner l'index du char et s'il ne se situe pas dans la listLettre (charactere speciaux) il retourne -1
            indexChar=listLettre.index(texte[nb].lower()) if texte[nb].lower() in listLettre else -1
            if indexChar!= -1:
                indexLettre=listLettre.index(texte[nb].lower())
                positionDecalage=(indexLettre+nbDecalage)%26
                #le if elif regarde si la lettre est en majuscule ou miniscule et change le size du caractere selon la reponse
                if texte[nb].islower()==True:
                    messageDecaler+=listLettre[positionDecalage].lower()
                elif texte[nb].isupper()==True:
                    messageDecaler+=listLettre[positionDecalage].upper()
                nb=nb+1  
            else:
                messageDecaler+=texte[nb]
            nb=nb+1  

        print("Message crypter: ",messageDecaler)      
    elif ChoixUsager.upper()== 'D':
      decalage=input("Entrez le code de décalage (entre 0 et 25): ")
      nbDecalage=int(decalage)
      if nbDecalage>=0 and nbDecalage<=25:
            pass
      else:
            while(nbDecalage<0 or nbDecalage>25):
                print("Vous avez inscrit une valeur suppérieur à 25 ou inférieur à zéro")
                decalage=input("Entrez le code de décalage (entre 0 et 25): ")
                nbDecalage=int(decalage)
      msgADecrypter=input("Entrez votre message à décrypter:")
      texte=msgADecrypter
      print("Texte: ",texte)
      nb=0
      decriptageReussi=""
      while nb<len(texte):
        #indexChar permet de retourner l'index du char et s'il ne se situe pas dans la listLettre (charactere speciaux) il retourne -1
        indexChar=listLettre.index(texte[nb].lower()) if texte[nb].lower() in listLettre else -1
        if indexChar!= -1:
          indexLettre=listLettre.index(texte[nb].lower())
          positionDecalage=(indexLettre-nbDecalage)%26
          #le if elif regarde si la lettre est en majuscule ou miniscule et change le size du caractere selon la reponse
          if texte[nb].islower()==True:
              decriptageReussi+=listLettre[positionDecalage].lower()
          elif texte[nb].isupper()==True:
              decriptageReussi+=listLettre[positionDecalage].upper()
          nb=nb+1  
        else:
          decriptageReussi+=texte[nb]
          nb=nb+1  

      print("Message crypté: ",decriptageReussi)

        
        
    reponseUsager=input("Autre message (O/N) ? ")
    reponseValide=reponsePossible.index(reponseUsager.upper()) if reponseUsager.upper() in reponsePossible else -1
    if reponseValide!=-1:
      reponseAutreMessage=reponseUsager
    else:
        #J'ai du mettre un break dans le if pour sortir de la boucle
        while(reponseUsager.upper()!='N' or reponseUsager.upper()!='O'):
            print("Vous avez écrit une lettre différente de O ou N")    
            reponseUsager=input("Autre message (O/N) ? ")
            if(reponseUsager.upper()=='N' or reponseUsager.upper()=='O'):
                break
            
        reponseAutreMessage=reponseUsager

