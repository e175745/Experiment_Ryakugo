import pandas
import sys
import pickle
import numpy as np
from sklearn.linear_model import LinearRegression
from input import read_file, conv_str_to_kana, conv_kana_to_vec, conv_vec_to_kana


# モデルのロード
try:
    args = sys.argv
    filename = args[1]
    print(filename)
    loaded_model = pickle.load(open(filename, 'rb'))
except Exception as e:
    print("名前が違います")
    sys.exit()

# 予測したいタイトルを取得
title_list = []
print("\n予測したいタイトルを入力:")
title = input()

# ベクトルに処理して予測
title_list.append(title)
kana_title = conv_str_to_kana(title_list)
vec_title = conv_kana_to_vec(kana_title,1,"T")
ryaku = loaded_model.predict(vec_title)
for title in ryaku:
    for index,i in enumerate(title):
        if i<=0.475:
            title[index] = 0
        else:
            title[index] = 1

ryaku = ryaku.tolist()
ryaku_kana = conv_vec_to_kana(ryaku,1)
print("\n予測された略:")
for x in ryaku_kana:
    print(" ".join(x))
    print("")
