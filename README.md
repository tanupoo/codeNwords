codeNwords
==========

ハイフンでN個のブロックに区切られたM桁の数字のコードを
N個の単語で表現するだけのプログラムです。
はい、なんちゃって[https://what3words.com/](what3words)です。

## CLIでの使い方

```
% python codeNwords.py word_list.txt
{'code': '500-897-234', 'words': 'さわぐ-もでる-くつした'}

% python codeNwords.py word_list.txt
{'code': '324-243-133', 'words': 'たてる-ゆうはん-ごめん'}

% python codeNwords.py word_list.txt -c 'さわぐ-もでる-くつした'
500-897-234

% python codeNwords.py word_list.txt -w '324-243-133'
たてる-ゆうはん-ごめん
```

## APIとサンプル

[test.py]

## word_list.txt

元データは東京大学松下達彦研究室言語学習ラボの
[日本語を読むための語彙データベース](http://www17408ui.sakura.ne.jp/tatsum/database.html)のうち、
「日本語を勉強する人のための語彙データベース（留学生用）」(ファイル名: VDLJ_Ver1_0_International-Students.xlsx) から、
make_word_list.py を用いて、
ご時世に相応しくないと思われる単語と、
口頭で伝えにくと思われる単語を除外しました。

留学生用語彙ランク3000までで約1000語用意できます。
ランクの最大値20288で約10000語用意できます。

```
% python make_word_list.py VDLJ_Ver1_0_International-Students.xlsx -o word_list.txt
```

ライセンスが見当たらないのですが何か問題がありましたらご指摘下さい。

