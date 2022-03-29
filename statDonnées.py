#!/usr/bin/env python
# coding: utf-8

# In[292]:


import seaborn as sns
from PIL import Image
import numpy as np 
from numpy import cov
import statistics 
import math
import os
from pathlib import Path
import openpyxl
import pandas as pd
from matplotlib import pyplot as plt 
import datetime

file = pd.read_excel(os.path.join(os.getcwd(), 'Downloads', 'Sentinel.xlsx'),index_col=0 ,engine='openpyxl') 
stdevlog=[]
for x in b:
   stdevlog.append(np.abs(math.log(x,10)))

file['logStDev']=stdevlog
file[['C0/max','C0/min','C0/stDev','C0/mean','logStDev']].plot(figsize=(12,12))
plt.title("statictics of NDVI for these 5 years ago  ")
plt.legend(["NDVI max","NDVI min","NDVI stDev","NDVI mean","NDVI logStdev"])
plt.xlabel("Dates")
plt.ylabel("NDVI")
plt.show()

a =file['C0/min'].tolist()
b=file['C0/stDev'].tolist()
c=file['C0/mean'].tolist()
d=file['C0/max'].tolist()


file[['C0/max','C0/min','C0/stDev','C0/mean']].plot.hist(by=file.index.year)

CORRELATION:
comparaison 
Correlation et regression linear
# In[268]:



corrMatrix = file[['C0/max','C0/min','C0/stDev','C0/mean']].corr()
sns.heatmap(corrMatrix, annot=True)
plt.show()


# In[170]:


import seaborn as sns
sns.pairplot(file[['C0/min','C0/max','C0/mean','C0/stDev']])


# In[ ]:





# In[265]:


#Filtration DES SIGNAUX 
#etape 1
from scipy import fftpack
from scipy import signal

new_ndvi=signal.detrend(d)
plt.plot(date,d)
plt.plot(date,new_ndvi)
plt.show()
#filtrer les signal trans de Fourier 
monFourier=fftpack.fft(new_ndvi)
valeurabs=np.abs(monFourier)
mesFrequences=fftpack.fftfreq(len(new_ndvi))
plt.plot(np.abs(mesFrequences),valeurabs)
plt.show()

monFourier[valeurabs<6.3]=0
plt.plot(np.abs(mesFrequences),np.abs(monFourier))
plt.show()


# In[ ]





# In[266]:


#fonction de fourier inverse
from scipy import fftpack
from scipy import signal
monfiltre=fftpack.ifft(monFourier)
plt.figure(figsize=(12,8))
plt.plot(date,c,lw=1)
plt.plot(date,monfiltre,lw=3)
plt.show()


# In[ ]:





# # saisonnalité / Séries temporelles

# In[222]:


import matplotlib as mpl
def seasonal_thing(file: pd.DataFrame, column: str) -> None:
    file['year'] = [d.year for d in file.index]
    file['month'] = [d.strftime('%b') for d in file.index]
    years = file['year'].unique()
#print(years)
    file = file.drop_duplicates(subset=['month','year'])
    file = file.sort_values(by="C0/date")

    np.random.seed(100)
    mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(years), replace=False)

    plt.figure(figsize=(12,6), dpi= 80)

    for i, y in enumerate(years):
        if i > 0:
       # print(file.loc[file.year == y])
            plt.plot('month', column, data=file.loc[file.year == y], color=mycolors[i], label=y)
            plt.text(file.loc[file.year==y].shape[0]-.9, file.loc[file.year==y, column][-1:].values[0], y, fontsize=12, color=mycolors[i])

# Decoration
    plt.gca().set(xlim=(-0.3, 11), ylim=(-0.005, 0.8), ylabel=f'${column}$', xlabel='$Month$')
    plt.yticks(fontsize=12, alpha=.7)
    plt.title(f"Seasonality of {column} Time Series", fontsize=20)
    plt.show()
    




# In[215]:


seasonal_thing(file,'C0/max')


# In[214]:


seasonal_thing(file,'C0/min')


# In[216]:


seasonal_thing(file,'C0/stDev')


# In[219]:



seasonal_thing(file,'C0/mean')   


# In[291]:


from statsmodels.tsa.stattools import acf
cor = acf(file['C0/mean'],fft=False)
fig, ax = plt.subplots(1, 1, figsize=(14,2))
ax.plot(cor)
ax.set_title("Autocorrélogramme")


# In[ ]:





# In[ ]:





# In[ ]:




