import json
with open('TF.json','r',encoding='utf8') as fTF:
    tf = json.load(fTF)
with open('IDF.json','r',encoding='utf8') as fIDF:
    idf = json.load(fIDF)

for i in tf: #讀取tf再逐一讀取裡面的內容並將變數設為1
    innerproduct = 0.0

    #針對i中model的key及value做計算，利用key去搜尋idf的值
    for k,v in i['model'].items():
        #TF*IDF
        i['model'][k] = round(v*idf[k],6)
        #將這個值平方後加到InnerProduct中
        innerproduct += round(v*idf[k],6)*round(v*idf[k],6)
    #將結果開根號並存入InnerProduct這個key值
    i['innerproduct'] = round(innerproduct ** 0.5 , 6)

with open('TF-IDF.json','w',encoding='utf8') as fTFIDF:
    json.dump(tf,fTFIDF,ensure_ascii=False,indent=4)