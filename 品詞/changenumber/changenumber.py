import sys
args = sys.argv # 読み込みファイル名の取得
FILE_IN = args[1] # ファイル名の格納

with open("品詞分解後のファイル/"+FILE_IN+".txt","r") as f:
    lines = f.readlines()

with open("./rule.txt","r") as f:
    rule = f.readlines()

with open("品詞分解後のファイル/"+FILE_IN+".txt","w") as w:
    for l in lines:
        for k in rule:
            l_split = l.replace("\n","").split(" ")
            k_split = k.replace("\n","").split(" ")
            if l_split[1] == k_split[0]:
                w.write(l.replace("\n","")+" "+str(k_split[1])+"\n")
