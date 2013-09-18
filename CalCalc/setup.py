from setuptools import setup

setup(
    name='CalCalc',
    author='Sonali Sharma',
    author_email='sonalisharma@berkeley.du',
    scripts=['CalCalc.py'],
    description='Provides answers to user queries provided on command line',
    long_description=open('README.txt').read(),
    install_requires = ['BeautifulSoup>=3.2.1'],
)