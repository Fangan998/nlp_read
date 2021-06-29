import time

#Longest positive match
def pos(text,dict_word,result,result_set): #text : A paragraph of text
    global longest_term

    start = 0
    while start <len(text):
        if start + longest_term -1 >= len(text):
            end = len(text)-1
        else:
            end = start + longest_term - 1
        while end >= start:
            word = text[start:end + 1]
            if word in dict_word:
                result[word] +=1      #renew the dictionary
                result_set.add(word)  #renew the sets
                start += len(word)
                break
            end -= 1
            if end < start:  #with can't find Matchable words, Represents punctuation marks or letters 
                start += 1

def neg(text,dict_word,result,result_set):
    end = len(text)-1
    while end >=0:
        if end - longest_term + 1 < 0:
            start = 0
        else:
            start =end - longest_term + 1
        while start <= end:
            word = text[start:end + 1]
            if word in dict_word:
                result[word] +=1
                result_set.add(word)
                end -= len(word)
                break
            start +=1
            if start > end:
                end -= 1 

def compare(set1, set2):     #set1:correct answer   set2:Result to check
    set_intersection = set1.intersection(set2)  #交集(Intersection)
    #Return the length of each set to facilitate the calculation of the P.R.F value later
    return [len(set1), len(set2), len(set_intersection)] 

def ranking(dictionary):
    #print("排名 : ")
    result = {}   #Keep the words that have appeared with the top 100
    rank = 0
    dictionary = dict(sorted(dictionary.items(), key=lambda d: d[1], reverse=True))
    for element in dictionary.keys():
        if dictionary[element] != 0:
            # print(f"{element}: {dictionary[element]} 次")
            result.update({element : dictionary[element]})
            rank += 1
            if rank >= 100:
                break
        else:     #Sort big to small ,If num is 0 ,The latter must be 0, No need to deal with  
            break
    # print("\n\n")
    return result


time_start = time.time()  
print("loading....")

longest_term = 0

dict_word = {} #bulic the dictionary
with open("dec\\lexicon1_raw_nosil.txt", encoding="utf8") as file:
    line = file.readline()
    while line:
        line_list = line.split()
        dict_word.update({line_list[0] : 0})   #Word occurrences
        if len(line_list[0]) > longest_term:
            longest_term = len(line_list[0])
        line = file.readline()

count = 0
#copy
dict_positive = dict_word.copy()  
dict_negative = dict_word.copy()

#計算P.R.F值的基準
sum_answer = 0.0       #標準答案的總長度(TP + FN)
sum_positive = 0.0     #正向最長匹配分詞結果的長度(TP + FP)
sum_negative = 0.0     #反向最長匹配分詞結果的長度(TP + FP)
sum_ans_posi = 0.0     #正向最長匹配結果與答案相同的長度(TP)
sum_ans_nega = 0.0     #反向最長匹配結果與答案相同的長度(TP)

with open("test_date\\GigaWord_text_lm.txt", encoding="utf8") as file: 
    line = file.readline()
    while line:
        count += 1
        text = ""
        set_answer = set()
        set_positive = set()
        set_negative = set()
        if count <= 1000000000:
            line_list = line.split()
            for element in line_list:
                # test => print(element)
                set_answer.add(element)   #原來的檔案已經是分詞完的狀態
                text += element
            #positive match
            pos(text, dict_word, dict_positive, set_positive)
            #negative match
            neg(text, dict_word, dict_negative, set_negative)
            #比較兩者結果 計算P.R值(採用累加的概念)
            result_pos = compare(set_answer, set_positive)
            result_neg = compare(set_answer, set_negative)
            sum_answer += result_pos[0]
            sum_positive += result_pos[1]
            sum_ans_posi += result_pos[2]
            sum_negative += result_neg[1]
            sum_ans_nega += result_neg[2]
            
            line = file.readline()
        else:
            break
        if count % 10000 == 0:                              
            print(f"已處理{count}行")

    print(f"共處理 {count}行")

# result_positive = ranking(dict_positive)
# result_negative = ranking(dict_negative)
print("\n正向與反向的P,R,F")
#計算P.R.F值
p_positive = sum_ans_posi / sum_positive  # P = TP / (TP + FP)
p_negative = sum_ans_nega / sum_negative
r_positive = sum_ans_posi / sum_answer    # R = TP / (TP + FN)
r_negative = sum_ans_nega / sum_answer
f_positive = (2 * p_positive * r_positive) / (p_positive + r_positive) # F = 2PR / (P + R)
f_negative = (2 * p_negative * r_negative) / (p_negative + r_negative)
print("正向:")
print(f"\t正向P : {round(p_positive, 5)}")
print(f"\t正向R : {round(r_positive, 5)}")
print(f"\t正向F : {round(f_positive, 5)}")
print("反向:")
print(f"\t反向P : {round(p_negative, 5)}")
print(f"\t反向R : {round(r_negative, 5)}")
print(f"\t反向F : {round(f_negative, 5)}")

time_end = time.time()
print(f"花費時間 : {round(time_end - time_start, 3)} 秒")
