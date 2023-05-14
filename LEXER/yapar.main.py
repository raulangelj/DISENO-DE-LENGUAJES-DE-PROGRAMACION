from src.YAPAR.YAPAR import Yapar
from src.LR.Lr import Lr0
from src.LR.Production import Production
from src.LR.TokenSintactic import TokenSintactic

example_lr = [
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('E'), TokenSintactic('+'), TokenSintactic('T')]),
    Production([TokenSintactic('E'), TokenSintactic('-\\>'), TokenSintactic('T')]),
    Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('T'), TokenSintactic('*'), TokenSintactic('F')]),
    Production([TokenSintactic('T'), TokenSintactic('-\\>'), TokenSintactic('F')]),
    Production([TokenSintactic('F'), TokenSintactic('-\\>'), TokenSintactic('('), TokenSintactic('E'), TokenSintactic(')')]),
    Production([TokenSintactic('F'), TokenSintactic('-\\>'), TokenSintactic('id')]),
]

def main():
    yapar = Yapar()
    yapar.read_file('LEXER/Mocks/YAPAR/slr-1.yalp')
    productions = yapar.get_productions()
    lr0 = Lr0(productions)
    lr0.graph()
    # yapar.read_file('src/YAPAR/grammar.yapar')
    # yapar.create_automata()
    # yapar.create_scanner()
    # yapar.run_scanner('src/YAPAR/program.yapar')

if __name__ == '__main__':
    main()