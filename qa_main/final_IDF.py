import json , math
count = 0 #總共有多少個Q
f = open('new_Gossiping-QA-Dataset.txt','r',encoding='utf8')
dict = {}
for words in f:
    count += 1 #讀完每個文件後讓count+1
    w = words.split('\t') #把Q和A中間的tab(\t)鍵切分開來
    words = w[0].split(" ") #取Q用空白切分
    res = {}
    for j in words:
        if j not in res: #如果這個詞沒再字典裡就讓它等於1，有就忽略
            res[j] = 1

    for k,v in res.items():
        if k in dict.keys(): #計算詞總共出現幾次
            dict[k] += v #每個文件不管出現幾次，只要出現皆為1，都是+1
        else:
            dict[k] = v
    
for k,v in dict.items():
    n = count/v #n = count(文件的數量:40多萬筆question)/v(該詞出現在所有文件的數量)
    dict[k] = math.log((n),10) #以10為底，取log，存回dict陣列裡

with open('IDF.json','w',encoding='utf8') as f:
    json.dump(dict,f,ensure_ascii=False,indent=4)