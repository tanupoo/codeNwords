
word_file = "word_list.txt"

import codeNwords

cwm = codeNwords.CodeWordMap(word_file)
ret = cwm.gencode()
print(ret)
print(cwm.code2words(ret["code"]))
print(cwm.words2code(ret["words"]))

words = "さわぐ-もでる-くつした"
expected = "500-897-234"
code = cwm.words2code(words)
print(f"{words} -> {code}: expected {expected}")

code = "324-243-133"
expected = "たてる-ゆうはん-ごめん"
words = cwm.code2words(code)
print(f"{code} -> {words}: expected {expected}")
