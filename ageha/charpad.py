import unicodedata


class Uchar:
    """ @type
    ユニコード文字
    """
    def __init__(self, chr, name, code, number, category, eawidth):
        self._ch = chr
        self._name = name
        self._code = code
        self._number = number
        self._category = category
        self._eawidth = eawidth

    def __add__(self, r):
        """ 
        Returns: 
            Str:
        """
        if not isinstance(r, Uchar):
            raise TypeError(r)
        return self.char() + r.char()
    
    def char(self):
        """ @method
        文字。
        Returns:
            Str:
        """
        return self._ch
    
    def name(self):
        """ @method
        文字についた名前。
        Returns:
            Str:
        """
        return self._name
        
    def code(self):
        """ @method
        文字を示すコード。
        Returns:
            Int:
        """
        return self._code
    
    def number(self):
        """ @method
        文字が意味する数値。
        Returns:
            Float:
        """
        return self._number
    
    def category(self):
        """ @method
        ユニコードのカテゴリ名。
        Returns:
            Str:
        """
        return self._category
    
    def east_asian_width(self):
        """ @method
        全角か半角か。
        Returns:
            Str:
        """
        return self._eawidth
    
    def bidirectional(self):
        """ @method
        文字に割り当てられた双方向クラス。
        Returns:
            Str:
        """
        return unicodedata.bidirectional(self._ch)
    
    def combining(self):
        """ @method
        文字に割り当てられた正規結合クラス。
        Returns:
            Str:
        """ 
        com = unicodedata.combining(self._ch)
        return com if com != 0 else ""
        
    def mirrored(self):
        """ @method
        鏡像化のプロパティ
        Returns:
            Bool:
        """         
        mirr = unicodedata.mirrored(self._ch)
        return True if mirr == 1 else False
    
    def decomposition(self):
        """ @method
        文字に割り当てられた文字分解マッピング。
        Returns:
            Str:
        """         
        return unicodedata.decomposition(self._ch)

    #
    #
    #
    @classmethod
    def fromchar(cls, ch, code=None):
        if code is None: code = ord(ch)
        return cls(
            ch,
            name = unicodedata.name(ch, None),
            code = code,
            number = unicodedata.numeric(ch, None),
            category = unicodedata.category(ch),
            eawidth = unicodedata.east_asian_width(ch)   
        )

    @classmethod
    def fromname(cls, name, code=None):
        ch = unicodedata.lookup(name)
        if code is None: code = ord(ch)
        return cls(
            ch,
            name = name,
            code = code,
            number = unicodedata.numeric(ch, None),
            category = unicodedata.category(ch),
            eawidth = unicodedata.east_asian_width(ch)   
        )

    def constructor(self, context, value):
        """ @meta
        Params:
            Int|Str: code | char
        """
        if isinstance(value, int):
            ch = chr(value)
            code = value
        else:
            if len(value) == 1:
                ch = value
            else:
                ch = unicodedata.lookup(value)
            code = ord(ch)
        return Uchar.fromchar(ch, code)
        
    def stringify(self):
        """ @meta """
        return "'{}' ({}) {}".format(self._ch, self._code, self._name)
    
    def pprint(self, app):
        """ @meta """
        import textwrap
        app.post("message", textwrap.dedent(
        """
        char: {}
        name: {}
        code: {:0X}
        category: {}
        east asian width: {}
        """.format(self._ch, self._name, self._code, self._category, self._eawidth)))


