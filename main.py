#crédit gabinbsn

### Bibliothèque graphique

##cette bibliothèque importe le webdriver
from selenium import webdriver

## cette bibliothèque importe la recherche d'élement html en python
from selenium.webdriver.common.by import By

## cette bibliothèque importe l'intéraction du clavier
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
## cette biblitothèque importe le temps et donne une possibilité de mettre en pause le programme
import time


###

## création de la classe mère
class sutomlancement:

    ##initialisation des instances, la variable driver permet
    # d'indiquer au programme si il utilise firefox,edge,chrome
    def __init__(self, driver):
        self.driver = driver

        ## Driver= str

    def initdriver(self):
        ## On converti le string en instance WebDriver, pour que le programme fonctionne sur les différents moteurs de recherche

        ## ici le self.driver s'associera à un driver permettant d'automatiser une page web par le moteur Edge
        self.driver = webdriver.Edge()

    ##associer driver à l'url de tusmo
    def lancersite(self):
        self.driver.get('https://sutom.nocle.fr/')

    ##lorsque cette fonction est appelé, Selenium fermera le pop_up règle pour pouvoir lancer le jeu
    def fermerregle(self):
        ## Bouton contient l'id HTML du bouton qui ferme le pop-up des règles (par une croix)
        bouton = self.driver.find_elements(By.ID, "panel-fenetre-bouton-fermeture")

        ## une fois le bouton stocké dans un tableau, nous simulons un clic
        bouton[0].click()

    ## Pour éviter que la page se referme trop rapidement, mettre ce code pour attendre

    def attendre(self):
        time.sleep(5000)


## Une fois la partie lancé, cette classe collecter le nombre de case vide pour deviner le nombre de lettre que le mot aura

class savoirnombredelettre(sutomlancement):

    ## Nous avons besoin de récuperer le driver de la classe sutomlancement par l'héritage (super) pour pouvoir savoir quelle moteur de recherche on utilise
    def __init__(self, driver):
        super().__init__(driver)

        # initialisation ou remise du compteyr à zéro
        self.compteur = 0

        # création d'une liste qui contiendra, la version affinnée de self.ligne1

        self.motatrouver = ""

    ## Les lettres sont contenus dans l'objet (case) <td> pour pouvoir connaître la longueur du mot nous devons compter le nombre de <td> dans un <tr> (ligne)

    # Pour récuperer le nombre de <td> (nombre de case contenant une lettre), cette fonction va retourner une variable contenant un <tr>

    def recuperertr(self):
        ##associer à nombrelettre la valeur de la ligne 1 du site internet ex : "P . . I ..R")
        self.ligne1 = self.driver.find_elements(By.XPATH, "/html/body/div/div[3]/table/tr[1]")

    # compter le nombre de lettre pour savoir quel lexique utiliser

    def compterlenombredelettre(self):

        # associer un string contenant, la valeur textuelle brut de la ligne 1 (tr)
        self.nombredelettre = self.ligne1[0].text

        # Parcours de caractere dans la liste nombrelettre
        for caractere in self.nombredelettre:

            # affinage de la recherche en spécifiant que le compteur s'incrèmente seulement si la case est un point ou une lettre de l'alphabet
            if caractere == '.' or caractere.isalpha():
                self.compteur += 1

                # la variable motatrouver contient juste les lettres et points de la version brut ex: "###€€€ le 31 de noel." deviendra "le31denoel."
                self.motatrouver += caractere

        # vérification par la console que le nombre de lettre et le string est celui affiché sur le site Internet
        print("il y 'a {} lettres, le mot est {} ".format(self.compteur, self.motatrouver))


