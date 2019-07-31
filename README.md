# Anime Title Abbreviation
=====
### 琉球大学工学部知能情報実験Ⅱ データマイニング班 G1
## Description
過去のアニメタイトルから未知のアニメタイトルの略称を予測する。
タイトルを一文字づつベクトル化し、線形回帰を用いてた略称となるばベクトル群を求める。
モジュールはsklearnに入っているLinearRegressionを使用した。

## File Contents
### input.py
データの取り込みや前処理に関する関数が書かれている。
基本的にはchar_vec_sklearn.pyでモジュールとしてインポートし、使用する。

### char_vec_sklearn.py
input.pyにある関数を用いて学習を行う。
基本的にはただ実行するだけで学習が行われる。
また、学習とともにモデルの保存や精度の計算を行う。

### exe_Ryaku.py
保存されたモデルを用いて未知のタイトルに対して略称を予測する。
下記のように実行することで起動可能。
% python3 exe_Ryaku.py Linear_Regression.sav
引数には保存したモデルの名前を渡してやる。
指示に従って予測してほしいタイトルを入力すると学習機によって予測された略称が出てくる。

## Git URL
https://github.com/e175745/Experiment_Ryakugo.git

## About Datasets
今回使用したデータセットについては、Webページに記載されている情報をウェブスクレイピングによって収集しcsvファイルに直したものを使用した。収集したデータの再配布はあまり良くないのでここでは公開しない。

## Development Environment
macOS Mojave
python 3.7.2
sklearn 0.20.3
janome 0.3.9

## Author
氏名 : 松本 一馬
連絡先 : e175745@ie.u-ryukyu.ac.jp
