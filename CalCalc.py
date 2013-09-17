import argparse
import BeautifulSoup
import urllib2

def calculate(userinput,return_float=False):
	try:
		ans  = eval(userinput)
		return ans
	except:
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
	assert calculate("sin60 - sin0") == '50'
def test_4():
	assert calculate("total states in US") == '50'
def test_5():
	assert calculate("total states in US") == '50'

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Evaluating command line expressions')
	parser.add_argument('-s', action="store",help='Enter an expression to evaluate e.g. 3*4-5*6 or "mass of moon in kgs" , make sure the string is provided within quotes')
	try:
		results =  parser.parse_args()
		ans = calculate(results.s,return_float=True)
		print "You Asked: %s"  %results.s
		print "Answer: %s" %ans
	except:
		print "There is an error in your input, check help below"
		parser.print_help()