##Une fois, le nombre de lettre trouvé, on ouvre le fichier texte corréspondant à sa première lettre et taille
class ouvrirlefichiercorrespondant(savoirnombredelettre):

    def __init__(self, driver, compteur, motatrouver):
        super().__init__(driver)
        self.compteur = compteur
        self.motatrouver = motatrouver

    # Pour ouvrir le fichier contenant le mot recherché, nous devons connaitre sa premiere lettre
    def devinerpremierelettre(self):
        self.premierelettre = self.motatrouver[0]

    # En fonction de la première lettre, nous allons ouvrir le fichier correspondant à sa lettre
    # Ex si self.premierelettre='a' c'est le fichier lexique/a.txt qui sera ouvert
    def ouvrirfichier(self):
        # convertir le nombre de lettre et la première lettre en lien de texte
        self.lien = "lexique/" + str(
            self.compteur) + "letters/" + self.premierelettre.lower() + ".txt"

        self.fichier = open(self.lien, "r", encoding="UTF-8")

    def creerliste(self):
        # création de la liste contenant tous les mots possibles
        self.nompossible = self.fichier.readlines()

        # maintenant on supprime le "\n" a la fin des mots
        self.nompossible = [i.replace("\n", "") for i in self.nompossible]
        self.nompossible = [word.rstrip('\n') for word in self.nompossible]


## Maintenant que nous avons ouvert le fichier correspondant, nous allons utiliser cette classe pour intéragir avec le site et récupérer les données que nous avons besoin
class Exportercode(ouvrirlefichiercorrespondant):
    def __init__(self, driver, compteur, motatrouver):
        super().__init__(driver, compteur, motatrouver)
        self.devinerpremierelettre()
        self.devinerpremierelettre()
        self.ouvrirfichier()
        self.creerliste()

    ## Cette méthode va connaitre le nombre de ligne restant
    def savoirquelleligne(self):
        self.ligne1 = self.driver.find_elements(By.XPATH, "/html/body/div/div[3]/table")
        print(len(self.ligne1))

    # Cette fonction va rentrer des lettres sur le site Internet puis les envoyer

    def rentrerdeslettres(self):
        # Initialisation de marquerlettre, qui va gérer la simulation de pression du clavier.
        self.marquerlettre = ActionChains(self.driver)
        # puisque le premier caractere est marqué dans la première case du sie internet, nous devons le supprimer pour eviter de faire une erreur de
        # style "aabandon"
        print(self.nompossible)
        self.nompossible[4] = self.nompossible[4][1:]

        print(self.nompossible)

        # Vu que il n'y a pas de zone de formulaire, nous allons simuler la pression de la touche dans send_keys
        self.marquerlettre.send_keys(self.nompossible[4]).perform()

        # Keys return corresponds à la touche "Entrée"
        self.marquerlettre.send_keys(Keys.RETURN).perform()

        # supprimer l'élément de la liste afin d'éliminer le mot incorrect
        del self.nompossible[4]

    def rentrerdeslettres2(self):
        # Initialisation de marquerlettre, qui va gérer la simulation de pression du clavier.
        self.marquerlettre = ActionChains(self.driver)
        # puisque le premier caractere est marqué dans la première case du sie internet, nous devons le supprimer pour eviter de faire une erreur de
        # style "aabandon"
        print(self.nompossible)
        self.nompossible[0] = self.nompossible[0][1:]

        print(self.nompossible)

        # Vu que il n'y a pas de zone de formulaire, nous allons simuler la pression de la touche dans send_keys
        self.marquerlettre.send_keys(self.nompossible[0]).perform()

        # Keys return corresponds à la touche "Entrée"
        self.marquerlettre.send_keys(Keys.RETURN).perform()

        # supprimer l'élément de la liste afin d'éliminer le mot incorrect
        del self.nompossible[0]


## Cette classe va éliminer des mots selon les règles du jeu

