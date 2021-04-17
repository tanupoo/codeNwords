codeNwords
==========

ハイフンでN個のブロックに区切られたM桁の数字のコードを
N個の単語で表現するだけのプログラムです。
はい、なんちゃって[what3words](https://what3words.com/)です。

単語数が不十分なのでMの最大値は4になります(後述)。

ブロック数を増やせば全体の桁数は増やせます。
伝える単語数が増えますがおそらくは使用上大きな問題にはならないかと思います。

## CLIでの使い方

- コードとN単語のペア生成の例

```
% python codeNwords.py word_list.txt
{'code': '398-292-128', 'words': 'あいさつ-うける-つめたい', 'version': '# ver. 2021-04-17T21:05:23.671706'}

% python codeNwords.py word_list.txt --nb-blocks 4 --nb-digits 4
{'code': '8015-0383-7595-3722', 'words': 'らいふる-ふえる-しきてん-りんしょう', 'version': '# ver. 2021-04-17T21:05:23.671706'}
```

- コードとN単語の変換の例

```
% python codeNwords.py word_list.txt -c 'さわぐ-もでる-くつした'
497-892-234

% python codeNwords.py word_list.txt -w '497-892-234'
さわぐ-もでる-くつした
```

## APIとサンプル

- [test.py](https://github.com/tanupoo/codeNwords/blob/main/test.py)

```python
import codeNwords

cwm = codeNwords.CodeWordMap(word_file)

ret = cwm.gencode()
print(cwm.code2words(ret["code"]))
print(cwm.words2code(ret["words"]))
```

`CodeWordMap()`の引数`map_type`を1(CODE2WORDS)または2(WORDS2CODE)にすると、
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
% python make_word_list.py VDLJ_Ver1_0_International-Students.xlsx -r 30000
```

留学生用語彙ランク3000までで約1000語用意できます。
ランクの最大値20288で約10000語用意できます。
リポジトリに置いてある変換済みの辞書は約10000語あります。
簡単な語彙から並べてあるのでMを3(--nb-digits=3)にすると簡単な語彙が選ばれます。

松下達彦先生に感謝致します。
ライセンスが見当たらないのですが何か問題がありましたらご指摘下さい。

