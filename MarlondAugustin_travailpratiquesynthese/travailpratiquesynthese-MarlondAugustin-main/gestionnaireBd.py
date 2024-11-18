import sqlite3
def insertionPartie(nomJoueur,jourPartie,nbPoint):
    try:
        connexion=sqlite3.connect("db_parties/parties.db")
        cur=connexion.cursor()
        #vérification si le joueur existe déjà ou non
        sql_paramVerif="SELECT count(nom) FROM classement WHERE nom ='%s'" %nomJoueur         
        cur.execute(sql_paramVerif)
        
        if cur.fetchone()[0]==1:
            #mise à jour
            sql_param="UPDATE classement SET nom=?,date=?,nbPoint=? WHERE nom = '%s'" %nomJoueur
            data_param=(nomJoueur,jourPartie,nbPoint)
        else:
            #insertion
            sql_param="INSERT INTO classement (nom,date,nbPoint)VALUES (?,?,?)"
            data_param=(nomJoueur,jourPartie,nbPoint)
            
        cur.execute(sql_param,data_param)
        connexion.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Erreur de connexion à la base de données",error)
    finally:
        if connexion:
            connexion.close()
def classementJoueurs():
    try:
        connexion=sqlite3.connect("db_parties/parties.db")
        cur=connexion.cursor()
        #vérification si le joueur existe déjà ou non
        sql_param="SELECT * FROM classement ORDER BY nbPoint DESC"         
        cur.execute(sql_param)
        data=cur.fetchall()
        connexion.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Erreur de connexion à la base de données",error)
    finally:
        connexion.close()
    return data

