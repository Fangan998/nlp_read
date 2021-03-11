dict_word = {}
f = open('dec/單字詞_13053(注音_無聲調).dic','r',encoding='utf-8')

for i in f.readlines():
    temp = i.strip().split(',')
    if len(temp)>=2:
        dict_word[temp[0]]= temp[1]   
f.close()

num_of_phonemes=0
dict_phoneme={}

f01=open('test_data/Gossiping-QA-Dataset.txt','r',encoding='utf-8')
for line in f01:
    for w in line:
        if w in dict_word:
            syllable = dict_word[w]
            for subsyllable in syllable:
                if subsyllable in dict_phoneme:
                    dict_phoneme[subsyllable] = dict_phoneme[subsyllable] + 1
                else:
                    dict_phoneme[subsyllable] = 1
f01.close()

print(sorted(dict_phoneme.items(),key=lambda x:x[1]))