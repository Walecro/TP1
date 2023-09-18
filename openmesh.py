import matplotlib.pyplot as plt
import math 
import os
def lit_fichier_mesh(path):
    f = open(path,"r")

    #recup tailles array
    tailles = f.readline()
    [nbn,nbt,nba] = map(int ,tailles.split())
    
    #Init arrays 

    coord = []
    tri = []
    ar = []
    refn = []
    reft = []
    refa = []
    

    
    #Recup data
    for i in range(0,nbn):
        data = f.readline()
        data = data.split()
        refn.append(int(data.pop()))
        yd = (float(data.pop()))
        xd = (float(data.pop()))
        coord.append([xd,yd])

    for i in range(0,nbt):
        data = f.readline()
        data = data.split()
        reft.append(int(data.pop()))
        s3d = (int(data.pop()))
        s2d = (int(data.pop()))
        s1d = (int(data.pop()))
        tri.append([s1d,s2d,s3d])

    for i in range(0,nba):
        data = f.readline()
        data = data.split()
        refa.append(int(data.pop()))
        yd = (float(data.pop()))
        xd = (float(data.pop()))
        ar.append([xd,yd])
    #Petit close qui va bien 
    f.close()

    #fix des points du triangle pour faire la correspondance avec l'array coord
    for side in tri:
        side[0] -= 1
        side[1] -= 1
        side[2] -= 1

    return [nbn,nbt,nba,coord,tri,ar,refn,reft,refa] 

def center_tri(x1,x2,x3,y1,y2,y3):
    return ((x1 + x2 + x3)/3, (y1 + y2 + y3)/3)

def center_ar(  ):
    return ((x1+x2)/2,(y1+y2)/2)

"""
Fonction permettant l'affichage d'un maillage
Entrée :
- nbn : nombre de noeuds 
- coord : Array 2D contenant les paires de coordonnées des points du maillage
- tri : Array 2D contenant les triplés de points composant un triangle 
- ar : Array 2D contenant les paires de points composant une arête 
"""
def trace_maillage_ind(nbn,coord,tri,ar):
    plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots() 
    x = []
    y = []
    for i in range(0,nbn):
        x.append(coord[i][0])
        y.append(coord[i][1])
    
    ax.triplot(x,y,tri[:],'o-')

    ind = 0

    #Affichage des indices des sommets
    for x1,y1 in coord:
        
        plt.text(x1,y1,ind, color = "black")
        ind = ind+1
    ind = 0

    #Affichage des indices des triangles
    for ex_tri in tri:
        center = center_tri(coord[ex_tri[0]][0],coord[ex_tri[1]][0],coord[ex_tri[2]][0],coord[ex_tri[0]][1],coord[ex_tri[1]][1],coord[ex_tri[2]][1])
        plt.text(center[0],center[1],ind,color="red")
        ind = ind +1

    ind = 0
    #Affichage des indices des arêtes  
    for ex_ar in ar:
        center = center_ar(coord[int(ex_ar[0]-1)][0],coord[int(ex_ar[1]-1)][0],coord[int(ex_ar[0]-1)][1],coord[int(ex_ar[1]-1)][1] )
        plt.text(center[0],center[1],ind,color="blue")
        ind = ind + 1

    ax.grid(True, which='both')
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.set_title("Mesh with indexes")

    fig.tight_layout()
    plt.show(block = False)

def trace_maillage_ref(nbn,coord,tri,ar,refn,reft,refa):
    plt.style.use('_mpl-gallery-nogrid')
    fig, ax = plt.subplots() 
    x = []
    y = []
    for i in range(0,nbn):
        x.append(coord[i][0])
        y.append(coord[i][1])
    
    ax.triplot(x,y,tri[:],'o-')

    ind = 0
    #Affichage des refs des sommets
    for x1,y1 in coord:
        
        plt.text(x1,y1,refn[ind], color = "black")
        ind = ind+1
    ind = 0

    #Affichage des ref des triangles
    for ex_tri in tri:
        center = center_tri(coord[ex_tri[0]][0],coord[ex_tri[1]][0],coord[ex_tri[2]][0],coord[ex_tri[0]][1],coord[ex_tri[1]][1],coord[ex_tri[2]][1])
        plt.text(center[0],center[1],reft[ind],color="red")
        ind = ind +1

    ind = 0
    #Affichage des ref des arêtes  
    for ex_ar in ar:
        center = center_ar(coord[int(ex_ar[0]-1)][0],coord[int(ex_ar[1]-1)][0],coord[int(ex_ar[0]-1)][1],coord[int(ex_ar[1]-1)][1] )
        plt.text(center[0],center[1],refa[ind],color="blue")
        ind = ind + 1






    ax.grid(True, which='both')
    ax.set_aspect('equal')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.set_title("Mesh with references")
    plt.autoscale()
    fig.tight_layout()
    plt.show()

def get_pas_tri(x1,x2,x3):
    return max( math.dist(x1,x2) , math.dist(x2,x3) , math.dist(x1,x3) )

"""
Fonction renvoyant le pas et la qualité du maillage representé dans tri 
Utilise également coord l'array 2D 
"""
def pas_qualite(coord,tri):
    r_pas = []
    r_qualite = []

    for triangle in tri:
        x1 = coord[triangle[0]]
        x2 = coord[triangle[1]]
        x3 = coord[triangle[2]]
        pastmp = get_pas_tri(x1,x2,x3)
        r_pas.append(pastmp)

        #Perimetre du triangle
        perit = (math.dist(x1,x2) + math.dist(x2,x3) + math.dist(x1,x3)) / 2
 
        #Aire du triangle
        airet = math.sqrt(perit * (perit - math.dist(x1,x2)) *
                (perit - math.dist(x2,x3)) * (perit -  math.dist(x1,x3)))
    
        # rayon du cercle inscrit
        r = airet / perit

        qualite = (math.sqrt(3) / 6 ) * (pastmp / r)
        r_qualite.append(qualite)
    pas = max(r_pas)
    qualite = max(r_qualite)

    


    return (pas,qualite)


def main():

    #Composition du path avec l'input utilisateur
    print([os.path.splitext(filename)[0] for filename in os.listdir("Maillages/")])
    path = input("Choose a mesh \n")
    path = "Maillages/" + path + ".msh"

    #Test d'existence du fichier si oui on continue sinon on arrête 
    if(os.path.exists(path)):

        [nbn,nbt,nba,coord,tri,ar,refn,reft,refa] = lit_fichier_mesh(path)
        trace_maillage_ind(nbn,coord,tri,ar)
        trace_maillage_ref(nbn,coord,tri,ar,refn,reft,refa)
        pas,qualite = pas_qualite(coord,tri)

        print("Pas du mesh = "+ str(pas)+"\nQualite du mesh = "+str(qualite))
    else: 
        print("Mesh does not exist")
    
    
if __name__ == "__main__":
    main()



   
    