import pandas as pd
import json

con_file1 = pd.read_csv('catagory.csv')

cl_names =  con_file1.columns
cat_dic = {}
for cl_name in cl_names:
    new_col = cl_name.replace(" ","_").upper()
    cat_list = []
    col_data = con_file1[cl_name]
    for j in col_data:
        if str(j)!='nan':
            cat_list.append(str(j).strip().upper())
    cat_dic[new_col] = cat_list

var = json.dumps(cat_dic)
with open('dynamic.json','wb') as f:
    f.write(var)
