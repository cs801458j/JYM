from konlpy.tag import Kkma
from konlpy.tag import Twitter
import re


open_file_name = "./dic.txt"
lines = open(open_file_name, 'r', encoding='UTF-8', newline='').readlines()

dic = {}
for line in lines:
    temp = line.split("\t")
    temp[1] = re.sub('\r\n', '', temp[1])
    dic[temp[0]] = temp[1]

kkma = Kkma()
twiter = Twitter()

input_sentence = "솔직히 너무 비싸네요. 튼튼하긴 하네요. 잘 쓰겠습니다."
print("input : " + input_sentence)

pos_list = kkma.pos(input_sentence)

positive_list = []
negative_list = []
neutral_list = []
for i in pos_list:
    if i[1] == "VA":
        va = dic[i[0] + "다"]
        if va == "1" or va == "2":
            positive_list.append(i[0])
        elif va == "-1" or va == "-2":
            negative_list.append(i[0])
        else:
            neutral_list.append(i[0])
    # elif i[1] == "NNG":
    # 보류
    elif i[1] == "XR":
        xr = dic[i[0] + "하다"]
        if xr == "1" or xr == "2":
            positive_list.append(i[0] + "하")
        elif xr == "-1" or xr == "-2":
            negative_list.append(i[0] + "하")
        else:
            neutral_list.append(i[0] + "하")

temp_sentence = ""

for j in range(len(positive_list)):
    if j is len(positive_list) - 1:
        temp_sentence += positive_list[j] + "지만, "
    else:
        temp_sentence += positive_list[j] + "고, "

for j in range(len(negative_list)):
    if j is len(negative_list) - 1:
        temp_sentence += negative_list[j] + "다."
    else:
        temp_sentence += negative_list[j] + "고, "

print("\n" + temp_sentence)
