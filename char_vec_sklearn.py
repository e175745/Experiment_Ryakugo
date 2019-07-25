# coding UTF-8
from input import read_file, conv_str_to_kana, conv_kana_to_vec, conv_vec_to_kana, calc_accuracy
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import csv
import pickle

#data = read_file('dataset_for.csv')
data = read_file('abbrs_title.csv')
kana_title = conv_str_to_kana(data[0])
kana_ans = conv_str_to_kana(data[1])
#vec_title = conv_kana_to_vec(kana_title,1,"T")
#vec_ans = conv_kana_to_vec(kana_ans,2,"R")
vec_title = conv_kana_to_vec(kana_title,1,"T")
vec_ans = conv_kana_to_vec(kana_ans,1,"R")
"""
# 相関関係ヒートマップ
sns.set()

vec_title = np.array(vec_title)
corr = np.corrcoef(vec_title.transpose(), vec_title)
print(corr)
sns.heatmap(corr, annot=True)
plt.show()
"""

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

"""
# データセットを学習用とテスト用に分割
X_train, X_test, Y_train, Y_test = train_test_split(vec_title, vec_ans, train_size = 0.8, test_size = 0.2, random_state = 1)

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
"""

loo = LeaveOneOut()
lr = LinearRegression()
vec_ans = np.array(vec_ans)
vec_title = np.array(vec_title)
result = []
result_T = []
count = 0
for train_index, test_index in loo.split(vec_title):
    X_train, X_test = vec_title[train_index], vec_title[test_index]
    Y_train, Y_test = vec_ans[train_index], vec_ans[test_index]
    lr.fit(X_train, Y_train)
    Y_pred = lr.predict(X_test)
    Y_pred = Y_pred.tolist()
    Y_test = Y_test.tolist()
    result.append(Y_pred[0])
    result_T.append(Y_test[0])

Y_pred = np.array(result)
Y_test = np.array(result_T)

# モデルの保存
filename = 'Linear_Regression.sav'
pickle.dump(lr, open(filename, 'wb'))

# 予測と正解の差異を計算
pred_diff = []
for j,title in enumerate(Y_pred):
    title_diff = []
    for k,val in enumerate(title):
        diff = abs(val - Y_test[j,k])
        title_diff.append(diff)
    pred_diff.append(title_diff)


# csvに出力

conbi = []
for k,title in enumerate(Y_pred):
    ans = Y_test[k]
    conbi.append(title)
    conbi.append(ans)

with open("conbi.csv", "w") as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(Y_pred)

# 0,1に変換
for title in result:
    for index,i in enumerate(title):
        if i<=0.35:
            title[index] = 0
        else:
            title[index] = 1
        """
        ind = abs(round(i))
        if index%2==0 and ind >= 6:
            title[index] = 5
        elif ind > 20 :
            title[index] = 20
        else :
            title[index] = ind
        """

# カナに直して比較
# Y_pred = Y_pred.tolist()
# Y_test = Y_test.tolist()

Y_pred_kana = conv_vec_to_kana(result,1)
Y_test_kana = conv_vec_to_kana(result_T,1)

for x, y in enumerate(Y_pred_kana):
    print(" ".join(Y_test_kana[x]))
    print(" ".join(y))
    print("\n")

print(calc_accuracy(Y_test_kana,Y_pred_kana))
