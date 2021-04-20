# XXX need to use unittest.

word_file = "word_list.txt"

import codeNwords

cwm = codeNwords.CodeWordMap(word_file)

print("## generation")
ret = cwm.gencode()
print(ret)
print(cwm.code2words(ret["code"]))
print(cwm.words2code(ret["words"]))

print("## conversion")
words = "ちゅうがた-すたじあむ-すぺいん"
expected = "6812-9567-1599"
code = cwm.words2code(words)["code"]
print(f"{words} -> {code}: result {code==expected}: expected {expected}")
if code != expected:
    raise ValueError(f"{code} != {expected}")

code = "0324-0243-0133"
expected = "わらう-しゅくだい-よろしい"
words = cwm.code2words(code)["words"]
print(f"{code} -> {words}: result {words==expected}: expected {expected}")
if words != expected:
    raise ValueError(f"{words} != {expected}")

try:
    codeNwords.CodeWordMap(word_file, map_type=0)
except ValueError:
    print("caught ValueError for map_type check.")
