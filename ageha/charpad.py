import unicodedata


class Unichar:
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
    def combine(self, *marks):
        """ @method
        結合文字を付して、NFCで正規化する。
        Params:
            *marks(str): 結合文字の名前
        Returns:
            Str:
        """
        chars = []
        chars.append(self._ch)
        for mark in marks:
            ucdname = convert_to_ucdname(mark)
            markchar = unicodedata.lookup(ucdname)
            chars.append(markchar)
        ch = unicodedata.normalize("NFC", "".join(chars))
        return ch

    #
    #
    #
    @classmethod
    def fromchar(cls, ch, code=None):
        if code is None: code = ord(ch)
        return Unichar(
            ch,
            name = unicodedata.name(ch, None),
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
        return Unichar.fromchar(ch, code)
        
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


def convert_to_ucdname(mark):
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



    
    