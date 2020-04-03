import random
import math

def Ouverture_Fichier():
    #ouverture et lecture du fichier
    fichier=open("iris.data","r")
    liste=[]
    temp=[]
    for ligne in fichier:
        if (ligne != '\n'):
            temp = ligne.rstrip("\n").split(",")
            for i in range(4):
                temp[i]=float(temp[i])
            liste.append(temp)
    fichier.close()
    return liste
 
def Normalisation (tab,axe):

    liste = []
    for element in tab:
        liste.append(element[axe])
    
    result = []
    for valeur in liste:
        valeur_a_ajouter = (valeur-min(liste))/(max(liste)-min(liste))
        result.append(valeur_a_ajouter)
    
    for i in range(len(tab)):
        tab[i][axe] = result[i]
    return

def Trouver_les_k_voisins (tab,k,element):
    result = []
    liste_des_distances = []
    for point in tab:
        d0 = ((point[0]-element[0])**2)
        d1 = ((point[1]-element[1])**2)
        d2 = ((point[2]-element[2])**2)
        d3 = ((point[3]-element[3])**2)
        p0 = 1
        p1 = 1
        p2 = 1
        p3 = 1
        distance = math.sqrt( p0*d0 + p1*d1 + p2*d2 + p3*d3 )
        liste_des_distances.append(distance)
    
    

    for i in range(k):
        value_min = min(liste_des_distances)
        liste_des_index_des_minimums = []
        for element in liste_des_distances:
            if (element == value_min):
                liste_des_index_des_minimums.append(liste_des_distances.index(element))
        index_conserve = random.choice(liste_des_index_des_minimums)
        result.append([tab[index_conserve],liste_des_distances[index_conserve]])
        del tab[index_conserve]
        del liste_des_distances[index_conserve]

    return result

def Determination_de_element(liste_voisin_distance):

    grp_versicolor = 0
    grp_virginica = 0
    grp_setosa = 0
    maxi = liste_voisin_distance[len(liste_voisin_distance)-1][1]
    for element in liste_voisin_distance:
        #! On veut mettre en avant la proximité des k voisins par rapport à l'élément testé
        #! On peut imaginer que notre élément à tester est au centre d'un cercle de rayon égal au maxi des distances des k voisins avec cet élément
        #! Ainsi plus un voisin est proche de l'élément à tester, plus il est probable que l'élément soit considéré comme faisant
        #! partie du même groupe que lui 
        if(element[0][4]== 'Iris-versicolor'):
            grp_versicolor +=  maxi- element[1] 
        if(element[0][4]== 'Iris-virginica'):
            grp_virginica += maxi-element[1] 
        if(element[0][4]== 'Iris-setosa'):
            grp_setosa += maxi -element[1] 
    if((grp_versicolor> grp_setosa) and (grp_versicolor> grp_virginica)): return 'Iris-versicolor'
    if((grp_setosa> grp_versicolor) and (grp_setosa> grp_virginica)): return 'Iris-setosa'
    if((grp_virginica> grp_setosa) and (grp_virginica> grp_versicolor)): return 'Iris-virginica'


def Algorithme_K_Voisin (k):
    liste = Ouverture_Fichier()
    Normalisation(liste,0)
    Normalisation(liste,1)
    Normalisation(liste,2)
    Normalisation(liste,3)
    
    index_element_a_tester = random.randrange(len(liste))
    element_a_tester = liste[index_element_a_tester]
    del liste[index_element_a_tester]


    liste_des_k_vsn = Trouver_les_k_voisins(liste,k,element_a_tester)

    reponse = Determination_de_element(liste_des_k_vsn)

    return (reponse,element_a_tester[4])


#! Main
nb_bon = 0
matrice_resultat = [[0,0,0],[0,0,0],[0,0,0]]
nb_eval = 100 #on teste 500 fois
k = 5 #k=5 semble être une valeur plafond en terme de précision

#Calcul des nb_eval tests et entrées dans la matrice de confusion
for i in range(nb_eval):
    tupl = Algorithme_K_Voisin(k)
    notre_resultat,vrai_result = tupl
    if(notre_resultat == vrai_result): nb_bon+=1


    if(notre_resultat=='Iris-versicolor'): x=0
    if(notre_resultat=='Iris-setosa'): x=1
    if(notre_resultat=='Iris-virginica'): x=2

    if(vrai_result=='Iris-versicolor'): y=0
    if(vrai_result=='Iris-setosa'): y=1
    if(vrai_result=='Iris-virginica'): y=2
    matrice_resultat[x][y]+= 1

    
print()
print("Le taux de réussite de l'algorithme est de " + str((nb_bon/nb_eval)*100) + "% sur " + str(nb_eval) + " tentatives")
print()
print('A gauche on lit ce que nous avons trouvé, en haut ce que la réponse était')
print()
print('            versicolor| setosa | virginica')
print('versicolor |    ' + str(matrice_resultat[0][0]) + '    | ' + str(matrice_resultat[0][1]) + '      |   ' + str(matrice_resultat[0][2]))
print('setosa     |    ' + str(matrice_resultat[1][0]) + '     | ' + str(matrice_resultat[1][1]) + '     |   ' + str(matrice_resultat[1][2]))
print('virginica  |    ' + str(matrice_resultat[2][0]) + '     | ' + str(matrice_resultat[2][1]) + '      |   ' + str(matrice_resultat[2][2]))