#
# 名前の検索に特化した文字クラス
#
class Alpha(Uchar):
    """ @type
    アルファベット。
    """
    def _with_combine(self, mark):
        """ 結合記号を付す。 """
        chars = [self._ch, mark]
        return unicodedata.normalize("NFC", "".join(chars))

    def accent(self):
        """ @method
        アキュート・アクセントを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0301))

    def grave_accent(self):
        """ @method
        グレイヴ・アクセントを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0300))
    
    def circumflex(self):
        """ @method [cir]
        サーカムフレックスを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0302))
        
    def tilde(self):
        """ @method
        チルダを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0303))
        
    def macron(self):
        """ @method
        マクロンを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0304))
        
    def breve(self):
        """ @method
        ブレーヴェ・アクセントを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0304))
        
    def caron(self):
        """ @method [hacek]
        カロンを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x030C))

    def trema(self):
        """ @method
        トレマを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0308))

    def cedilla(self):
        """ @method
        セディーユを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0327))

    def ogonek(self):
        """ @method
        オゴネクを結合する。
        Returns:
            Str:
        """
        return self._with_combine(chr(0x0328))

    def constructor(self, context, value):
        """ @meta
        Params:
            Str: name
        """
        lang, sep, roman = value.partition("/")
        if sep:
            romans = lang_romans.get(lang.lower())
            if romans is None:
                raise ValueError("変換表がない言語です: {}".format(lang))
            ch = romans.get(roman)
            if ch is None:
                raise ValueError("文字の割り当てがありません: {}".format(ch))
            return Alpha.fromchar(ch)
        else:        
            return Alpha.fromchar(value)


class CharMap():
    def __init__(self):
        self._map = None

    def get(self, roman):
        if self._map is None:
            self._map = self.load()
        return self._map.get(roman)

    def load(self):
        raise NotImplementedError()

class _LatinRoman(CharMap):
    def load(self):
        return {
            "ae" : chr(0x00E6),
            "AE" : chr(0x00C6),
            "oe" : chr(0x0153),
            "OE" : chr(0x0152)
        }

class _RussianRoman(CharMap):
    pass

class _PolishRoman(CharMap):
    pass

class _OCSRoman(CharMap):
    pass

lang_romans = {}
for elems in [
    ("la", "latin", _LatinRoman()),
    ("ru", "russian", _RussianRoman()),
    ("pl", "polish", _PolishRoman()),
    ("ocs", _OCSRoman()),
]:  
    for name in elems[:-1]:
        lang_romans[name] = elems[-1]



class Combining(Uchar):
    """ @type
    結合文字。
    """
    def constructor(self, context, value):
        """ @meta
        Params:
            Str: name
        """
        if not isinstance(value, str):
            raise TypeError(value)
        value = Combining.convert_to_ucdname(value)
        return Combining.fromname(value)

    @classmethod
    def convert_to_ucdname(cls, mark):
        if mark == "acute":
            mark = "acute-accent"
        elif mark == "grave":
            mark = "grave-accent"
        elif mark == "accent":
            mark = "acute-accent"
        elif mark.startswith("small"):
            parts = mark.split("-")
            if len(parts) >= 2:
                if parts[1] == "capital":
                    mark = "latin-letter-" + mark
                else:
                    mark = "latin-small-letter" + mark[len("small"):]

        name = " ".join([x.capitalize().replace("_","-") for x in mark.split("-")])
        return "Combining {}".format(name)


    
class Shape(Uchar):
    """ @type
    図形。
    """
    def constructor(self, context, value):
        """ @meta
        Params:
            Str|Int: name
        """
        if not isinstance(value, (int, str)):
            raise TypeError(value)
        ch = Shape.symbols.get(str(value))
        if ch is None:
            raise ValueError("文字の割り当てがありません")
        return Shape.fromchar(ch)        

    class _SymbolMap(CharMap):
        def load(self):
            return {
                "triangle" : chr(0x25B2),
                "square" : chr(0x25A0),
                "diamond" : chr(0x25C6),
                "circle" : chr(0x25CF),
                "lozenge" : chr(0x25CA),
                "star" : chr(0x2605),
                "3" : chr(0x25B2),
                "4" : chr(0x25A0),
                "0" : chr(0x25CF)
            }
    symbols = _SymbolMap()

    class _TriMap(CharMap):
        def load(self):
            return {
                "black" : chr(0x25B2),
                "white" : chr(0x25B3)
            }

    # triangle Shape white up
    