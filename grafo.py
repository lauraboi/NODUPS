#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
from graphviz import Digraph
import sys

def caminos(G, go, jerarquia, diccionario, lista_path, provisional, contador_paths):
    """
    Funcion que busca los posibles caminos entre un termino GO y el termino
    raiz y calcula la frecuencia de aparicion de cada nodo presente en los
    caminos encontrados
    """
    paths = nx.all_simple_paths(G, source = go, target = name_to_id[jerarquia])
    for path in paths:
        contador_paths +=1
        for go_id in path:
            if go_id in provisional.keys():
                provisional[go_id] += 1
            else:
                provisional[go_id] = 1
        lista_path.append(nx.subgraph(G, path))
    for go in provisional.keys():
        if go in diccionario.keys():
            diccionario[go] += provisional[go]/contador_paths
        else:
            diccionario[go] = provisional[go]/contador_paths


def from_freq_to_percent(dic, new_dic):
    """
    Funcion que transforma las frecuencias de los terminos GO  en porcentajes
    """
    max = 0
    for nodo in dic:
        if dic[nodo] > max:
            max = dic[nodo]

    for nodo in dic:
        new_dic[nodo] = dic[nodo] / max * 100

def eliminar_frec_baja(grafo):
    """
    Funcion que elimina los nodos con baja frecuencia
    """
    b = set()
    for n in grafo.nodes(data=True):
        if n[1]["frec"] < 4:
            b.add(n[0])

    nuevos_vertices(grafo, b)
    eliminar_nodos(grafo, b)


def nuevos_vertices(grafo, eliminar):
    """
    Funcion que enlaza los nodos entrantes de un nodo con frecuencia baja
    con los nodos salientes del mismo
    """
    for nodo in eliminar:
        if grafo.in_edges(nodo):
            for i_edge in grafo.in_edges(nodo):
                for o_edge in grafo.out_edges(nodo, keys=True):
                    if i_edge[0] != o_edge[1]:
                        grafo.add_edge(i_edge[0], o_edge[1], o_edge[2])


def eliminar_nodos(grafo, eliminar):
    """
    Funcion que elimina los nodos presentes en una lista
    """
    for nodo in eliminar:
        grafo.remove_node(nodo)


def eliminar_listas(grafo):
    """
    Funcion que elimina los atributos de los nodos que son listas
    """
    a = set()
    for n in grafo.nodes(data=True):
        for k in n[1].keys():
            if type(n[1][k]) == type([]):
                a.add(k)

    for n in grafo.nodes(data=True):
        for key in a:
            if key in n[1]:
                del n[1][key]



def grafo_DOT(name, outfichero, GOs, color):
    """
    Funcion que dibuja el grafo con los nodos de una muestra
    """
    # Cabecera
    g = Digraph(str(name), filename = outfichero)
    g.attr(rankdir='BT')
    g.attr('node', fontname='Arial', fontsize='12', shape='box', \
           style='rounded,filled', color="/%s/9" % (color))

    # Definimos rangos de frecuencias para colorear
    rango1 = 5
    rango2 = 7
    rango3 = 10
    rango4 = 15
    rango5 = 20
    rango6 = 30
    rango7 = 50
    rango8 = 70
    rango9 = 100

    # Definimos los nodos
    for nodo in name.nodes(data=True):
        if nodo[1]["frec"] <= rango1:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/1" % (color), shape="diamond")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/1" % (color))
        elif nodo[1]["frec"] <= rango2:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/2" % (color), shape="diamond")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/2" % (color))
        elif nodo[1]["frec"] <= rango3:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/3" % (color), shape="diamond")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/3" % (color))
        elif nodo[1]["frec"] <= rango4:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/4" % (color), shape="diamond")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/4" % (color))
        elif nodo[1]["frec"] <= rango5:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/5" % (color), shape="diamond")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/5" % (color))
        elif nodo[1]["frec"] <= rango6:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/6" % (color), shape="diamond")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/6" % (color))
        elif nodo[1]["frec"] <= rango7:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/7" % (color), shape="diamond", fontcolor="white")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/7" % (color), fontcolor="white")
        elif nodo[1]["frec"] <= rango8:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/8" % (color), shape="diamond", fontcolor="white")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/8" % (color), fontcolor="white")
        elif nodo[1]["frec"] <= rango9:
            if nodo[0] in GOs:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/9" % (color), shape="diamond", fontcolor="white")
            else:
                g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="/%s/9" % (color), fontcolor="white")
        else:
            g.node(nodo[0].replace(":", "_"), label= nodo[0] + '\n' + id_to_name[nodo[0]].replace(" ", "\ ") + '\n' + str(round(nodo[1]["frec"], 2)), fillcolor="red")

    # Definimos los ejes
    for edge in name.edges(keys=True):
        g.edge(edge[0].replace(":", "_"), edge[1].replace(":", "_"), label=edge[2])

    # Representamos el grafo y guardamos el fichero en formato DOT (si hay "/n" en el label no nos sirve el fichero)
    g.render()


