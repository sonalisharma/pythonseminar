# Import relevant modules
import pymc
import numpy as np
import pandas as pd
data = pd.read_csv('hw_11_data/laa_2011_april.csv',sep='\t')

# Priors on unknown parameters
alpha = pymc.Normal('alpha',mu=0.255,tau=1/float(0.0011))
beta = pymc.Normal('beta',mu=1-0.255,tau=1/float(0.0011))
mus = dict()
xs = dict()

# model
@pymc.deterministic(plot=False)
def playeravg(a=alpha, b=beta):
    return pymc.Beta('avg',a,b)

for i in range(len(data)):
    mus['mu'+ str(i)] = playeravg
    xs['x' + str(i)] = pymc.Binomial('x' + str(i),n=data.AB[i], p=playeravg, value=data.H[i])  