class elimination(Exportercode):
    def __init__(self, driver, compteur, motatrouver):
        super().__init__(driver, compteur, motatrouver)
        self.devinerpremierelettre()
        self.devinerpremierelettre()
        self.ouvrirfichier()
        self.creerliste()
        self.compteurs=1
    # Selon la règle du jeu, une lettre qui est grisé dans le clavier numérique, signifie que le mot que l'on cherche, ne possède pas cette lettre
    # Nous avons donc besoin pour cette première couche d'élimination de retirer tout les mots comportant, les lettres que nous n'avont pas besoin

    def casegrise(self):
        print(len(self.nompossible))
        print("0",len(self.nompossible))
        ##Wait va servir a attendre, que le premier mot est marqué
        wait = WebDriverWait(self.driver, 3)
        # Divs va contenir toutes les lettres qui sont grisé
        divs = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='input-lettre lettre-non-trouve']")))

        # On attribue le STR de toutes les lettres, pour les placer dans la liste letters
        letters = [div.get_attribute("innerHTML") for div in divs]
        letters2 = [x.lower() for x in letters]
        print(letters)
        # self.possible prends la valeur du tableau self.nompossible sans les lettres grisées
        liste = [item for item in self.nompossible if all(char not in item for char in letters2)]
        self.nompossible=liste
        print("1",len(liste))
    #ex : si nous entrons le mot fer: et que le site indique que le e par exemple, n'est pas a sa bonne place, nous pouvons supprimer, tout les mots contenant e au deuxième caractère
    def caserouge(self):

        #la ligne, envoie la ligne en recherche du site internet. Par exemple "M.N..E", on va chercher cela dans la balise TR, car les lettres sont contenus dans des balises "td"
        #compteur contient le nombre de ligne restant

        ligne = self.driver.find_element(By.XPATH, "/html/body/div/div[3]/table/tr[1]")

        #maintenant que nous avons récolté la liste, nous allons faire une sous recherche, pour trouver la classe de chaque TD,
        #Ainsi nous pouvons voir les différentes état des lettres, non-trouver, trouvé, pas à leur place
        td_list = ligne.find_elements(By.TAG_NAME, "td")
        compteur = 0
        #création d'une liste qui va contenir les mots filtrés
        liste = []

        #Nous allons parcourir toute les cases pour savoir l'état des lettres
        for td in td_list[1:]:
            print("q",td.text)

            # Passons à la seconde couche d'élimination, en prenant les lettres obligatoire et leurs index et en supprimant les mots où l'emplacement des lettres n'est pas bonne

            #bien-place resultat correspond à la classe des lettres qui ont été trouvé, nous allons donc faire une instruction, lorsque la case
            #dans la liste de case contient une lettre bien placé
            if td.get_attribute('class') == 'bien-place resultat':
                print("q",td.get_attribute('class'), td.text, compteur)

                #nous allons maintenant parcourir, chaque mot de la liste, et créer une nouvelle liste qui contiendra les mots à la bonne place
                for i in range(len(self.nompossible)):

                    # nous allons maintenant parcourir, chaque mot de la liste, et créer une nouvelle liste qui contiendra les mots à la bonne place
                    if self.nompossible[i][td_list[1:].index(td)+1] == td.text.lower():
                        print("bien",self.nompossible[i])

                        #si la place du caractère recherché est égal au caractère à la place du mot de la liste

                        liste.append(self.nompossible[i])


                # self.possible = [word for word in self.nompossible if not any(letter in word for letter in letters)]
        # maintenant, nous avons une liste filtrée, nous n'avons plus que à supprimé les doublons:

        # création d'une fonction, qui va créer une liste d'ensemble (qui va automatiquement supprimer les doublons)
        remove_duplicates = lambda input_list: list(set(input_list))
        liste = remove_duplicates(liste)
        print("3",len(liste))
        self.nompossible=liste


    def casejaune(self):

        # la ligne, envoie la ligne en recherche du site internet. Par exemple "M.N..E", on va chercher cela dans la balise TR, car les lettres sont contenus dans des balises "td"
        # compteur contient le nombre de ligne restant
        ligne = self.driver.find_element(By.XPATH, "/html/body/div/div[3]/table/tr[1]")
        # maintenant que nous avons récolté la liste, nous allons faire une sous recherche, pour trouver la classe de chaque TD,
        # Ainsi nous pouvons voir les différentes état des lettres, non-trouver, trouvé, pas à leur place
        td_list = ligne.find_elements(By.TAG_NAME, "td")
        compteur = 0
        # création d'une liste qui va contenir les mots filtrés
        liste = []

        # Nous allons parcourir toute les cases pour savoir l'état des lettres
        for td in td_list[1:]:

            # Passons à la seconde couche d'élimination, en prenant les lettres obligatoire et leurs index et en supprimant les mots où l'emplacement des lettres n'est pas bonne

            # bien-place resultat correspond à la classe des lettres qui ont été trouvé, nous allons donc faire une instruction, lorsque la case
            # dans la liste de case contient une lettre bien placé
            if td.get_attribute('class') == 'mal-place resultat':
                print(td.get_attribute('class'), td.text, compteur)

                # nous allons maintenant parcourir, chaque mot de la liste, et créer une nouvelle liste qui contiendra les mots à la bonne place
                for i in range(len(self.nompossible)):

                    # nous allons maintenant parcourir, chaque mot de la liste, et créer une nouvelle liste qui contiendra les mots à la bonne place
                    if self.nompossible[i][td_list[1:].index(td) + 1] != td.text.lower():
                        print("mal",self.nompossible[i])
                        # si la place du caractère recherché est égal au caractère à la place du mot de la liste

                        liste.append(self.nompossible[i])

                # self.possible = [word for word in self.nompossible if not any(letter in word for letter in letters)]
           # maintenant, nous avons une liste filtrée, nous n'avons plus que à supprimé les doublons:

        # création d'une fonction, qui va créer une liste d'ensemble (qui va automatiquement supprimer les doublons)
        remove_duplicates = lambda input_list: list(set(input_list))
        liste = remove_duplicates(liste)
        print(len(self.nompossible))
        print("final",len(liste))
        self.compteurs+=1
    def test(self):
        ##Wait va servir a attendre, que le premier mot est marqué
        wait = WebDriverWait(self.driver, 9)
        # Divs va contenir toutes les lettres qui sont grisé
        divs = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/div[3]/table/tr[3]")))

        letters = [div.text for div in divs]
        print("1",letters)
