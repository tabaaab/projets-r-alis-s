import halfedge_mesh
from statistics import mean
import numpy as np
import math



def angle_ddrl(mesh):
    angle=[]
    for face in mesh.facets:
        angles_facet=[]
        edge_facet=face.halfedge
        suivante_halfedge=edge_facet.next
        angle_facet=edge_facet.get_angle_normal()
        angles_facet.append(angle_facet)
        while edge_facet.index != suivante_halfedge.index:
            angle_facet=suivante_halfedge.get_angle_normal()
            angles_facet.append(angle_facet)
            suivante_halfedge=suivante_halfedge.next
        angle.append(angles_facet)
    return angle


def max_angle(mesh):
    valeurs=[]
    angle=angle_ddrl(mesh)
    for i in range(len(angle)):
        max_angle=max(angle[i])
        valeurs.append(max_angle)
    return valeurs

def moyenne_angle(mesh):
    valeurs = []
    angle = angle_ddrl(mesh)
    for i in range(len(angle)):
        moyenne_angle = mean(angle[i])
        valeurs.append(moyenne_angle)
    return valeurs


def colors(mesh):
    couleur=[]
    #moyenne des angles
    #valeurs=moyenne_angle(mesh)
    #valeurs=max_angle(mesh)
    #moyenne ameliorer en fonction des voisines
    valeurs=amelioration_loc(mesh)
    maxi= max(valeurs)
    minn= min(valeurs)
    print(valeurs)
    for i in range(len(valeurs)):
        if valeurs[i]==maxi:
            couleur.append([1.0, 0.0,0.0,1.0])
        elif valeurs[i]==minn:
            couleur.append([1.0, 1.0, 1.0, 1.0])
        else:
            #amelioration lineaire G et B varie
            couleur.append([1.0, 1 -(valeurs[i]/maxi), 1 -(valeurs[i]/maxi), 1.0])

    return couleur

def couleur_conversion(mesh):
    col=[]
    fin=[]
    #couleur=colors(mesh)
    couleur=segmentation(mesh)
    for i in couleur:
        col=' '.join(str(elem) for elem in i)
        fin.append(col)
    return fin


def create_off_file(mesh):
    couleurs=couleur_conversion(mesh)
    file_content=['OFF','\n'+str(len(mesh.vertices))+' '+str(len(mesh.facets))+' '+str(int(len(mesh.halfedges)/2))]
    for vertex in mesh.vertices:
        s='\n'+str(vertex.x)+' '+str(vertex.y)+' '+str(vertex.z)
        file_content.append(s)
    for face in range(len(mesh.facets)):
        s='\n3 '+str(mesh.facets[face].a)+' '+str(mesh.facets[face].b)+' '+str(mesh.facets[face].c)+' '+couleurs[face]
        file_content.append(s)
    file=open('tests/data/generated.off','w')
    file.writelines(file_content)
    file.close()


def amelioration_loc(mesh):
    #valeur=moyenne_angle(mesh)
    valeur=max_angle(mesh)
    #valeur=max_angle(mesh)
    nouveaux=[]
    for face in mesh.facets:
        valeur_facet = []
        halfedge=face.halfedge
        suivante_halfedge=halfedge.next
        opposit = halfedge.opposite
        index_voisine_facet = opposit.facet.index
        valeur_facet.append(valeur[index_voisine_facet])
        while halfedge.index!=suivante_halfedge.index:
            opposit=suivante_halfedge.opposite
            index_voisine_facet=opposit.facet.index
            valeur_facet.append(valeur[index_voisine_facet])
            suivante_halfedge = suivante_halfedge.next
        nouveaux.append(mean(valeur_facet))
    return nouveaux

def seuil_par_pi():
    seuil =(math.pi)/36
    return seuil

def seuil_par_moyenne(mesh):
    moyenne = amelioration_loc(mesh)
    seuil = mean(moyenne)
    return seuil

def seuil_par_mediane(mesh):
    moyenne= amelioration_loc(mesh)
    seuil=np.median(moyenne)
    return seuil

def seuil_fixer_par_user():
    entrer=input("entrer un seuil")
    print(entrer)

def segmentation(mesh):
    col=[]
    col1_classe=np.random.uniform(0,1,4)
    col2_classe=np.random.uniform(0,1,4)
    #seuil=seuil_par_moyenne(mesh)
    #seuil=0.02
    seuil=seuil_par_mediane(mesh)
    #seuil=seuil_par_pi()
    valeurs=amelioration_loc(mesh)
    for val in valeurs:
        if val>seuil:
            col1_classe[0]=1
            col1_classe[3]=1
            col.append(col1_classe)
        else:
            col2_classe[0]= 1
            col2_classe[3]= 1
            col.append(col2_classe)
    return col


'''def segmentation_composante_connexe(mesh):
    angle_deadrale=[]

    for face in mesh.facets:
        edge_facet=face.halfedge
        angle_facet=edge_facet.get_angle_normal()'''



mesh = halfedge_mesh.HalfedgeMesh("tests/data/cube_highres.off")


#print(colors(mesh))
#print(couleur_conversion(mesh))
create_off_file(mesh)
#print(amelioration_loc(mesh))
#print(couleur_conversion(mesh))
#print(moyenne_angle(mesh))
#print(couleur_conversion(mesh))
#print(couleur_conversion(mesh))

#print(angle_ddrl(mesh))
#print(moyenne_angle(mesh))
