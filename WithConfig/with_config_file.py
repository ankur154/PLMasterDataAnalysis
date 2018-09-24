import nltk
from nltk.corpus import state_union
from nltk.tokenize import sent_tokenize, word_tokenize
import pandas as pd
from gensim.models import word2vec
# from pattern.en import spelling
# from pattern.en import suggest
import re
import csv
from nltk.corpus import stopwords


def get_catagory():
    cat_dic = {}
    cat_dic['SPEC_NUMBER'] = ['SPEC.NO', 'SPECN', 'SPEC NO.', 'SPECIFICATION NO', 'SPECN . NO.']
    cat_dic['SK_NUMBER'] = ['SK NO', 'SK. NO.', 'SK', 'SKETCH NO', 'SKETCH']
    cat_dic['AMENDMENT_NO'] = ['AMD','AMENDMENT','AMENDMENT NO','AMENDMENT NO.','AMD.','AMENDMENT NUMBER','AMD NO','AMD.NO.','AMD NO.','AMD. NUMBER','AMD NUMBER']
    cat_dic['DRG._NUMBER'] = ['DRG.NO.','DRG','DRG.','DRG NO.','DRG NO','DRG NO.', 'DRAWING NUMBER', 'DRAWING NO', 'DRAWING NO.']
    cat_dic['QUANTITY'] = ['QTY', 'QUANTITY', 'AMOUMT']
    cat_dic['ITEM_NUMBER'] = ['ITEM', 'ITMNO', 'ITEM NO', 'ITEM NO.', 'ITEM NUMBER', 'ITM NO']
    cat_dic['ALT_NUMBER'] = ['ALT', 'ALT NO.', 'ALT NO', 'ALT NUMBER', 'ALT.NO.', 'ALTNO', 'ALT NO.','ALT.']
    cat_dic['REV_NUMBER'] = ['REV', 'REV NO', 'REV NUMBER', 'REV. NO.', 'REV.NO.']
    cat_dic['DRAWING_ATTACHED'] = ['DRAW', 'DRAWING', 'DRW','DRAW ATTACHED','DRAWING ATTACHED', 'DRAW ATT']
    cat_dic['OTHER_SPECIFICATION'] = ['OTH SPEC','OTHER SPECIFICATION','OTHER SPEC', 'SPECIFICATION', 'SPEC']
    cat_dic['REST_DATA'] = ['REST', 'LEFT', 'UNPROCESSED','UNCATAGORISE']
    
    con_file = pd.read_csv('configuration.csv')
    headings = con_file['COLUMN_NAME']

    colname=[]
    for heading in headings:
        in_col = heading.strip()
        for keys in cat_dic:
            for li_val in cat_dic[keys]:
                if in_col == li_val:
                    colname.append(keys)
    #print colname
    return colname
            


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
    
def meaning(word):
    li=[]
    syns = wordnet.synsets(word)
    for i in syns:
        val = i.lemma_names()[1:]
        for j in val:
            li.append(str(j))
    return li

def reduce_length(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)

def word_catagory_gra(s,typ):
    li=[]
    w = word_tokenize(s)
    d=pos_tag(w)
    for i in d:
        if i[1]==typ:
            li.append(i[0])
    return li

def word_catagory_san(s):
    st = NERTagger('trained_data/classifiers/english.all.3class.distsim.crf.ser.gz', 'trained_data/stanford-ner.jar')
    for sent in sent_tokenize(s):
        tokens = word_tokenize(sent)
        tags = st.tag(tokens)
        for tag in tags:
            print tag

def other_spec(rest_str3):
    wli = word_tokenize(rest_str3)
    list_tuple=[]
    rest_str3 = ''
    var_li=[]
    for i in range(len(wli)):
        if wli[i].isdigit():
            list_tuple.append((wli[i-1], wli[i]))
            var_li.append(wli[i-1])
            var_li.append(wli[i])
        elif not wli[i].isdigit() and not wli[i].isalpha():
            templ = re.findall(r"[-+]?\d*\.\d+|\d+", wli[i])
            for j in templ:
                list_tuple.append((wli[i-1],j))
            var_li.append(wli[i-1])
            var_li.append(wli[i])

    var_li = set(var_li)
    var_li = list(var_li)
    for i in var_li:
        wli.pop(wli.index(i))
    
    for i in wli:
        rest_str3 += i + ' '
    spec_str = ''
    
    if len(list_tuple):
        for rel in list_tuple:
            spec_str += rel[0]+' '+rel[1]+' '

    return rest_str3, spec_str

