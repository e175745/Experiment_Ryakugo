#coding utf-8
import pandas as pd
import numpy as np
from janome.tokenizer import Tokenizer

# 判定に使うカナリスト
kana_lists = [\
    [u"ア", u"イ", u"ウ", u"エ", u"オ"],\
    [u"ァ", u"ィ", u"ゥ", u"ェ", u"ォ"],\
    [u"カ", u"キ", u"ク", u"ケ", u"コ"],\
    [u"ガ", u"ギ", u"グ", u"ゲ", u"ゴ"],\
    [u"サ", u"シ", u"ス", u"セ", u"ソ"],\
    [u"ザ", u"ジ", u"ズ", u"ゼ", u"ゾ"],\
    [u"タ", u"チ", u"ツ", u"テ", u"ト"],\
    [u"ダ", u"ヂ", u"ヅ", u"デ", u"ド"],\
    [u"ナ", u"ニ", u"ヌ", u"ネ", u"ノ"],\
    [u"ハ", u"ヒ", u"フ", u"ヘ", u"ホ"],\
    [u"バ", u"ビ", u"ブ", u"ベ", u"ボ"],\
    [u"パ", u"ピ", u"プ", u"ペ", u"ポ"],\
    [u"マ", u"ミ", u"ム", u"メ", u"モ"],\
    [u"ヤ", u"", u"ユ", u"", u"ヨ"],\
    [u"ャ", u"", u"ュ", u"", u"ョ"],\
    [u"ラ", u"リ", u"ル", u"レ", u"ロ"],\
    [u"ワ", u"ヰ", u"", u"ヱ", u"ヲ"]]

def conv_kana_to_vec(str_list,weight, TorR):
    output_vec_vow = []
    output_vec_con = []
    # for文で一文字づつ判定
    for title in str_list:
        title_vow = []
        title_con = []
        for char in title:
            vowel_list = [0]*5
            consonant_list = [0]*20
            if char == u"ン":
                consonant_list[17] = weight
            elif char == u"ー":
                consonant_list[18] = weight
            elif char == u"ッ":
                consonant_list[19] = weight
            elif char == u"ヴ":
                consonant_list[10] = weight
                vowel_list[2] = weight
            else:
                for i, kana_list in enumerate(kana_lists):
                    if char in kana_list:
                        index = kana_list.index(char)
                        consonant_list[i] = weight
                        vowel_list[index] = weight
                        break

            title_vow += vowel_list
            title_con += consonant_list

        if TorR=="T":
            while len(title_vow) <= 5*35:
                emp_list = [0]*5
                title_vow = title_vow + emp_list
            while len(title_con) <= 20*35:
                emp_list = [0]*20
                title_con = title_con + emp_list
                #タイトル群に追加
            output_vec_vow.append(title_vow)
            output_vec_con.append(title_con)

        elif TorR=="R":
            while len(title_vow) <= 5*4:
                emp_list = [0]*5
                title_vow = title_vow + emp_list
            while len(title_con) <= 20*4:
                emp_list = [0]*20
                title_con = title_con + emp_list
                #タイトル群に追加
            output_vec_vow.append(title_vow)
            output_vec_con.append(title_con)
    return output_vec_vow, output_vec_con

def conv_kana_to_vec_meta(str_list,weight, TorR):
    output_vec = []
    # for文で一文字づつ判定
    for title in str_list:
        title_vec = []
        for char in title:
            vowel_list = [0]*5
            consonant_list = [0]*20
            if char == u"ン":
                consonant_list[17] = weight
            elif char == u"ー":
                consonant_list[18] = weight
            elif char == u"ッ":
                consonant_list[19] = weight
            elif char == u"ヴ":
                consonant_list[10] = weight
                vowel_list[2] = weight
            else:
                for i, kana_list in enumerate(kana_lists):
                    if char in kana_list:
                        index = kana_list.index(char)
                        consonant_list[i] = weight
                        vowel_list[index] = weight
                        break

            title_vec = title_vec + vowel_list + consonant_list

        if TorR=="T":
            while len(title_vec) <= 25*35:
                emp_list = [0]*25
                title_vec = title_vec + emp_list
                #タイトル群に追加
            output_vec.append(title_vec)

        elif TorR=="R":
            while len(title_vec) <= 25*4:
                emp_list = [0]*25
                title_vec = title_vec + emp_list
                #タイトル群に追加
            output_vec.append(title_vec)
    return output_vec

def read_file(file):

    # csvファイルを読み込み
    # 教師とデータそれぞれを別の配列に入れる
    data = pd.read_csv(file)
    str_list = list(data['Title_kana'])
    answer_list = list(data['Ryaku_kana'])
    return str_list, answer_list

def conv_str_to_kana(str_list,answer_list):

    #ファイルから読み込んだものをJanomeを使ってカタカナに変換
    t = Tokenizer()
    kana_list = []
    kana_ans_list = []
    for i in str_list:
        kana = ""
        for token in t.tokenize(i):
            if token.reading == "*":
                kana = kana + (token.base_form)
            else:
                kana = kana + (token.reading)
        kana_list.append(kana)

    for j in answer_list:
        kana_ans = ""
        for token in t.tokenize(j):
            if token.reading == "*":
                kana_ans = kana_ans + (token.base_form)
            else:
                kana_ans = kana_ans + (token.reading)
        kana_ans_list.append(kana_ans)

    return kana_list, kana_ans_list

def conv_vec_to_kana(vec_list):
    kana_list = []
    for vec_title in vec_list:
        title = []
        while len(vec_title) != 0 :
            vec_char = vec_title[0:25]
            del vec_title[0:25]
            char = conv_vec_to_char(vec_char)
            if char != "":
                title.append(char)
        kana_list.append(title)

    return kana_list


def conv_vec_to_char(vec_char):
    kana_lists_array = np.array(kana_lists)
    vowel_vec = vec_char[0:5]

    del vec_char[0:5]
    consonant_vec = vec_char
    char = ""
    try:
        consonant_index = consonant_vec.index(1)
        if consonant_index == 17 :
            char = u"ン"
        elif consonant_index == 18 :
            char = u"ー"
        elif consonant_index == 19 :
            char = u"ッ"
        else :
            vowel_index = vowel_vec.index(1)
            char = kana_lists_array[consonant_index,vowel_index]

    except ValueError:
        pass

    return char

def calc_accuracy(list_ans, list_ryaku):
    num = 0
    acc = 0

    for i,ans in enumerate(list_ans):
        ryaku = list_ryaku[i]

        for j,char in enumerate(ans):
            num+=1

            try:
                if char == ryaku[j] :
                    acc+=1

            except IndexError:
                pass
    acc = acc/num
    return acc

# 処理諸々
"""
data = read_file('datasets_two.csv')
kana_title, kana_ans = conv_str_to_kana(data[0],data[1])
vec_title = conv_kana_to_vec(kana_title)
vec_ans = conv_kana_to_vec(kana_ans)
kana_title = conv_vec_to_kana(vec_title)
conv_vec_to_kana(vec_title)

for y in kana_title:
    print(" ".join(y))

for i,kana_title in enumerate(kana_title):
    print(kana_title)
    print(vec_title[i])

s = "やはり俺の青春ラブコメは間違っている"
t = Tokenizer()
for token in t.tokenize(s):
    print(token)
"""
