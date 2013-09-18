from distutils.core import setup

setup(
    name='CalCalc',
    version='0.1.0',
    author='Sonali Sharma',
    author_email='sonalisharma@berkeley.du',
    packages=['CalCalc'],
    scripts=['CalCalc.py'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Provides answers to user queries provided on command line',
    long_description=open('README.txt').read(),
    install_requires=[
        "BeautifulSoup >= 3.2.1"
    ],
)