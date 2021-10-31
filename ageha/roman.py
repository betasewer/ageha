
capital_roman = NumeralParser("ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ", offset=1)
small_roman = NumeralParser("ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ", offset=1)
kakomisuuji = NumeralParser("①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳㉑㉒㉓㉔㉕㉖㉗㉘㉙㉚㉛㉜㉝㉞㉟㊱㊲㊳㊴㊵㊶㊷㊸㊹㊺㊻㊼㊽㊾㊿", offset=1)



#
#
#
class AlphaRomanParser():
    def __init__(self):
        self.letters = [
            (1, ("i", "I", "ｉ", "Ｉ")),
            (5, ("v", "V", "ｖ", "Ｖ")),
            (10, ("x", "X", "ｘ", "Ｘ")),
        ]
        
    def detect(self, text):
        letters = []
        for _, x in self.letters:
            letters.extend(x)
        return text[0] in letters
        
    def __call__(self, text):
        digit = []
        for ch in text:
            num = next((n for (n,letters) in self.letters if ch in letters), None)
            if num is not None:
                if len(digit)>0 and digit[-1] < num:
                    digit[-1] = -digit[-1]
                digit.append(num)
            else:
                raise NumeralParseError(text)
        return sum(digit)
        
parse_alpha_roman = AlphaRomanParser()