# Import relevant modules
import pymc
import numpy as np
import pandas as pd
data = pd.read_csv('hw_11_data/laa_2011_april.csv',sep='\t')

# Priors on unknown parameters
alpha = pymc.Normal('alpha',mu=0.255,tau=1/float(0.0011))
beta = pymc.Normal('beta',mu=1-0.255,tau=1/float(0.0011))

avg = pymc.Beta('avg', alpha=alpha, beta=beta, size=len(data))
#def playeravg(a=alpha, b=beta):
#    return pymc.Beta('avg',a,b, size=len(data))

#mus['mu'+ str(i)] = playeravg
xi = pymc.Binomial('xi',n=data.AB, p=avg, value=data.H)  