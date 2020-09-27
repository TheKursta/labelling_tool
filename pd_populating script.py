# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import os

root_dir = "C:\\Users\\klavs\\Desktop\\"

df_list = []
for filename in os.listdir(root_dir):
    if filename.endswith(".txt"):    
        file = open(os.path.join(root_dir,filename),"r")
        line = file.readlines()[0]
        line = line.rstrip()
        att = line.split("\t")
        panda_attributes = {"name":filename[-3],"start":att[0],"stop":att[1],"peak":att[2],"non_correl":att[3],"abnormal_limb":att[4],"low_occ":att[5],"heavy_occl":att[6],"other":att[7]}
        df = pd.DataFrame(panda_attributes, index = [0])
        df_list.append(df)
        
#concat dfs
df = pd.concat(df_list).reset_index(drop = True)
df.to_json(os.path.join(root_dir,"concat_df.json"),index = True)