def draw_att(descrip):
    if 'drawing' in descrip.lower():
        dic['DRAWING_ATTACHED'] = 'Yes'
    else:
        dic['DRAWING_ATTACHED'] = 'No'

def sk_no(descrip):
    des_low = descrip.lower()
    if 'sk' in des_low:
        val = des_low.index('sk')
        rest_str1 = descrip[:val]
        new_str=''
        alert=0
        while True:
            if alert==1 and des_low[val].isalpha():
                break
            new_str += descrip[val]
            val += 1
            try:
                if des_low[val].isdigit():
                    alert=1
            except:
                break
        rest_str1 += descrip[val:]
    else:
        new_str=''
        rest_str1 = descrip[:]
    dic['SK_NUMBER'] = new_str
    return rest_str1

def drg_no(rest_str1):
    des_low = rest_str1.lower()
    if 'drg' in des_low:
        val = des_low.index('drg')
        rest_str1 = descrip[:val]
        new_str=''
        alert=0
        while True:
            if alert==1 and des_low[val].isalpha():
                break
            new_str += descrip[val]
            val += 1
            try:
                if des_low[val].isdigit():
                    alert=1
            except:
                break
        rest_str1 += descrip[val:]
    else:
        new_str=''
    dic['DRG._NUMBER'] = new_str
    return rest_str1

def amd_no(rest_str1):
    des_low = rest_str1.lower()
    if 'amend' in des_low:
        val = des_low.index('amend')
        rest_str4 = rest_str1[:val]
        new_str=''
        alert=0
        while True:
            if alert==1 and des_low[val].isalpha():
                break
            new_str += rest_str1[val]
            val += 1
            try:
                if des_low[val].isdigit():
                    alert=1
            except:
                break
        rest_str4 += rest_str1[val:]
        rest_str1=rest_str4[:]
    elif 'amd' in des_low:
        val = des_low.index('amd')
        rest_str4 = rest_str1[:val]
        new_str=''
        alert=0
        while True:
            if alert==1 and des_low[val].isalpha():
                break
            new_str += rest_str1[val]
            val += 1
            try:
                if des_low[val].isdigit():
                    alert=1
            except:
                break
        rest_str4 += rest_str1[val:]
        rest_str1=rest_str4[:]
    else:
        new_str=''
    dic['AMENDMENT_NO'] = new_str
    return rest_str1

def quantity(rest_str1):
    des_low = rest_str1.lower()
    if 'qty' in des_low:
        val = des_low.index('qty')
        rest_str4 = rest_str1[:val]
        new_str=''
        alert=0
        while True:
            if alert==1 and des_low[val].isalpha():
                break
            new_str += rest_str1[val]
            val += 1
            try:
                if des_low[val].isdigit():
                    alert=1
            except:
                break
        rest_str4 += rest_str1[val:]
        rest_str1=rest_str4[:]
    else:
        new_str=''
    dic['QUANTITY'] = new_str
    return rest_str1

def rev_no(rest_str1):
    des_low = rest_str1.lower()
    if 'rev' in des_low:
            val = des_low.index('rev')
            if des_low[val+3] != 'i' and des_low[val+3] != 'a' and des_low[val+3] != 'e':
                rest_str4 = rest_str1[:val]
                new_str=''
                alert=0
                while True:
                    if alert==1 and des_low[val].isalpha():
                        break
                    new_str += rest_str1[val]
                    val += 1
                    try:
                        if des_low[val].isdigit():
                            alert=1
                    except:
                        break
                rest_str4 += rest_str1[val:]
                rest_str1=rest_str4[:]
            else:
                new_str=''
    else:
        new_str=''
    dic['REV_NUMBER'] = new_str
    return rest_str1