# Cette classe va permettre de rentrer les mots de la liste dans le pendu
""""
class exportermot(Ouvrir):
    def __init__(self,driver,compteur,motatrouver):
        super().__init__(self,driver,compteur,motatrouver)

    def test(self):
        print(self.motatrouver)
"""
## Maintenant que nous avons ouvert le fichier, nous allons trouver par élimination le mot rechercher
"""
class verifieretatdelacase(ouvrirlefichiercorrespondant):

    def __init__(self,driver,compteur,nompossible,motatrouver):
        super.init__(self)
"""


# fonction principal, qui appelle les classes précédentes, une par une
def fonctionjouer(webdriver):
    lancerjeu = sutomlancement(webdriver)
    lancerjeu.initdriver()
    lancerjeu.lancersite()
    lancerjeu.fermerregle()

    # lancerjeu.attendre()

    savoirlettre = savoirnombredelettre(lancerjeu.driver)
    savoirlettre.recuperertr()
    savoirlettre.compterlenombredelettre()

    fichier = ouvrirlefichiercorrespondant(lancerjeu.driver, savoirlettre.compteur, savoirlettre.motatrouver)
    fichier.devinerpremierelettre()
    fichier.ouvrirfichier()
    fichier.creerliste()

    # Instanciation de la sous-classe
    Entrerlettre = Exportercode(lancerjeu.driver, fichier.compteur, fichier.motatrouver)
    Entrerlettre.savoirquelleligne()
    Entrerlettre.rentrerdeslettres()

    case = elimination(lancerjeu.driver, fichier.compteur, fichier.motatrouver)

    case.casegrise()
    case.caserouge()
    case.casejaune()
    #case.test()
    lancerjeu.attendre()


# cette variable lancera le programme
fonctionjouer("webdriver.edge")

