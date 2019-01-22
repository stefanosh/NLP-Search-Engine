import argparse

#Read one or more words from the command line 
parser = argparse.ArgumentParser(description='Quering the database')
parser.add_argument('words', metavar='word_name', type=str, nargs='+',
                    help='The word with which you make a search request. You can add multiple words with space between.')

args = parser.parse_args()
print(args)
