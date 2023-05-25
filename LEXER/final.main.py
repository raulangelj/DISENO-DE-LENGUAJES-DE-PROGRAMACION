from src.Tokens.Tokens import *
from src.YALEX.YALEX import Yalex
from src.YAPAR.YAPAR import Yapar
from src.LR.Lr import Lr0
import os
import glob
import pickle
import shutil

compiler_content = f'''import os
import pickle
from src.Tokens.Tokens import *
from src.scanner.scanner_parser import ScannerParser

input_txt = input('Ingrese la ruta del archivo a analizar: ')
with open('{RUTE_DATA}scanner.pkl', 'rb') as file:
    scanner = pickle.load(file)
    scanner.analize(input_txt)
'''

def main():
    try:
        yalex_path = input('Ingrese la ruta del archivo YALEX: ')
        # Yalex
        yalex = Yalex(yalex_path)
        scanner = yalex.generate_scanner()

        yapar_path = input('Ingrese la ruta del archivo YAPAR: ')
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
        if os.path.exists(f'{RUTE_DATA}'):
            shutil.rmtree(f'{RUTE_DATA}')
        os.makedirs(f'{RUTE_DATA}')
        # create picle file with scanner
        with open(f'{RUTE_DATA}scanner.pkl', 'wb') as file:
            pickle.dump(scanner, file)
        if not os.path.exists(RUTE_COMPILER):
            os.makedirs(RUTE_COMPILER)
        with open(f'{RUTE_COMPILER}scanner.py', 'w') as file:
            header_value = scanner.header
            trailer_value = scanner.trailer
            file.write(header_value + '\n' + compiler_content + '\n' + trailer_value)
        # input_txt = input('Ingrese la ruta del archivo a analizar: ')
        # scanner.analize(input_txt)
    except Exception as e:
        print(e)    

if __name__ == '__main__':
    main()