#!/usr/bin/env python

import random
from datetime import datetime
import hashlib

CODE2WORDS = 1
WORDS2CODE = 2
BOTH = 3

class CodeWordMap():

    def __init__(self, word_file: str, nb_digits: int=4, nb_blocks: int=3,
                 map_type: int=3):
        """
        map_type:
            1: code to words
            2: words to code
            3: both (default)
        """
        map_c2w = open(word_file).read().splitlines()
        self.version = map_c2w[0]   # take the version.
        map_c2w = map_c2w[1:]   # skip the first line.
        max_num = pow(10,nb_digits)-1
        if len(map_c2w) <= max_num:
            raise ValueError("ERROR: the number of words is not enough "
                            "againt the nb_digits, "
                            f"{len(map_c2w)}(given)<={max_num}")
        # set self vars.
        self.word_file = word_file
        self.nb_digits = nb_digits
        self.nb_blocks = nb_blocks
        self.map_type = map_type
        self.max_num = max_num
        # make maps.
        map_c2w = map_c2w[:max_num+1]
        if map_type not in [1,2,3]:
            raise ValueError("ERROR: map_type must be either 1,2,or 3, "
                             f"but {map_type}.")
        if map_type in [1,3]:
            self.map_c2w = map_c2w[:max_num+1]
        if map_type in [2,3]:
            self.map_w2c = dict([(v,k) for k,v in enumerate(map_c2w)])

    def words2code(self, words: str) -> str:
        """
        converting a given word into the code.
        given words: e.g. "かいだん-おわり-ゆしゅつ" -> "060-684-351"
        @return code.
        """
        if self.map_type not in [2,3]:
            raise ValueError("ERROR: map_type must set to 2 or 3 "
                             "to call words2code() "
                             "when CodeWordMap class was generated.")
        code_w = words.split("-")
        if len(code_w) != self.nb_blocks:
            raise ValueError("ERROR: nb_blocks doesn't match the given words, "
                             f"{len(words)}(given)!={self.nb_blocks}.")
        code_n = []
        for cw in code_w:
            n = self.map_w2c.get(cw)
            if n is None:
                raise ValueError(f"ERROR: the word {cw} doesn't exist.")
            code_n.append(str(n).rjust(self.nb_digits,"0"))
        return { "code": "-".join(code_n), "version": self.version }

    def code2words(self, code: str) -> str:
        """
        converting a given code into the N words.
        code: e.g. "060-684-351" -> "かいだん-おわり-ゆしゅつ"
        @return N words.
        """
        code_n = code.split("-")
        if len(code_n) != self.nb_blocks:
            raise ValueError("ERROR: nb_blocks doesn't match the given code, "
                             f"{len(code_n)}(given)!={self.nb_blocks}.")
        code_w = []
        for n in code_n:
            if len(n) < self.nb_digits:
                raise ValueError("ERROR: nb_digits doesn't match the given "
                                 f"code len, {n}(given)!={self.nb_digits}.")
            num = int(n)
            if num > self.max_num:
                raise ValueError("ERROR: a code in a block must be less "
                                 f"than {1+self.max_num}.")
            code_w.append(self.map_c2w[num])
        return { "words": "-".join(code_w), "version": self.version }

    def basen(self, n: int, base: int) -> list:
        if base < 2:
            raise ValueError("base must be > 1")
        d = []
        while n >= base:
            n,k = n//base,n%base
            d.append(k)
        d.append(n)
        return list(reversed(d))

    def gencodebase(self) -> list:
        n = hashlib.sha1(int(datetime.timestamp(datetime.now()) +
                             random.random()*1E15).to_bytes(8,"big")).digest()
        return self.basen(int.from_bytes(n,"big"), base=self.max_num+1)

    def gencode(self) -> (str, str):
        """
        generating a set of code and N words.
        @return code and N words.
        """
        code_w = []
        code_n = []
        for n in self.gencodebase()[-self.nb_blocks:]:
            code_w.append(self.map_c2w[n])
            code_n.append(str(n).rjust(self.nb_digits,"0"))
        return { "code": "-".join(code_n), "words": "-".join(code_w),
                "version": self.version }

if __name__ == "__main__":
    from argparse import ArgumentParser
    from argparse import ArgumentDefaultsHelpFormatter
    ap = ArgumentParser(
            description="code2words generates code "
                        "or convert code to words vice varsa.",
            formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("word_file",
                    help="specify a filename containing the word list.")
    ap.add_argument("-w", action="store", dest="code2words",
                    help="specify a code to convert into words.")
    ap.add_argument("-c", action="store", dest="words2code",
                    help="specify words to convert into code.")
    ap.add_argument("--nb-blocks", "-b", action="store", dest="nb_blocks",
                    type=int, default=3,
                    help="specify the number of blocks.")
    ap.add_argument("--nb-digits", "-g", action="store", dest="nb_digits",
                    type=int, default=4,
                    help="specify the number of digits in a block.")
    opt = ap.parse_args()
    if opt.code2words:
        cwm = CodeWordMap(opt.word_file, nb_digits=opt.nb_digits,
                          nb_blocks=opt.nb_blocks, map_type=1)
        print(cwm.code2words(opt.code2words))
    elif opt.words2code:
        cwm = CodeWordMap(opt.word_file, nb_digits=opt.nb_digits,
                          nb_blocks=opt.nb_blocks, map_type=2)
        print(cwm.words2code(opt.words2code))
    else:
        cwm = CodeWordMap(opt.word_file, nb_digits=opt.nb_digits,
                          nb_blocks=opt.nb_blocks, map_type=3)
        print(cwm.gencode())

