import string
import unicodedata

#
#
#
def compose_number(baseexp, digits):
    """
    Params:
        baseexp(int): 基底の10の対数
        digits(Sequence[int]): 各桁のリスト（左から右の順）
    """
    return sum(x * 10 ** (baseexp + d) for d,x in zip(range(len(digits)), reversed(digits)))

#
# 
#
class BijectiveNumeric:
    def __init__(self, letters):
        self.letters = letters
    
    @property
    def base(self):
        return len(self.letters)
    
    def write(self, num):
        """
        数値をこの記数に変換する
        Params:
            num(int):
        Returns:
            str:
        """
        m = num + 1 # 1ベースにする
        k = self.base
        digits = []
        while True:
            q = (m-1) // k
            d = m - q * k
            digit = self.letters[d-1]
            digits.append(digit)
            if m <= k:
                break
            m = q
        return "".join(reversed(digits))
    
    def parse(self, text):
        """
        この記数を数値に変換する
        Params:
            text(str):
        Returns:
            str:
        """
        num = 0
        for i, ch in enumerate(reversed(text)):
            d = self.letters.index(ch) + 1
            num += d * pow(self.base, i)
        return num-1

ABCNumeric = BijectiveNumeric(string.ascii_uppercase)



def parse_decimal(text):
    """
    ユニコードでDecimalあるいはDigitに関連付けられた数値に変換し、10進数値を返す
    """
    digits = []
    for ch in text:
        dig = unicodedata.decimal(ch, None)
        if dig is None:
            dig = unicodedata.digit(ch, None)
            if dig is None:
                continue
        digits.append(dig)
    return compose_number(0, digits)



