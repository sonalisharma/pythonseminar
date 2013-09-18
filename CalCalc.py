import argparse
import BeautifulSoup
import urllib2
import re

def calculate(userinput,return_float=False):
	"""
	This methos is used to read the user input and provide and answer. The answer is computed dircetly
	using eval method if its a numerical expression, if not the wolfram api is used to get the appropriate answer.

	Parameters:
	userinput : This is a string, passed by the user in command line
				e.g. "3*4+12" or "mass of moon in kgs"
	return_float: This is to provide the output format, when specified as true then float is returned

	Execution:
	calculate("3*4+12", return_float=True)

	Output:
	The result is either a float or a string

	"""
	try:
		#This is to make sure user does not provide remve, delete or other sys commands in eval
		#eval is used purely for numeric calculations here.
		if (bool(re.match('.*[a-zA-Z].*', userinput, re.IGNORECASE))):
			raise Exception ("Try with wolfram")
		else:
			ans  = eval(userinput)
			if return_float:
				ans = float(re.findall(r'\d+', ans))
			return ans 
	except Exception:
		data = urllib2.urlopen('http://api.wolframalpha.com/v2/query?appid=UAGAWR-3X6Y8W777Q&input='+userinput.replace(" ","%20")+'&format=plaintext').read()
        soup = BeautifulSoup.BeautifulSoup(data)
        keys = soup.findAll('plaintext')
        if (keys):
        	#Printing the first returned rresult of the query. The first result is the heading, second
        	#result is the actual value hence printing [1:2]
        	for k in keys[1:2]:
        		ans = k.text
        else:
        	ans = "Sorry! No results found, try another question!"
        return ans
def test_1():
	assert abs(4.0 - calculate("2**2")) < 0.001
def test_2():
	assert calculate("total states in US") == '50'
def test_3():
	assert calculate("56*3+1000%2") == '168'
def test_4():
	assert 'Alaska' in calculate("largest state in US")
def test_5():
	assert '8' in calculate("planets in our solar system")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Evaluating command line expressions')
	parser.add_argument('-s', action="store",help='Enter an expression to evaluate e.g. 3*4-5*6 or "mass of moon in kgs" , make sure the string is provided within quotes')
	try:
		results =  parser.parse_args()
		ans = calculate(results.s,return_float=True)
		if ans=="":
			ans="Sorry! No results found, try another question!"
		print "You Asked: %s" %results.s
		print "Answer: %s" %ans
	except:
		print "There is an error in your input, check help below"
		parser.print_help()
