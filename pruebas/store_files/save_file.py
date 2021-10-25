#!/usr/bin/python3

from manejador import manejador
import sys, getopt


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

    

    file = open(nombre_archivo, 'rb')
    binary = file.read()
    file.close()

    pass_manager = manejador(base)
    pass_manager.agregar(binary, nombre_archivo)


if __name__ == "__main__":
   main(sys.argv[1:])