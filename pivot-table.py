# -*- coding: utf-8 -*-
"""
Created on Mon May 16 22:34:32 2016

@author: Jay
"""
import pandas as pd

AIRPORTS_FILENAME = "airports.dat"


ROUTES_FILENAME = "routes.dat"
ROUTES_NEW = "routes_new.csv"

LINE_SEPARATOR = ","

def pivot_table():
    f = open(ROUTES_FILENAME)
    text = f.read()
    f.close()
    f = open(ROUTES_NEW, 'w')
    f.write('Airline,Airline ID,Source Airport,Source Airport ID, Destination airport,Destination airport ID,Codeshare,Stops,Equipment\n')    
    f.write(text)
    f.close()
    
    df = pd.read_csv(ROUTES_NEW)
    print pd.pivot_table(df,index=["Airline"])


pivot_table()  

