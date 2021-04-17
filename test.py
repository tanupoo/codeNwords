
word_file = "word_list.txt"

import codeNwords

cwm = codeNwords.CodeWordMap(word_file)

print("## generation")
ret = cwm.gencode()
print(ret)
print(cwm.code2words(ret["code"]))
print(cwm.words2code(ret["words"]))

print("## conversion")
words = "さわぐ-もでる-くつした"
expected = "497-892-234"
code = cwm.words2code(words)
print(f"{words} -> {code}: result {code==expected}: expected {expected}")
if code != expected:
    raise ValueError(f"{code} != {expected}")

code = "324-243-133"
expected = "たてる-ゆうはん-ごめん"
words = cwm.code2words(code)
print(f"{code} -> {words}: result {words==expected}: expected {expected}")
if words != expected:
    raise ValueError(f"{words} != {expected}")
