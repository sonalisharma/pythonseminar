import argparse
def calculate(userinput):
	print "Testing command line argument"

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Evaluating command line expressions',
									 help='Enter an expression to evaluate e.g. 3*4-5*6 or mass of moon in kgs')
	parser.add_argument('-s', action="store")
	results =  parser.parse_args()
	calculate()
