import time

def gg():
    file=open('dec/lexicon1_raw_nosil.txt','r',encoding='utf-8')
    wifl=open('dec/cut_raw_nosil.txt','w',encoding='utf-8')
    
    for i in file.readlines():
        temp = i.strip().split()
        wifl.write(f'{temp[0]}\n')
        
    file.close()
    wifl.close()
    
    #以前的def listf()，已經整合至此
    rdfl=open('dec/cut_raw_nosil.txt','r',encoding='utf-8')
    j=[]
    for i in rdfl.readlines():
        temp = i.strip().split()
        j.append(temp[0])  
    rdfl.close()
    return j

def positive_match(text, dict_word):  # text => 一段文字
    global longest_term
    #正向最長匹配  
    start = 0  #要尋找的字首
    while start < len(text):    #使用類似反向雙指標的方法
        if start + longest_term - 1 >= len(text):
            end = len(text) - 1
            #print("a")
        else:
            end = start + longest_term - 1
            #print("b")
        while end >= start:
            #print("c")
            word = text[start:end + 1]
            if word in dict_word:
                
                #test => 
                #print(word)
                
                if word in T:
                    T[word] = T[word] +1
                else:
                    T[word] = 1 #更新儲存分詞結果的字典
                    
                #result_set.add(word)   #更新儲存分詞結果的集合
                
                start += len(word)
                break
            end -= 1 
            if end < start:  #完全找不到可匹配的詞  代表是標點符號或是字母
                start += 1      


def negative_match(text, dict_word):
    #反向最長匹配  
    end = len(text) - 1
    while end >= 0:    
        if end - longest_term + 1 < 0:
            start = 0
        else:
            start = end - longest_term + 1
        while start <= end:  
            word = text[start:end + 1]
            if word in dict_word:
                #test => print(word)
                if word in T:
                    T[word] = T[word] +1
                else:
                    T[word] = 1 #更新儲存分詞結果的字典
                    
                #result_set.add(word)
                end -= len(word)
                break
            start += 1 
            if start > end:
                end -= 1       

def prf(gold,pred) -> tuple:
    A_size,B_size,A_cap_B_size = 0,0,0
    
    #集合
    A,B = set(gold),set(pred)
            
    #正解
    A_size += len(A)
    global All_size
    All_size = All_size + A_size
    #print(A_size)
            
    #預測
    B_size += len(B)
    global Bll_size
    Bll_size = Bll_size + B_size
    #print(B_size)
            
    #重合部分
    A_cap_B_size += len(A & B)
    global All_cap_B_size
    All_cap_B_size = All_cap_B_size + A_cap_B_size
    #print(A_cap_B_size)
        
#start cout time
start = time.time()

longest_term = 0

All_cap_B_size = 0
Bll_size = 0
All_size = 0

dict_word = {}
with open("dec/lexicon1_raw_nosil.txt", encoding="utf8") as file:
    line = file.readline()
    while line:
        line_list = line.split()
        dict_word.update({line_list[0] : 0})   #詞語 : 出現次數
        if len(line_list[0]) > longest_term:
            longest_term = len(line_list[0])
        line = file.readline()

T = {}
   
declist = []
declist = gg()
        
text = open('test_data/GigaWord_text_lm.txt','r',encoding='utf-8')

a=[]

s_list = []

def ha(a:list()):
    c = a
    t = ""
    for i in range(len(c)):
        t += c[i]
    return t

Rt = 0

for j in text.readlines():
    Rt += 1
    c =  j.strip().split()
    t = ""
    t = ha(c)    
    a = negative_match(t,dict_word)#正向為positive_match,反向為negative_match
    
    print(a)#預測解答句子
    print(c)#正確解答句子
    
    prf(c,a)#prf
    
    print(Rt)#這是第幾行，顯示目前進度
    
    if(Rt >= 1):
        break

#排列並列印出現的次數
Tr = sorted(T.items(), key=lambda x:x[1],reverse=True)
print(Tr[0:100]) #前100名

'''
B_ans = All_cap_B_size / Bll_size
A_ans = All_cap_B_size / All_size

#p,r,f

print('p:'+str(B_ans))
print('r:'+str(A_ans))
print('f:'+str(2*B_ans*A_ans / (B_ans+A_ans)))
'''

text.close()
end= time.time()

#最終花費時間
print(f'{end-start} s')

