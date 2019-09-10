#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# Se indican los dos ficheros a unir y el fichero de salida
interpro_file = sys.argv[1]
join_file = sys.argv[2]
outfile = join_file.split("_")[0] + "_interpro.txt"


dic_inter = dict()

# Para cada linea del fichero de anotacion de InterProScan
for linea in open(interpro_file, "r"):
    linea = linea.strip().split("\t")
    # Se comprueba que hayan anotaciones y se guardan los GO anotados a cada accession
    if linea[0].split(".")[0] in dic_inter.keys() and len(linea) >= 14:
        dic_inter[linea[0].split(".")[0]].extend(linea[13].split("|"))
    # Si aun no existe el accession en el diccionario se agrega
    elif len(linea) >= 14:
        dic_inter[linea[0].split(".")[0]] = linea[13].split("|")

listaGO = list()

# Se eliminan los GO duplicados por cada accession y se guardan en la lista
for acc in dic_inter.keys():
    tset = set(dic_inter[acc])
    listaGO.extend(list(tset))

# Los GO anotados con el mapeador se guardan en una lista sin el Aspect
for line in open(join_file, "r"):
    line = line.strip().split(";")
    if line[0] == "taxid":
        continue
    else:
        for go in line[7].split("|"):
            listaGO.append(go[2:])

# Se concantenan todos los GO y se guardan en el fichero de salida
cadena = ""

for go in listaGO:
    if go != "":
        cadena += go + "|"

out = open(outfile, "w")

out.write(cadena[:-1])

out.close()
