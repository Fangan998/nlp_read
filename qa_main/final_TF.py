import jieba,json

fr = open('lexicon1_raw_nosil.txt','r',encoding='utf8') #字典
fw = open('new_lexicon1_raw_nosil.txt','w',encoding='utf8') #新字典(空白檔案)

for i in fr:
    i = i.split() #切分空白
    print(i[0],file = fw)

fw.close()
fr.close()

jieba.load_userdict('new_lexicon1_raw_nosil.txt') #寫入至新字典

f = open('Gossiping-QA-Dataset.txt','r',encoding='utf8') #讀QA檔
fw = open('new_Gossiping-QA-Dataset.txt','w',encoding='utf8')

for i in f:
    i = i[:-1].split('\t') #把每行的QA分開
    if len(i)==2: #確認陣列長度等於2
        i[0] = i[0].replace(" ","") #把空白取代掉
        i[1] = i[1].replace(" ","")
        #把斷好的詞用空格組好，利用tab(\t)把Q和A合起來寫入新的QA檔
        print(" ".join(jieba.cut(i[0])) + "\t" +" ".join(jieba.cut(i[1])),file = fw)

fw.close()
f.close()

res = []

fr = open('new_Gossiping-QA-Dataset.txt','r',encoding='utf8')
for index,questionAnswer in enumerate(fr): #索引值:index，元素內容:questionAnswer
    dict = {}
    i = questionAnswer.split('\t') #把Q和A中間的tab(\t)鍵切分開來
    dict['id'] = str(index) #[key:str(index)] >>> ['ID':'0','ID':'1',......]
    dict['question'] = i[0]
    dict['answer'] = i[1][:-1] #i[1][:-1] >>> [:-1]代表Answer每次讀到最後一個字都是換行(\n)，我們不需要換行

    dictModel = {}

    i[0] = i[0].split(" ") #切分Q的詞

    for j in i[0]:
        if j not in dictModel: #讀取每行Q，如果這個詞沒再dictModel裡就讓他等於1
            dictModel[j] = 1
        else:
            dictModel[j] += 1 #否則就+1

    for k,j in dictModel.items():
        dictModel[k] = round(j/len(i[0]),6) #每個value值(j)/每句的總詞數(i[0]),取小數點6位

    dict['model'] = dictModel #建好的Model存入陣列

    res.append(dict) #存入dict字典裡

with open('TF.json','w',encoding='utf8') as f:
    json.dump(res,f,ensure_ascii=False,indent=4)