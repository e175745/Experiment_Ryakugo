# coding UTF-8
from input import read_file, conv_str_to_kana, conv_kana_to_vec, conv_vec_to_kana
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np
import csv

data = read_file('dataset_proto.csv')
kana_title, kana_ans = conv_str_to_kana(data[0],data[1])
vec_title = conv_kana_to_vec(kana_title,1,"T")
vec_ans = conv_kana_to_vec(kana_ans,1,"R")

"""
for i,kana_title in enumerate(kana_title):
    print(kana_title)
    print(vec_title[i])

clf = svm.SVC(gamma=0.001, C=100)
clf.fit(vec_title[:-1], vec_ans[:-1])

result = clf.predict(data[:-1])
print("実際の答え={0}, 予測結果={1}".format(vec_ans[-1], result))

result = clf.score(data, vec_ans)
print(result)
"""
# データセットを学習用とテスト用に分割
X_train, X_test, Y_train, Y_test = train_test_split(vec_title, vec_ans, train_size = 0.8, test_size = 0.2, random_state = 0)

# 線形回帰に適用
lr = LinearRegression()
lr.fit(X_train, Y_train)
Y_pred = lr.predict(X_test)

Y_pred = np.array(Y_pred)
Y_test = np.array(Y_test)

# 予測と正解の差異を計算
pred_diff = []
for j,title in enumerate(Y_pred):
    title_diff = []
    for k,val in enumerate(title):
        diff = abs(val - Y_test[j,k])
        title_diff.append(diff)
    pred_diff.append(title_diff)

print(mean_absolute_error(Y_test, Y_pred))
# csvに出力
with open("pred_diff.csv", "w") as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(pred_diff)

# 0,1に変換
for title in Y_pred:
    for index,i in enumerate(title):
        if i<=0.35:
            title[index] = 0
        else:
            title[index] = 1
    # title[index] = round(j)

# カナに直して比較
Y_pred = Y_pred.tolist()
Y_test = Y_test.tolist()

Y_pred_kana = conv_vec_to_kana(Y_pred)
Y_test_kana = conv_vec_to_kana(Y_test)

for x, y in enumerate(Y_pred_kana):
    print(" ".join(Y_test_kana[x]))
    print(" ".join(y))
    print("\n")
