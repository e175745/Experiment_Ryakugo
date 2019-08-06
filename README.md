# Anime Title Abbreviation

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

### ziken03
実験の途中まで、試していたクラスタリングおよびアンサンブル学習に使用していたコードなどが入ったディレクトリ。  
最終的には使わなかったが、参考までにリポジトリに置いておく。メインのソースコードとは関係ないため説明は割愛。  

### 品詞
上記のziken03と同じく途中まで試していた、タイトル上の品詞を要素とする学習のソースコード。  
同じように最終的に使わず、メインのソースコードとは関係ないため説明は割愛する。  

### Linear_Regression.sav 
char_vec_sklearn.pyにて作成される学習機モデルを保存してあるsav形式のファイル。  
pickleのdumpコマンドによって保存されており、exe_Ryaku.pyを起動する際に必要。  

### ieExperiment2_presentation.pdf
実験の発表の際に使用したパワーポイント資料。  

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

## License
Copyright <2019> <Matsumoto Kazuma>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
