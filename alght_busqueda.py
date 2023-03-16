"""ALGORITMOS DE BUSQUEDA EN REDES
AUTHOR:GUSTAVO ESPINOSA OTALORA 
"""

#Llamar librerias
import networkx as nx #Libreria de redes
import matplotlib.pyplot as plt #libreira para plotear
import pandas as pd #libreria de maneo de datos
import scipy as sp #libreria oython cientifico
import numpy as np #libreira manejo de matrices
import random #generador de elecciones aleatorias
import operator #operador

#definicion de funciones
#funcion de busqueda
def walked_nodes_by_degree_prob(network,nodo):
    nodes = list(network.nodes())
    current_node = nodo
    walked_nodes = [current_node]
    while len(walked_nodes) < nx.number_of_nodes(network): #nx.number_of_nodes(G1)
        neighbors = list(network.neighbors(current_node))
        neighbor_degrees = [network.degree(node) for node in neighbors]
        probabilities = [degree/sum(neighbor_degrees) for degree in neighbor_degrees]
        next_node = random.choices(neighbors, weights=probabilities)[0]
        walked_nodes.append(next_node)
        current_node = next_node
    return walked_nodes



"""Creacion de DataFrame, red y Caracteristicas"""
Redani=pd.read_csv("CN_spa.csv",header=None,sep=",") #importar dataframe, lista de enlaces
G = nx.from_pandas_edgelist(Redani,source=0,target=1) #Red
#grafo=nx.draw_networkx(G,with_labels=False,node_size=15)#Dibujar la red
#plt.show()
print("numero de nodos:",G.number_of_nodes(), "numero de enlaces:",G.number_of_edges())

#matriz de adyacencia
adyacencia=nx.adjacency_matrix(G).todense()
#dataframe de la matriz de adyacencia
DFadj=pd.DataFrame(adyacencia)
DFadj.to_csv('adjacencymatrix.csv')


#formacion grafo auxiliar
DFsec=pd.read_csv("adjacencymatrix.csv",header=None)
p1=DFsec.drop([0],axis=0) #elimina la columna de cabecera
p2=p1.drop([0],axis=1) #elimina la fila de cabecera
Pg=nx.from_pandas_adjacency(p2)
G1 = nx.from_pandas_adjacency(p2)
#grafo1=nx.draw_networkx(G1,with_labels=False,node_size=15)
#plt.show()
print("numero de nodos:",G1.number_of_nodes(), "numero de enlaces:",G1.number_of_edges())



#tamaño de cluster
clustersize=nx.average_clustering(G)
print("Tamaño de cluster:",clustersize)

#distribucion de grados red auxiliar
degree=nx.degree(G1)
degree1=pd.DataFrame(degree)
#listdegree1=list(degree)
#degree2=pd.DataFrame(listdegree1, dtype = np.float64)
print("grados de la red auxiliar:",degree1)

#distribucion de grados red animal
degreeani=nx.degree(G)
degree1ani=pd.DataFrame(degreeani)
#listdegree1ani=list(degreeani)
#degree2ani=pd.DataFrame(listdegree1ani, dtype = np.float64)
print("grados de la red animal.",degree1ani)



#Grado medio
meandegree=np.mean(degree1ani.iloc[:,1])
print("grado medio de la red:",meandegree)

#pd.value_counts(degree1.iloc[:,1])


"""BUSQUEDA POR GRADO DE NODO"""


count=1
i=1 #contador
matrix=[] #matriz de resultados
while i < nx.number_of_nodes(G1): #ciclo que crea la matriz nx.number_of_nodes(G1)
    while count < nx.number_of_nodes(G1)+1: #ciclo que recorre la red nx.number_of_nodes(G1)+1
        pp=walked_nodes_by_degree_prob(G1,count)
        count+=1
        matrix.append(pp) #añade las listas a la matriz
        i+=1
newmatrix=np.delete(matrix,0,axis=1) #quita la primera columna
arreglouni=np.ravel(newmatrix)#convierte la mattriz a un arreglo unidimension
valores,frecuencia=np.unique(arreglouni,return_counts=True)#cal val,frec
tabla=[valores,frecuencia]#tabula
dataf=pd.DataFrame(tabla)#dataframe
matrixDF=pd.DataFrame(matrix)
matrixDF.to_csv("matrizF.csv")
print(dataf)

#valores de la matriz y frecuencias
unique_values, counts = np.unique(matrix, return_counts=True)

#arreglo para creacion de histograma
elementoi=unique_values-1
arreglo=list(G.nodes())
palabra=[]
for elemeto in elementoi:
   palabra.append(arreglo[elemeto])
listapalabra=np.reshape(palabra,(1,-1))
frecuenciapalabra=[listapalabra,counts]


#esta seccion imprime el grafico de barras con numbres de los nodos
"""
plt.bar(palabra,counts)
plt.xlabel("Palabra")
plt.xticks(rotation=90,fontsize=7)
plt.ylabel("Frecuencia")
"""
#esta seccion imprime el grafico con numeros en lugar de nombres
plt.bar(elementoi,counts,width=0.8)
plt.xlabel("Numero de nodo")
plt.xticks(rotation=90)
plt.ylabel("Frecuencia")
plt.show()

