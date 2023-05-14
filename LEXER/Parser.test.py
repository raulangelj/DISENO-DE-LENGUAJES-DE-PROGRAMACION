from src.Convertor.Parser import Parser
from termcolor import colored
import pandas as pd
import os

def test1():
	# Test 1
	# Read file cases.txt
	print('Test 1')
	# read the file name "cases.csv" in this directory with pandas
	df = pd.read_csv(os.path.dirname(__file__) + "/Mocks/cases.csv")
	# for each value in intial column of the dataframe execute the function convert_from_infix_to_postfix and compare the result with the value in thhe parse column
	data = {}
	for index, exp in enumerate(df['Initial']):
		parser = Parser()
		test_postfix = parser.convert_from_infix_to_postfix(exp)
		text_infix = parser.infix
		real_infix = df['Parse'][index]
		real_postfix = df['Postfix'][index]
		data[index] = {
			'Initial': exp,
			'Real_Infix': real_infix,
			'Test_Infix': text_infix,
			'Real_Postfix': real_postfix,
			'Test_Postfix': test_postfix,
			'Pass_Infix': real_infix == text_infix,
			'Pass_Postfix': real_postfix == parser.postfix,
			'Pass': real_infix == text_infix and real_postfix == parser.postfix,
		}

	# show the tests that failed in a table
	df = pd.DataFrame(data).T
	df = df[df['Pass'] == False]
	if df.empty:
		print(colored('All tests passed!', 'green'))
	else:
		print_table(df)


def print_table(df):
	# print the numebr of tests that failed in red
	print(colored(f'{len(df)} tests failed', 'red'))
	# print the table with the tests that failed with the item "Pass" in red
	df['Pass'] = df['Pass'].apply(lambda x: colored(x, 'red'))
	# put the color of the items that failed in red
	df['Pass_Infix'] = df['Pass_Infix'].apply(lambda x: colored(x, 'red') if x == False else x)
	df['Pass_Postfix'] = df['Pass_Postfix'].apply(lambda x: colored(x, 'red') if x == False else x)
	# put the color of the item that succeeded in green
	df['Pass_Infix'] = df['Pass_Infix'].apply(lambda x: colored(x, 'green') if x == True else x)
	df['Pass_Postfix'] = df['Pass_Postfix'].apply(lambda x: colored(x, 'green') if x == True else x)
	print(df[['Initial', 'Real_Infix', 'Test_Infix', 'Real_Postfix', 'Test_Postfix', 'Pass_Infix', 'Pass_Postfix', 'Pass']])


if __name__ == '__main__':
	test1()