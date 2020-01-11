#!/usr/bin/env python
# coding: utf-8


import os
import yake
import xml.etree.ElementTree as ET
import pandas as pd


df = pd.read_csv(r'/home/anshul/Work/Citation_Dataset/ValenzuelaAnnotations.csv',encoding ='utf-8')
cd = pd.DataFrame({'Paper':df['Paper'],'Cited-by':df['Cited-by']})
del df


cited_src = r'/home/anshul/Work/Citation_Dataset/Cited-xml'
citing_src = r'/home/anshul/Work/Citation_Dataset/Citing-xml/citing'


similar_keywords = []

for i in range(len(cd)):
    cited_name = cd['Paper'][i] + '.tei.xml'
    cited_filepath = os.path.join(cited_src, cited_name)
    
    citing_name = cd['Cited-by'][i] + '.tei.xml'
    citing_filepath = os.path.join(citing_src, citing_name)
    
    #cited_XML information extraction code
    
    cited_tree = ET.parse(cited_filepath)
    cited_root = cited_tree.getroot()
    final_text = ""
    for x in cited_root[1][0]:
        cited_text = ""
        for body in x:
            if type(body.text) == str:
                cited_text = cited_text + body.text
        final_text = final_text + cited_text

    kw_extractor = yake.KeywordExtractor()
    cited_keywords = kw_extractor.extract_keywords(final_text)
    cited_keywords_final = []
    for i in cited_keywords:
        cited_keywords_final.append(i[1])

    #citing_XML information extraction code
    
    citing_tree = ET.parse(citing_filepath)
    citing_root = citing_tree.getroot()
    final_text = ""
    for x in citing_root[1][0]:
        citing_text = ""
        for body in x:
            if type(body.text) == str:
                citing_text = citing_text + body.text
        final_text = final_text + citing_text

    citing_keywords = kw_extractor.extract_keywords(final_text)
    citing_keywords_final = []
    for i in citing_keywords:
        citing_keywords_final.append(i[1])
    
    #print(len(set(cited_keywords_final) & set(citing_keywords_final)))
    similar_keywords.append(len(set(cited_keywords_final) & set(citing_keywords_final)))


#print(similar_keywords)

final_df = pd.DataFrame({'Cited':cd['Paper'],'Cited-by':cd['Cited-by'],'Score':similar_keywords})
del cd
final_df.to_csv(r'/home/anshul/Work/Citation_Dataset/results.csv', index= False, header = True)