def spec_no(des_low):
    wt = word_tokenize(des_low.lower())
    wt_org = word_tokenize(des_low)
    
    spec_no=''
    word_flag=0
    rest_str1=''
    for k in range(len(wt)):
        if wt[k].startswith('specn'):
            spec_no += wt_org[k] + ' '
            word_flag=1
            continue
        elif word_flag == 0:
            rest_str1 += wt_org[k]+ ' '
            
        if word_flag==1:
            if bool(re.search('\d', wt[k])):
                spec_no += wt_org[k] +' '
                break
            else:
                rest_str1 += wt_org[k] + ' '                   
    dic['SPEC_NUMBER'] = spec_no
    return rest_str1

def item_no(rest_str1):
    des_low = rest_str1.lower()
    if 'item n' in des_low:
        val = des_low.index('item n')
        rest_str2 = rest_str1[:val]
        new_str=''
        alert=0
        while True:
            if alert==1 and des_low[val].isalpha():
                break
            new_str += rest_str1[val]
            val += 1
            try:
                if des_low[val].isdigit():
                    alert=1
            except:
                break
        rest_str2 += rest_str1[val:]
    else:
        new_str=''
        rest_str2 = rest_str1[:]
    dic['ITEM_NUMBER'] = new_str
    return  rest_str2

def alt_no(rest_str2):
    des_low = rest_str2.lower()
    if 'alt' in des_low:
        val = des_low.index('alt')
        rest_str3 = rest_str2[:val]
        new_str=''
        alert=0
        while True:
            if alert==1 and des_low[val].isalpha():
                break
            new_str += rest_str2[val]
            val += 1
            try:
                if des_low[val].isdigit():
                    alert=1
            except:
                break
        rest_str3 += rest_str2[val:]
    else:
        new_str=''
        rest_str3 = rest_str2[:]
    dic['ALT_NUMBER'] = new_str
    return rest_str3


units=['m', 'mm', 'cm', 'dm', 'km', 'AE', 'lj', 'pc', '"', 'in', 'ft', 'yd', 'mi', 'sqm', 'sqcm']        
# Reading data file 
filename = "3098.csv"                    
in_file = pd.read_csv(filename)

#  Get DESCRIPTION coloumn from data file
descriptions = in_file['DESCRIPTION']         

stop_words = set(stopwords.words('english'))
pun_words = set(['.' , '?' , '/' , ',' , '!', ':', ';', '-', '_'])

dic={}
#Parsing description string one by one
with open('Processed_data.csv','a') as f:
    fieldnames = get_catagory()
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for description in descriptions:
        word_tokens = word_tokenize(description)
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentence = [w for w in filtered_sentence if not w in pun_words]
        filtered_sentence = [w for w in filtered_sentence if not w in units]
        descrip = ''
        for z in filtered_sentence:
            descrip += z+' '

        if 'DRAWING_ATTACHED' in fieldnames:   
            draw_att(descrip)
        if 'SK_NUMBER' in fieldnames:
            descrip = sk_no(descrip)
        if 'DRG._NUMBER' in fieldnames:
            descrip = drg_no(descrip)
        if 'AMENDMENT_NO' in fieldnames:
            descrip = amd_no(descrip)
        if 'QUANTITY' in fieldnames:
            descrip = quantity(descrip)
        if 'REV_NUMBER' in fieldnames:
            descrip = rev_no(descrip)
        if 'SPEC_NUMBER' in fieldnames:
            descrip = spec_no(descrip)
        if 'ITEM_NUMBER' in fieldnames:
            descrip = item_no(descrip)
        if 'ALT_NUMBER' in fieldnames:
            descrip = alt_no(descrip)
        if 'OTHER_SPECIFICATION' in fieldnames:
            rest_str, spec_str =  other_spec(descrip)
            dic['OTHER_SPECIFICATION'] = spec_str
        if 'REST_DATA' in fieldnames:
            dic['REST_DATA'] = rest_str
        
        writer.writerow(dic)

    
