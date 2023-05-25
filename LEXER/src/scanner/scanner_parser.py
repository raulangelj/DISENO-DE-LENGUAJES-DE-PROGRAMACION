from src.Automata.DFA import DFA
from src.Tokens.Tokens import *
from src.Convertor.Character import *
from src.Automata.DFA import tokenListModel
from src.LR.TokenSintactic import TokenSintactic
from src.LR.Lr import Lr0
import os
import glob
import pickle
import shutil

class ScannerParser():
    def __init__(self, adf_yalex: DFA, header:str, trailer: str) -> None:
        self.adf_yalex = adf_yalex
        self.header = header
        self.trailer = trailer
        self.lr: Lr0 = None
    
    def analize(self, file_to_scan: str) -> None:
        file_data = ''
        with open(file_to_scan, 'r') as file:
            for line in file:
                for character in line:
                    file_data += character
        tokens = None
        sentence = Characters(file_data)
        tokens = self.adf_yalex.simulate(sentence)
        self.tokens = tokens
        for token in tokens:
            if token.token_type.value != 1:
                return_val = token.accepted_state.return_value.value[1:-1].strip() if token.accepted_state.return_value else ''
                exec(return_val)
            else:
                print(f'TOKEN NO VALIDO: {token.characters}')
        self.lr.render_parsing_table()
        adapt_tokens = self.adaptor_tokenListModel(tokens)
        print(self.lr.match(adapt_tokens))
        

    def adaptor_tokenListModel(self, tokens:  List[tokenListModel]) -> List[TokenSintactic]:
        adapt_tokens: List[TokenSintactic] = []
        for token in tokens:
            if token.token_type.value != 1:
                if token.accepted_state.return_value.value:
                    value = token.accepted_state.return_value.token_id
                    adapt_tokens.append(TokenSintactic(value.upper()))
        # if adapt_tokens len is bigger than 0 add the terminal $ to the end
        if adapt_tokens:
            adapt_tokens.append(TokenSintactic(acceptance_simbol))
        return adapt_tokens


    
    # def read_yalex(self) -> None:
    #     file_path = input('Ingrese la ruta del archivo: ')
    #     file_data = ''
    #     with open(file_path, 'r') as file:
    #         for line in file:
    #             for character in line:
    #                 file_data += character
    #     tokens = None
    #     setence = Characters(file_data)
    #     tokens = self.adf_yalex.simulate(setence)
    
    # def generate_scanner_file(self) -> None:
    #     # Clear output directory
    #     if os.path.exists(f'{RUTE_DATA}'):
    #         shutil.rmtree(f'{RUTE_DATA}')
    #     os.makedirs(f'{RUTE_DATA}')
    #     with open(f'{RUTE_DATA}automata.pkl', 'wb') as file:
    #         pickle.dump(self.adf_yalex, file)
        
    #     if not os.path.exists(RUTE_COMPILER):
    #         os.makedirs(RUTE_COMPILER)
    #     with open(f'{RUTE_COMPILER}scanner.py', 'w') as file:
    #         header_value = self.header[2:-2].strip() if self.header else ''
    #         trailer_value = self.trailer[2:-2].strip() if self.trailer else ''
    #         file.write(header_value + '\n' + compiler_content + '\n' + trailer_value)
