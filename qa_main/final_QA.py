import jieba,json
try:
    with open('IDF.json','r',encoding='utf8') as fIDF:
        IDF = json.load(fIDF)
    with open('TF-IDF.json','r',encoding='utf8') as fTFIDF:
        TFIDF = json.load(fTFIDF)
    #將建好的字典載入jieba的詞庫中
    jieba.load_userdict('dec\\new_lexicon1_raw_nosil.txt')
except:
    print('末偵測到 idf.json,TF-IDF.json 和 new_lexicon1_raw_nosil.txt ')
    print('請執行前面的程式或修改路徑，謝謝')

while True:
    print('\nQA\n')
    query = input() #設一個query的變數為使用者輸入問題

    dict = {}
    #query進行jieba斷詞，再利用join將切好的詞用空白組成一句
    query = " ".join(jieba.cut(query))
    dict['question'] = query #將使用者問題存入dict的字典

    dictModel = {}
    q = query.split(' ') #切分使用者問題的詞
    for i in q:
        if i not in dictModel: #與計算tf模型一樣
            dictModel[i] = 1
        else:
            dictModel[i] += 1
    
    for k,v in dictModel.items():
        dictModel[k] = round(v/len(q),6)

    dict['model'] = dictModel #將每個切好的詞存入dictmodel中

    innerproduct = 0.0
    for k,v in dict['model'].items(): #將model中的每個key去判斷是否有在idf.json模型中
        #print(v*idf[k])
        if k in IDF: #要是存在將使用者tf值與idf相乘，不存在就忽略
            dict['model'][k] = round(v*IDF[k],6)
            #將每個相乘的值平方後相加存入innerproduct的變數中
            innerproduct += round(v*IDF[k],6)*round(v*IDF[k],6)
    
    dict['innerproduct'] = round(innerproduct ** 0.5 ,6)

    cosid = {}

    for tfidf in TFIDF: #讀取TFIDF的所有值
        compare = 0.0 #變動餘弦似定裡的值
        for k,v in dict['model'].items(): #逐一比對預先建好的tfidf模型中的model
            if k in tfidf['model']: #如果query中的詞在模型中，那就將兩個value相乘
                compare += tfidf['model'][k] * v #將整個query中每個詞相乘結果相加
            
        if compare > 0.0:
            #將相加結果除以tfidf與dict innerproduct值的相乘，結果為cos
            compare = round((compare/(tfidf['innerproduct']*dict['innerproduct'])),6)
            cosid[compare] = tfidf['id']

    cosid = sorted(cosid.items(),reverse=True) #將cosid這個字典針對它的key做逆向排序
    #print(cosid[:3]) [(0.908177,'366244'), (0.688402,'412946'), (0.668227,'48340')] 
    # >>> 你好 [相似度,ID]

    try:
        if query == q:
            break 
        else:    
            print(f'1.',TFIDF[int(cosid[0][1])]['question'])
            print(TFIDF[int(cosid[0][1])]['answer'],'\n')

            print('2.',TFIDF[int(cosid[1][1])]['question'])
            print(TFIDF[int(cosid[1][1])]['answer'],'\n')

            print('3.',TFIDF[int(cosid[2][1])]['question'])
            print(TFIDF[int(cosid[2][1])]['answer'])
            
    except:
        print('沒有這個問題')
