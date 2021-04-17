#!/usr/bin/env python

import sys
import xlrd
import re
import pykakasi

NG_WORD_FILE = "ng_word_list.txt"

stat = {
        "nb_short_word": 0,
        "nb_long_word": 0,
        "nb_confuse_word1": 0,
        "nb_confuse_word2": 0,
        "nb_sushi": 0,
        "nb_katakana": 0,
        "nb_txu": 0,
        "nb_sensitive_word": 0,
        "nb_hinshi_mismatched": 0,
        "nb_words_taken": 0,
        }

re_hinshi = re.compile("^(名詞|動詞|形容詞).*")
#re_hinshi = re.compile("^名詞.*")
#re_hinshi = re.compile("^(名詞|形容詞).*")
re_confuse1 = re.compile("[ヲーズヅ]")
re_confuse2 = re.compile("[オコソトノホモヨロ][ウオ]")
re_sensitive = None # create later.

def getopts():
    from argparse import ArgumentParser
    from argparse import ArgumentDefaultsHelpFormatter
    ap = ArgumentParser(
            description="wordfilter generates word list ",
            formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("base_dict", help="specify the base dictionary.")
    ap.add_argument("-r", action="store", dest="word_rank",
                    type=int, default=3000,
                    help="specify the word rank.")
    ap.add_argument("-s", action="store_true", dest="show_stat",
                    help="specify to show statistics.")
    ap.add_argument("-o", action="store", dest="output_file",
                    help="specify a filename to be stored the output.")
    ap.add_argument("--exclude-katakana", action="store_true",
                    dest="ex_katakana",
                    help="specify a filename to be stored the output.")
    return ap.parse_args()

def main():
    opt = getopts()
    # reading vocabulary database.
    # assuming the dict is "VDLJ_Ver1_0_International-Students.xlsx"
    # the first line is the header. needs to skip 1 line.
    xls_wb = xlrd.open_workbook(opt.base_dict)
    xls_sheet = xls_wb.sheet_by_index(1)
    rows = xls_sheet.get_rows()
    row = rows.__next__()
    # read ng word list.
    ng_words = open(NG_WORD_FILE).read().splitlines()
    ng_words = filter(lambda s: '#' not in s and len(s) > 0, ng_words)
    re_sensitive = re.compile("({})".format("|".join(ng_words)))
    # open output file.
    if opt.output_file:
        ofd = open(opt.output_file, "w")
    else:
        ofd = sys.stdout
    # start evaluation.
    wdb = {}
    kks = pykakasi.kakasi()
    for row in rows:
        lexeme = row[9].value
        yomi = row[11].value
        hinshi = row[12].value
        rank = row[1].value
        # word rankのチェック
        if rank > opt.word_rank:
            continue
        # (option)カタカナ語を除外する。
        if opt.ex_katakana and lexeme == yomi:
            stat["nb_katakana"] += 1
            continue
        # 3文字から5文字に絞る。
        word_len = len(yomi)
        if word_len < 3:
            stat["nb_short_word"] += 1
            continue
        if word_len > 5:
            stat["nb_long_word"] += 1
            continue
        # 3文字語で2文字目が「っ」を除外する。
        if word_len == 3 and yomi[1] == "ッ":
            stat["nb_txu"] += 1
            continue
        # 品詞を絞る。
        r = re_hinshi.match(hinshi)
        if not r:
            stat["nb_hinshi_mismatched"] += 1
            continue
        # 数詞を除外する。
        if hinshi.find("数詞") > 0:
            stat["nb_sushi"] += 1
            continue
        # 紛らわしい語彙を除外する。
        r = re_confuse1.search(yomi)
        if r:
            stat["nb_confuse_word1"] += 1
            continue
        r = re_confuse2.search(yomi)
        if r:
            stat["nb_confuse_word2"] += 1
            continue
        # 相応しくない語彙を除外する。
        r = re_sensitive.match(yomi)
        if r:
            stat["nb_sensitive_word"] += 1
            continue
        # ひらがなに変換する。
        kksres = kks.convert(yomi)
        if len(kksres) > 1:
            raise ValueError(f"{yomi}")
            continue
        # 重複を除外する。
        wdb.update({kksres[0]["hira"]:None})
    #
    if opt.show_stat:
        stat["nb_words_taken"] = len(wdb.keys())
        for k,v in stat.items():
            print(f"{k}: {v}", file=sys.stderr)
    else:
        for k in wdb.keys():
            print(k, file=ofd)

if __name__ == "__main__":
    main()
