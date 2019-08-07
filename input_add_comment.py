#coding utf-8
import pandas as pd
import numpy as np
from janome.tokenizer import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity
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
    """
    カタカナをベクトルに変換
    母音は５種類、子音20種類
    ん、ー、っ、ゔは「kana_lists」にないので先に決定しておく
    """
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
                #母音と子音の重きを決めていく
                for i, kana_list in enumerate(kana_lists):#「kana_list」に「kana_lists」の配列を代入。その配列の番目が「i」。つまり「kana_list」≒「kana_lists」
                    if char in kana_list:#上の「char」が「kana_list」の何番目にあるかを確かめる
                        index = kana_list.index(char)#「char」の「kana_lists」の何番目という情報を「index」に代入
                        consonant_list[i] = weight#i番目、つまり子音要素に重き
                        vowel_list[index] = weight#index番目、つまり母音要素に重き
                        break
    
        title_vec = title_vec + vowel_list + consonant_list
        
        if TorR=="T":
            while len(title_vec) <= 25*39:
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


"""
    def conv_kana_to_vec_type2(str_list, TorR):
    output_vec = []
    # for文で一文字づつ判定
    for title in str_list:
    title_vec = []
    for char in title:
    vowel_index = 0
    consonant_index = 0
    if char == u"ン":
    consonant_index = 18
    elif char == u"ー":
    consonant_index = 19
    elif char == u"ッ":
    consonant_index = 20
    elif char == u"ヴ":
    consonant_index = 11
    vowel_index = 3
    else:
    for i, kana_list in enumerate(kana_lists):
    if char in kana_list:
    index = kana_list.index(char)
    consonant_index = i+1
    vowel_index = index+1
    break
    title_vec.append(vowel_index)
    title_vec.append(consonant_index)
    if TorR=="T":
    while len(title_vec) <= 35*2+1:
    title_vec.append(0)
    #タイトル群に追加
    output_vec.append(title_vec)
    elif TorR=="R":
    while len(title_vec) <= 5*2+1:
    title_vec.append(0)
    #タイトル群に追加
    output_vec.append(title_vec)
    return output_vec
    """


def read_file(file):
    """
    csvファイルを読み込み
    教師とデータそれぞれを別の配列に入れる
    """
    data = pd.read_csv(file)
    str_list = list(data['Title_kana'])
    answer_list = list(data['Ryaku_kana'])
    return str_list, answer_list

def conv_str_to_kana(str_list):
    """
    ファイルから読み込んだものをJanomeを使ってカタカナに変換する
    """
    t = Tokenizer()
    kana_list = []
    for i in str_list:
        kana = ""
        for token in t.tokenize(i):
            if token.reading == "*":
                kana = kana + (token.base_form)
            else:
                kana = kana + (token.reading)
        kana_list.append(kana)
    
    return kana_list


"""
    def conv_vec_to_kana_type2(vec_list,weight):
    kana_list = []
    for vec_title in vec_list:
    title = []
    while len(vec_title) != 0 :
    vec_char = vec_title[0:2]
    del vec_title[0:2]
    char = conv_vec_to_char_type2(vec_char,weight)
    if char != "":
    title.append(char)
    kana_list.append(title)
    return kana_list
    """


def conv_vec_to_kana(vec_list,weight):
    """
    ベクトルをカナに変換する
    """
    kana_list = []
    for vec_title in vec_list:
        title = []
        while len(vec_title) != 0 :
            vec_char = vec_title[0:25]
            del vec_title[0:25]
            char = conv_vec_to_char(vec_char,weight)
            if char != "":
                title.append(char)
        kana_list.append(title)
    
    return kana_list

def conv_vec_to_char(vec_char, weight):
    """
    ベクトルをcharに変換
    """
    kana_lists_array = np.array(kana_lists)
    vowel_vec = vec_char[0:5]
    
    del vec_char[0:5]
    consonant_vec = vec_char
    char = ""
    try:
        consonant_index = consonant_vec.index(weight)
        if consonant_index == 17 :
            char = u"ン"
        elif consonant_index == 18 :
            char = u"ー"
        elif consonant_index == 19 :
            char = u"ッ"
        else :
            vowel_index = vowel_vec.index(weight)
            char = kana_lists_array[consonant_index,vowel_index]

except ValueError:
    pass
    
    return char


"""
    def conv_vec_to_char_type2(vec_char, weight):
    kana_lists_array = np.array(kana_lists)
    vowel_index = vec_char[0]
    consonant_index = vec_char[1]
    char = ""
    if consonant_index == 18 :
    char = u"ン"
    elif consonant_index == 19 :
    char = u"ー"
    elif consonant_index == 20 :
    char = u"ッ"
    else :
    char = kana_lists_array[consonant_index-1,vowel_index-1]
    return char
    """


def fix_data(title_list,ryaku_list):
    """
    予測した文字が元タイトルになかった場合、タイトルにある文字に変更する
    """
    
    title_s = title_list
    ryaku_s = ryaku_list
    fix_list = []
    
    for i,title in enumerate(title_s):
        title_charlist = []
        ryaku_charlist = []
        
        ryaku = ryaku_s[i]
        while len(title) != 0 :
            title_charlist.append(title[0:25])
            del title[0:25]
        
        while len(ryaku) != 0 :
            ryaku_charlist.append(ryaku[0:25])
            del ryaku[0:25]
    
        fix_title = []
        for title_char in title_charlist:
            sim_list = []
            list_a =[]
            for ryaku_char in ryaku_charlist:
                list_a.append(title_char)
            #sim_list.append(cosine_similarity(title_char, ryaku_char))
            sim_list = cosine_similarity(list_a, ryaku_charlist)
            sim_list = sim_list[0]
            sim_list = sim_list.tolist()
            sim_index = sim_list.index(min(sim_list))
            fix_title = fix_title + ryaku_charlist[sim_index]
        
                fix_list.append(fix_title)
            return fix_list, ryaku_list

def calc_accuracy(list_ans, list_ryaku):
    """
    1文字ごとの正答率を出す
    """
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
    data = read_file('dataset_two.csv')
    kana_title, kana_ans = conv_str_to_kana(data[0],data[1])
    vec_title = conv_kana_to_vec(kana_title,1,"T")
    #vec_ans = conv_kana_to_vec(kana_ans)
    #kana_title = conv_vec_to_kana(vec_title)
    #conv_vec_to_kana(vec_title)
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
