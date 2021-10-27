#!/usr/bin/python3

import sys, getopt

from manejador import manejador

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hf:d:",["file=","database="])
    except getopt.GetoptError:
        print("Hubo un error!")

    base = 'base.db'
    nombre_archivo = "ejemplo.pdf"

    for opt, arg in opts:
        if opt in ("-f", "--file"):
            nombre_archivo = arg
        elif opt in ("-d", "--database"):
            base = arg

    pass_manager = manejador(base)
    data = pass_manager.leer(nombre_archivo)

    file = open(data[0], 'wb')
    file.write(data[1])
    file.close()

if __name__ == "__main__":
   main(sys.argv[1:])