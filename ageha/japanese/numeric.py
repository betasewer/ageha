#!/usr/bin/env python3
# coding: utf-8
import re

from ageha.numeric import compose_number

#
#
#
class NumeralParseError(Exception):
    pass

    
class KansuujiNumeral():
    def __init__(self) -> None:
        self.numbers = "〇一二三四五六七八九"
        self.subunits = ("十", "百", "千")
        self.hiunits  = ("万", "億", "兆", "京", "垓", "𥝱", "穣", "溝", "澗", "正", "載", "極", "恒河沙", "阿僧祇", "那由他", "不可思議", "無量大数")
    
    def detect(self, text):
        ch = text[0]
        return ch in self.numbers or ch in self.subunits or ch in self.hiunits[:6] # 穣以降は誤検出の可能性あり

    def get_unitchar(self, exp):
        key = exp % 4
        if key != 0:
            return self.subunits[key-1]
        key = exp // 4
        if key != 0:
            return self.hiunits[key-1]
        return None
    
    def get_digits(self, value):
        if not isinstance(value, str):
            value = str(value)

        digits = []
        for ch in value:
            digit = int(ch)
            digits.append(digit)
        digits.reverse()
        return digits

    def parse(self, text, *, strict=True):
        """ 
        漢数字を数値に変換する。十式、〇式両方に対応。
        Params:
            text(str):
        Returns:
            int:
        """
        num = 0
        digbuf = []
        subdigit = 0
        hiunitbuf = []
        def checkbufempty(buf):
            if len(buf)>0:
                if strict:
                    raise ValueError("解釈不能な文字: " + "".join(buf))
                else:
                    buf.clear()
            
        for ch in text:
            if ch in self.numbers:
                d = self.numbers.find(ch)
                digbuf.append(d)
                checkbufempty(hiunitbuf)
                continue
            elif ch in self.subunits:
                exp = self.subunits.index(ch) + 1
                if len(digbuf) == 0:
                    digbuf.append(1)
                subdigit += compose_number(exp, digbuf)
                digbuf.clear()
                checkbufempty(hiunitbuf)
                continue
            
            hiunitbuf.append(ch)
            for i, hiunit in enumerate(self.hiunits):
                s = "".join(hiunitbuf)
                if hiunit == s:
                    exp = 4 * (i + 1)
                    if digbuf:
                        num += compose_number(exp, digbuf)
                        digbuf.clear()
                    if subdigit:
                        num += subdigit * 10 ** exp
                        subdigit = 0
                    hiunitbuf.clear()

            if len(hiunitbuf) > 3:
                hiunitbuf = hiunitbuf[1:]

        if digbuf:
            num += compose_number(0, digbuf)
        if subdigit:
            num += subdigit
        checkbufempty(hiunitbuf)

        return num
    
    def unit_write(self, value):
        """ すべての単位語を明記（十式） """
        chars = []
        for exp, d in enumerate(self.get_digits(value)):
            if d == 0:
                continue
            
            uc = self.get_unitchar(exp)
            if uc is not None:
                chars.append(uc)
            
            if d == 1 and (0 < exp and exp < 4): # 万以下の単位では一をつけない
                continue
            else:
                c = self.numbers[d]
                chars.append(c) 

        if not chars:
            return self.numbers[0] # ゼロ
        return "".join(reversed(chars))

    def write(self, value):
        """ 4桁ごとの単位語を明記（〇式） """
        chars = []
        subdigits = ""
        for exp, d in enumerate(self.get_digits(value)):
            if (exp % 4) == 0:
                uc = self.get_unitchar(exp)
                if uc is not None:
                    chars.extend([x for x in subdigits.rstrip("〇")]) # 下位桁の左の余った〇を削除する（逆転しているので右から）
                    subdigits = ""
                    chars.append(uc)
            
            c = self.numbers[d]
            subdigits += c
        
        if subdigits:
            chars.extend(subdigits)
            
        return "".join(reversed(chars))

    def nounit_write(self, value):
        """ 単位語なし """
        chars = []
        for d in self.get_digits(value):
            c = self.numbers[d]
            chars.append(c)
        return "".join(reversed(chars))
    
#
kansuuji = KansuujiNumeral()
parse_kansuuji = kansuuji.parse
write_kansuuji = kansuuji.write
write_unit_kansuuji = kansuuji.unit_write

        
#
#
#
class KanBasic:
    def constructor(self, value):
        """ @meta """
        return parse_kansuuji(value)

class Kan(KanBasic):
    """ @type subtype
    単位語なしの漢数字
    BaseType:
        Int: 
    """
    def stringify(self, value):
        """ @meta """
        return kansuuji.nounit_write(value)

class Kan10(KanBasic):
    """ @type subtype
    単位語を明記する漢数字
    BaseType:
        Int: 
    """
    def stringify(self, value):
        """ @meta """
        return kansuuji.unit_write(value)

class Kan1000(KanBasic):
    """ @type subtype
    4桁ごとの単位語を明記する漢数字
    BaseType:
        Int: 
    """
    def stringify(self, value):
        """ @meta """
        return kansuuji.write(value)



