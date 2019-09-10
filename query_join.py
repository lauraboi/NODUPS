#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pymongo import MongoClient
from urllib.parse import quote_plus
import sys

def connect():
    """Obtiene una conexión a la base de datos go de mongo"""
    # Construir una uri para conectar a la base de datos:
    host = 'trurl.uv.es'
    port = '27017'
    username = quote_plus('gouser')
    password = quote_plus('Nai6mail')
    database = quote_plus('go')
    authdb = quote_plus('admin')

    uri = 'mongodb://%s:%s@%s:%s/%s?authSource=%s' % \
        (username, password, host, port, database, authdb)

    client = MongoClient(uri)
    return client


def main():
    """
    Funcion principal que realiza la busqueda de los GO relacionados
    con cada GI anotado a la muestra
    """
    # Se conecta a la base de datos y a la coleccion NODUPS
    client = connect()
    db = client.get_database()
    collection = db.nodups

    # Se indica el fichero de entrada y salida
    file = open(sys.argv[1], "r")
    out = open(sys.argv[1][:-4] + "_go.csv", "w")

    n = 1 # Contador de linea
    # Por cada linea del fichero:
    for line in file:
        line = line.strip()
        # Si es la cabecera se escribe en el fichero de salida
        if n == 1:
            n += 1
            out.write(line + "\n")
        # Si es el cuerpo del fichero:
        else:
            # Se indica que el GI se encuentra en la segunda columna
            gi = line.split(";")[1]
            a = dict()
            a["gi"] = gi # se crea un diccionario con el GI
            b = dict()
            # Se crea un diccionario para indicar los campos que no necesitamos
            b["_id"] = 0

            # Se ejecuta el comando de busqueda
            find = collection.find(a,b)

            go = list()
            go_num = 0 # Contador de GO mapeados a cada GI
            # Se parsean los resultados
            for result in find:
                # Se une la letra que indica la jerarquia del GO al identificador
                junto = result["Aspect"] + ':' + result["GO_ID"]
                go.append(junto)
                go_num += 1

            # Si se han obtenido GO se unen y se escriben en el fichero de salida
            if go:
                out.write(line[:-1] + "|".join(go) + ";" + str(go_num) + "\n")
            else:
                out.write(line + str(go_num) + "\n")


    file.close()
    out.close()

if __name__ == "__main__":
    main()
