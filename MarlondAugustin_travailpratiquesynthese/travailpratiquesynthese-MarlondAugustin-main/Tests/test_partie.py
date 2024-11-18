import array
import unittest
import partie2 as PartieClasse
import random
class Tester(unittest.TestCase):

    def test_insertionInvalide(self):
        #L'erreur s'agit que le champs des points contient des int mais on entre des strings pour créer une erreur
        listeNom=["Marc","Paul","Nicholas","Jean-Baptiste","Simon"]
        listePoint=[0,1,2,3,4]
        listeDate=["May 07  09:19:48 2022","May 21  09:00:00 2022","June 01  09:30:00 2022","Apr 07  09:19:48 2022","Apr 23  09:30:00 2022"]
        partie=PartieClasse.partie2(listeNom[random.randint(0,4)],listePoint[random.randint(0,4)],listeDate[random.randint(0,4)])
        self.assertEqual(partie.insertion(),"Invalide")
    def test_setPartie(self):
        #On teste si le résultat d'afficherEvenement est équivalent au String créer manuellement
        listeNom=["Marc","Paul","Nicholas","Jean-Baptiste","Simon"]
        listePoint=[0,1,2,3,4]
        listeDate=["May 07  09:19:48 2022","May 21  09:00:00 2022","June 01  09:30:00 2022","Apr 07  09:19:48 2022","Apr 23  09:30:00 2022"]
        i=0
        while i<len(listeDate):
            partie=PartieClasse.partie2(listeNom[i],listeDate[i],listePoint[i])
            self.assertEqual(partie.afficherEvenement(),(listeNom[i]+", Date : "+listeDate[i])+", Nombre de points: "+ str(listePoint[i]))
            i+=1

if __name__=="__main__":
    unittest.main()

