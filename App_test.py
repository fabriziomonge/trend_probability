#!/usr/bin/env python
# coding: utf-8

# In[7]:


import streamlit as st
import pandas as pd
import numpy as np
from pycaret.classification import *
import pandas_datareader as pdr


# In[3]:


#controllo accessi

url = 'http://www.sphereresearch.net/Notebooks/Accessi.xlsx'
accessi = pd.read_excel(url)
accessi = accessi.set_index('User', drop = True)

# In[4]:


Utente = st.text_input("Inserire il nome utente")
Psw = st.text_input("Inserire la password", type='password')


# In[12]:


try:

    if Psw == accessi['Password'][Utente]:

        ticker = st.text_input("Inserire il ticker da analizzare", "VTI")


        st.sidebar.markdown("""Nel caso in cui la somma delle opzioni non sia pari a 100 il programma ribasa il portafoglio al 100% in proporzione ai dati inseriti""") 
    
    else:
        st.write("""
           In caso di utilizzo senza credenziali non sarà possibile modificare i pesi delle asset in portafoglio.
    """)
        ticker = ("VTI")
except:
    
    st.write("""
       In caso di utilizzo senza credenziali non sarà possibile modificare i pesi delle asset in portafoglio.
    """)
    ticker = ("VTI")


# In[25]:


df = pdr.get_data_yahoo(ticker, start = '2000-1-1')['Close']
df = df.resample('M').last()
df = pd.DataFrame(df)
df['index']= df.index
df = df.set_index('index', drop=True)


# In[21]:


# df


# In[26]:


st.write("""
   """)
st.write("""
## Andamento del titolo selezionato:
 """, ticker)
st.line_chart(df)
# df.plot() #rimuovere in fase di committment


# In[28]:


#creiamo le features
for i in range (1,15):
    nome = "Roc"+str(i)
    df[nome] = df.Close/df.Close.shift(i)


# In[38]:


#crea il target

df['diff'] = df.Close.shift(-1)-df.Close.shift(4)
df['diff'] = df['diff'].fillna(-1)
df
df.loc[df['diff']>=0, 'risk']="NO"
df.loc[df['diff']<0, 'risk']="SI"
df = df.drop('diff',1)


# In[39]:


df


# In[41]:


exp_clf101 = setup(data = df, target = 'risk', feature_selection=False, ignore_features = ['Close'], session_id=123, silent=True)


# In[ ]:




