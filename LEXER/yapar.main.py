from src.YAPAR.YAPAR import Yapar
from src.LR.Lr import Lr0
from src.LR.Production import Production
from src.LR.TokenSintactic import TokenSintactic
from src.Tokens.Tokens import *
import pickle

example_lr = [
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('T')]),
    Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('T'), TokenSintactic('*'), TokenSintactic('F')]),
    Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('F')]),
    Production([TokenSintactic('F'), TokenSintactic('-\\>'), TokenSintactic('('), TokenSintactic('E'), TokenSintactic(')')]),
    Production([TokenSintactic('F'), TokenSintactic('-\\>'), TokenSintactic('id')]),
]

def main():
    # opoen tokens file
    try:
        with open(f'{RUTE_DATA}tokens.pkl', 'rb') as file:
            tokens = pickle.load(file)
            yapar = Yapar()
            file_path = input('Ingrese la ruta del archivo: ')
            yapar.read_file(file_path)
            # yapar.read_file('LEXER/Mocks/YAPAR/slr-1.yalp')
            # check if all the tokens in yapar.get_tokens_array() are in tokens
            for token in yapar.get_tokens_array():
                if token.lower() not in tokens:
                    raise Exception(f'Token {token} not found in tokens')
            productions = yapar.get_productions()
            lr0 = Lr0(productions)
            lr0.graph()
    except Exception as e:
        print(e)
    # yapar.read_file('src/YAPAR/grammar.yapar')
    # yapar.create_automata()
    # yapar.create_scanner()
    # yapar.run_scanner('src/YAPAR/program.yapar')

if __name__ == '__main__':
    main()