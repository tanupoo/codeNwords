codeNwords
==========

ハイフンでN個のブロックに区切られたM桁の数字のコードを
N個の単語で表現するだけのプログラムです。
はい、なんちゃって[https://what3words.com/](what3words)です。

語彙数が不十分なのでMの最大値は4になります。(後述)
ブロック数を増やせば全体の桁数は増やせるので伝える語彙が増えますが
おそらくは使用上大きな問題にはならないかと思います。

## CLIでの使い方

```
% python codeNwords.py word_list.txt
{'code': '500-897-234', 'words': 'さわぐ-もでる-くつした'}

% python codeNwords.py word_list.txt
{'code': '324-243-133', 'words': 'たてる-ゆうはん-ごめん'}

% python codeNwords.py word_list.txt --nb-blocks 4 --nb-digits 4
{'code': '6197-0673-6913-4043', 'words': 'ふりかかる-せいど-かくらん-あにめ'}
```

```
% python codeNwords.py word_list.txt -c 'さわぐ-もでる-くつした'
500-897-234

% python codeNwords.py word_list.txt -w '324-243-133'
たてる-ゆうはん-ごめん
```

## APIとサンプル

[test.py]

map_typeを1(CODE2WORDS)または2(WORDS2CODE)にすると、
少しだけメモリを節約できます。

## Usage

```
% python codeNwords.py -h
usage: codeNwords.py [-h] [-w CODE2WORDS] [-c WORDS2CODE]
                     [--nb-blocks NB_BLOCKS] [--nb-digits NB_DIGITS]
                     word_file

code2words generates code or convert code to words vice varsa.

positional arguments:
  word_file             specify a filename containing the word list.

optional arguments:
  -h, --help            show this help message and exit
  -w CODE2WORDS         specify a code to convert into words. (default: None)
  -c WORDS2CODE         specify words to convert into code. (default: None)
  --nb-blocks NB_BLOCKS, -b NB_BLOCKS
                        specify the number of blocks. (default: 3)
  --nb-digits NB_DIGITS, -g NB_DIGITS
                        specify the number of digits in a block. (default: 3)
```

## 辞書

元データは東京大学松下達彦研究室言語学習ラボの
[日本語を読むための語彙データベース](http://www17408ui.sakura.ne.jp/tatsum/database.html)のうち、
「日本語を勉強する人のための語彙データベース（留学生用）」(ファイル名: VDLJ_Ver1_0_International-Students.xlsx) から、
make_word_list.py を用いて、
ご時世に相応しくないと思われる単語と、
口頭で伝えにくと思われる単語を除外しました。

```
% python make_word_list.py VDLJ_Ver1_0_International-Students.xlsx -o word_list.txt
```

留学生用語彙ランク3000までで約1000語用意できます。
ランクの最大値20288で約10000語用意できます。
リポジトリに置いてある変換済みの辞書は約10000語あります。
簡単な語彙から並べてあるのでMを3(--nb-digits=3)にすると簡単な語彙が選ばれます。

松下達彦先生に感謝致します。
ライセンスが見当たらないのですが何か問題がありましたらご指摘下さい。

