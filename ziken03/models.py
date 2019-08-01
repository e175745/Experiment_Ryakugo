# coding UTF-8
import matplotlib.pyplot as plt
from input import read_file, conv_str_to_kana, conv_kana_to_vec, conv_vec_to_kana, calc_accuracy
from sklearn import svm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

#データ生成部
List = pd.read_csv('dataset_proto.csv')
data = read_file('dataset_proto.csv')
kana_title, kana_ans = conv_str_to_kana(data[0],data[1])
vec_title = conv_kana_to_vec_meta(kana_title,1,"T")
vec_ans = conv_kana_to_vec_meta(kana_ans,1,"R")

List1 = List.copy()
List1['Title_vec'] = vec_title
List1['Ans_vec'] = vec_ans

pca = PCA(n_components=1)
x_pca = pca.fit_transform(vec_title)
y_pca = pca.fit_transform(vec_ans)
List2 = List1.copy()
List2['X'] = x_pca
List2['Y'] = y_pca

model1 = KMeans(n_clusters=5, random_state=0)
data1_X = List2[['X','Y']]
model1.fit(data1_X)
y1 = model1.labels_
print(y1)
data_results = List2.copy()
data_results['分類結果'] = y1
data_result = data_results.sort_values('分類結果')

#データ分類部
list_title = data_results[['Title_vec']]
list_ans = data_results[['Ans_vec']]
list_title = list_title.values
list_ans = list_ans.values

num = 0
list0_title = []
list1_title = []
list2_title = []
list3_title = []
list4_title = []
list0_ans = []
list1_ans = []
list2_ans = []
list3_ans = []
list4_ans = []

list_ = data_results[['分類結果']].values
for i in list_:
    if int(i) == 0:
        list0_title.extend(list_title[num])
        list0_ans.extend(list_ans[num])
    elif int(i) == 1:
        list1_title.extend(list_title[num])
        list1_ans.extend(list_ans[num])
    elif int(i) == 2:
        list2_title.extend(list_title[num])
        list2_ans.extend(list_ans[num])
    elif int(i) == 3:
        list3_title.extend(list_title[num])
        list3_ans.extend(list_ans[num])
    elif int(i) == 4:
        list4_title.extend(list_title[num])
        list4_ans.extend(list_ans[num])
    else:
        print("なんか抜けてるよ")
    num += 1

#学習と予測の関数
def clustering(trainX,trainY):
    X_train, X_test, Y_train, Y_test = train_test_split(vec_title, vec_ans, train_size = 0.8, test_size = 0.2, random_state = 0)
    # 線形回帰に適用
    lr = LinearRegression()
    lr.fit(trainX,trainY)
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

    #print(mean_absolute_error(Y_test, Y_pred))
    # csvに出力
    with open("pred_diff.csv", "w") as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(pred_diff)

    # 0,1に変換
    for title in Y_pred:
        for index,i in enumerate(title):
            if i<=0.2:
                title[index] = 0
            else:
                title[index] = 1
        # title[index] = round(j)

    # カナに直して比較
    Y_pred = Y_pred.tolist()
    Y_test = Y_test.tolist()

    Y_pred_kana = conv_vec_to_kana(Y_pred)
    Y_test_kana = conv_vec_to_kana(Y_test)

    return calc_accuracy(Y_pred_kana,Y_test_kana), Y_pred_kana, Y_test_kana

#実行部
model_listT = [list0_title, list1_title, list2_title, list3_title, list4_title]
model_listA = [list0_ans, list1_ans, list2_ans, list3_ans, list4_ans]

for i in range(5):
    score, Y_pred_kana, Y_test_kana = clustering(model_listT[i], model_listA[i])
    print("モデル"+str(i)+"号")
    print(str(score)+"点")
    """
    for x, y in enumerate(Y_pred_kana):
        print(" ".join(Y_test_kana[x]))
        print(" ".join(y))
        print("\n")
    """
