import os
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style 
import numpy as np
import seaborn as sns


def womtable():
    df = None
    hm = None
    plt.clf()
    df = pd.read_csv("../binaryx_bot/wom.csv",names=['Hora', 'Lv1', 'Lv2', 'Lv3', 'Lv4', 'Lv5', 'Lv6'])
    df['Hora'] = df['Hora'].astype('datetime64[ns]')
    df['Hora'] = df['Hora'].dt.floor('Min')
    df['Time'] = df['Hora'].dt.tz_localize("GMT").dt.tz_convert('America/Sao_Paulo')
    hm=df.groupby(df["Hora"].dt.hour)[["Lv1","Lv2","Lv3","Lv4","Lv5","Lv6"]].mean()
    sns.heatmap(hm.div(2.5),cmap='RdYlGn', linewidths=0.5, annot=True).set(title='Média de WOM por hora \n De '+df['Hora'].min().strftime('%Y-%m-%d %r')+ ' às '+df['Hora'].max().strftime('%Y-%m-%d %r'))
    plt.xlabel('Nível', fontsize = 12) # x-axis label with fontsize 15
    plt.ylabel('Hora (Brasil)', fontsize = 12) # y-axis label with fontsize 15
    plt.show()
    plt.savefig('table.png')
    
    return