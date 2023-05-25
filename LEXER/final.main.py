from src.Tokens.Tokens import *
from src.YALEX.YALEX import Yalex
from src.YAPAR.YAPAR import Yapar
from src.LR.Lr import Lr0
import os
import glob
import pickle
import shutil

def main():
    try:
        yalex_path = input('Ingrese la ruta del archivo YALEX: ')
        yapar_path = input('Ingrese la ruta del archivo YAPAR: ')
        # Yalex
        yalex = Yalex(yalex_path)
        scanner = yalex.generate_scanner()

        # Yapar
        yapar = Yapar()
        yapar.read_file(yapar_path)
        # validation for tokens
        tokens = yalex.rule_returns.keys()
        for token in yapar.get_tokens_array():
            if token.lower() not in tokens:
                raise Exception(f'Token {token} not found in tokens')
        productions = yapar.get_productions()
        scanner.lr = Lr0(productions)
        # Mover al otro archivo
        input_txt = input('Ingrese la ruta del archivo a analizar: ')
        scanner.analize(input_txt)
    except Exception as e:
        print(e)    

if __name__ == '__main__':
    main()