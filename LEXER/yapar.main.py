from src.YAPAR.YAPAR import Yapar
from src.LR.Lr import Lr0

def main():
    yapar = Yapar()
    yapar.read_file('LEXER/Mocks/YAPAR/slr-1.yalp')
    lr0 = Lr0([])
    lr0.graph()
    # yapar.read_file('src/YAPAR/grammar.yapar')
    # yapar.create_automata()
    # yapar.create_scanner()
    # yapar.run_scanner('src/YAPAR/program.yapar')

if __name__ == '__main__':
    main()