if __name__ == "__main__":

    # Se lee el fichero que contiene el grafo de la GO
    G = nx.read_gpickle("/home/alu1718/lauraboi/pipeline_galapagos/go.gpickle")

    # Objeto que se utilizara para obtener el nombre a partir de un GO_ID
    id_to_name = {id_: data.get('name') for id_, data in G.nodes(data=True)}

    # Objeto que se utilizara para obtener el GO_ID a partir del nombre
    name_to_id = {data['name']: id_ for id_, data in G.nodes(data=True) if 'name' in data}

    # Fichero que contiene todos los GO de una muestra en una linea
    # separados por |

    nombre = sys.argv[1]
    fichero = open(nombre, 'r')


    lista_GO = fichero.read()[:-1].split("|")

    # Empezamos a trabajar con las tres jerarquias
    dic_GO_P = dict()
    lista_path_P = list()

    dic_GO_C = dict()
    lista_path_C = list()

    dic_GO_F = dict()
    lista_path_F = list()

    for go in lista_GO:
        ## 'biological_process'
        try:
            provisional_P = dict()
            contador_P = 0

            caminos(G, go, 'biological_process', dic_GO_P, lista_path_P, provisional_P, contador_P)
        except:
            continue

        ## 'cellular_component'
        try:
            provisional_C = dict()
            contador_C = 0

            caminos(G, go, 'cellular_component', dic_GO_C, lista_path_C, provisional_C, contador_C)
        except:
            continue

        ## 'molecular_function'
        try:
            provisional_F = dict()
            contador_F = 0

            caminos(G, go, 'molecular_function', dic_GO_F, lista_path_F, provisional_F, contador_F)
        except:
            continue


    ## Biological process
    P = nx.compose_all(lista_path_P)

    new_dic_GO_P = {}

    from_freq_to_percent(dic_GO_P, new_dic_GO_P)

    # Agregar atributo frecuencia al grafo P
    for nodo in P.nodes():
        P.node[nodo]['frec'] = new_dic_GO_P[nodo]

    # Eliminamos los nodos que tienen frecuencia baja (<4)
    eliminar_frec_baja(P)

    # Guardamos la representacion del grafo en un fichero pdf
    nombreP = "P_graph_" + nombre.split("_")[0]
    grafo_DOT(P, nombreP, lista_GO, "pubu9")


    ## Cellular component
    C = nx.compose_all(lista_path_C)

    new_dic_GO_C = {}

    from_freq_to_percent(dic_GO_C, new_dic_GO_C)

    # Agregar atributo frecuencia al grafo C
    for nodo in C.nodes():
        C.node[nodo]['frec'] = new_dic_GO_C[nodo]

    # Eliminamos los nodos que tienen frecuencia baja (<5)
    eliminar_frec_baja(C)

    # Guardamos la representacion del grafo en un fichero pdf
    nombreC = "C_graph_" + nombre.split("_")[0]
    grafo_DOT(C, nombreC, lista_GO, "ylgn9")



    ## Molecular function
    F = nx.compose_all(lista_path_F)

    new_dic_GO_F = {}

    from_freq_to_percent(dic_GO_F, new_dic_GO_F)

    # Agregar atributo frecuencia al grafo F
    for nodo in F.nodes():
        F.node[nodo]['frec'] = new_dic_GO_F[nodo]

    # Eliminamos los nodos que tienen frecuencia baja (<5)
    eliminar_frec_baja(F)

    # Guardamos la representacion del grafo en un fichero pdf
    nombreF = "F_graph_" + nombre.split("_")[0]
    grafo_DOT(F, nombreF, lista_GO, "purples9")
