import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import re
import random
import requests
from bs4 import BeautifulSoup

import cv2 #!pip install opencv-python
from wordcloud import WordCloud #!pip install wordcloud
import nltk #!pip install nltk
from nltk import FreqDist
nltk.download('stopwords')  # run this if you get any error
stpwrd = set(nltk.corpus.stopwords.words('english'))


### 
image = cv2.imread("C:/Users/Admin/Desktop/china.jpg") 
PersonImage = image
 
# word cloud
def Word_cloud(data, title, mask=None):
    font_path = "C:/Users/Admin/Desktop/STFangSong.ttf"
    Cloud = WordCloud(scale=3,
                      random_state=21,
                      colormap='autumn',
                      mask=mask,
                      stopwords=stpwrd,
                      collocations=True,
                     font_path=font_path).generate(data)
    plt.figure(figsize=(20,12))
    Cloud.to_file(str(title)+'.png')  #uncomment this if you want to download it
    plt.imshow(Cloud)
    plt.axis('off')
    plt.title(title)
    plt.show()
    return Cloud

### read csv file: index, title1, page_url, title2, first_paragraph
def read_csv_files(year, month_list):    
    df = []
    for m in month_list:
        file_name = str(year) + m + ".csv"
        tmp = pd.read_csv("C:/Users/Admin/Desktop/FA_data/" + file_name, index_col=0)
        df.append(tmp)
    return df

def search_keyword(df_data, feature, kws):
    filter_list = []
    tmp_data = df_data.copy()
    col_list = list(tmp_data[feature])
    i = 0
    while i<len(col_list):
        fg = False
        for kw in kws:
            if kw.lower() in col_list[i].lower():
                fg = True
        filter_list.append(fg)
        i += 1
    return tmp_data[ filter_list ]

def tokenize01(st):
    # if it is date, return
    if len(st)==10 and st[4]=="-" and st[7]=="-" and int(st[5:7])<=12 and int(st[8:10])<=31:
        return [st]
    if 'https:' == st:
        return []
    if 'www.foreignaffairs.com' == st:
        return []
    return [st] #st.split("-")

def analyze_URL(year, month_list):
    df = read_csv_files(year, month_list)
    url_list = []
    for it in df:
        feature = "page_url"
        url_list = url_list + list( it[feature] )
    print( len(url_list) )
    len_dic = {}
    word_dic = {}
    select_text = ""
    for link in url_list[:]:
        its = link.split("/")
        L = len(its)
        if L not in len_dic:
            len_dic[L]=1
        else:
            len_dic[L]+=1
        for it in its:
            for w in tokenize01(it):
                if w not in word_dic:
                    word_dic[w] = 1
                else:
                    word_dic[w] += 1
                select_text = select_text + " " + w
    print(len_dic)
    """
    wf = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)
    top_N = 30
    i = 0
    while i<top_N:
        print(wf[i])
        i += 1
    """
    #search_t = "Word Cloud for links "  + str(year)
    #wc = Word_cloud(select_text, search_t, mask=PersonImage)
    return 

def analyze_content(year, month_list):
    df = read_csv_files(year, month_list)
    content_list = []
    for it in df:
        it = it[ it['page_url'].str.contains('china') ]
        feature = "first_paragraph"
        content_list = content_list + list( it[feature] )
    print( len(content_list) )
    select_text = ""
    for it in content_list:
        select_text = select_text + "\n " + it
    #
    search_t = "Word Cloud for content "  + str(year)
    wc = Word_cloud(select_text, search_t, mask=PersonImage)
    return 


month_list = ['_January_February', '_March_April', '_May_June', '_July_August', '_September_October', '_November_December']

year = 2022
for year in range(2022, 2023): # 2009, 2023
    #analyze_URL(year, month_list)
    analyze_content(year, month_list)

    df = read_csv_files(year, month_list)
    whole_counter = 0
    counter = 0
    i = 0
    while i<len(df):
        tmp_df = df[i]
        #print( year, month_list[i], "\t\t", len(tmp_df) )
        whole_counter += len(tmp_df)
        feature = "page_url"
        kws = ["China", "Chinese", "Beijing", "Xi Jinping"]
        tmp_data = search_keyword(tmp_df, feature, kws)
        #print(tmp_data[feature])
        counter = counter + len(tmp_data)
        i += 1
    ratio = round(counter*100/whole_counter, 2)
    print( year, "\t", counter, "\t", whole_counter, "\t", ratio, "%" )
    
