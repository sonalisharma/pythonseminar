import argparse
import BeautifulSoup
import urllib2

def calculate(userinput):
	try:
		print eval(userinput)
	except:
		print "Error in evaluating expression"


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Evaluating command line expressions')
	parser.add_argument('-s', action="store",help='Enter an expression to evaluate e.g. 3*4-5*6 or "mass of moon in kgs" , make sure the string is provided within quotes')
	try:
		results =  parser.parse_args()
		calculate(results.s)
	except:
		print "There is an error in your input, check help"
		parser.print_help()
