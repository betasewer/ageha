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
    def fromchar(cls, ch, code=None, **kwargs):
        if code is None: code = ord(ch)
        return cls(
            ch,
            name = unicodedata.name(ch, None),
            code = code,
            number = unicodedata.numeric(ch, None),
            category = unicodedata.category(ch),
            eawidth = unicodedata.east_asian_width(ch),
            **kwargs
        )

    @classmethod
    def fromname(cls, name, code=None, **kwargs):
        ch = unicodedata.lookup(name)
        if code is None: code = ord(ch)
        return cls(
            ch,
            name = name,
            code = code,
            number = unicodedata.numeric(ch, None),
            category = unicodedata.category(ch),
            eawidth = unicodedata.east_asian_width(ch),
            **kwargs
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

#
#
#
class DelayTable():
    def __init__(self, loader):
        self._map = None
        self._load = loader

    def get(self, key):
        # 辞書から検索
        self.load()
        if not isinstance(self._map, dict):
            raise TypeError()
        
        return self._map.get(key)

    def search(self, keys):
        # リストから1つ検索
        return next(self.search_all(keys), None)
    
    def search_all(self, keys):
        # リストからすべて検索
        self.load()
        if not isinstance(self._map, list):
            raise TypeError()
        
        left = set(keys)
        for value, vkeys in self._map:
            if left.issubset(set(vkeys)):
                yield value
        
    def load(self):
        if self._map is None:
            self._map = self._load()
        return self._map

#
#
#
@DelayTable
def latin_roman():
    return {
        "ae" : chr(0x00E6),
        "AE" : chr(0x00C6),
        "oe" : chr(0x0153),
        "OE" : chr(0x0152)
    }

@DelayTable
def russian_roman():
    pass

@DelayTable
def polish_roman():
    pass

@DelayTable
def ocs_roman():
    pass

lang_romans = {}
for elems in [
    ("la", "latin", latin_roman),
    ("ru", "russian", russian_roman),
    ("pl", "polish", polish_roman),
    ("ocs", ocs_roman),
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
    幾何学模様を表す文字。
    """
    # 形
    TRI = 0x0001 # 0x25B2
    SQUARE = 0x0002 # 0x25A0
    DIAMOND = 0x0003 # 0x25C6
    CIRCLE = 0x0004 # 0x25CF
    LOZENGE = 0x0005 # 0x25CA
    STAR = 0x0006 # 0x2605
    RECT = 0x0007 # 0x2605
    ARC = 0x0008
    # 色
    BLACK = 0x1000
    WHITE = 0x2000
    HATCH = 0x3000 # 網掛け
    BLACKWHITE = 0x4000 # 白黒
    # 向き
    LEFT  = 0x10000
    RIGHT = 0x20000
    UP    = 0x30000
    DOWN  = 0x40000
    #
    SMALL = 0x100000
    LARGE = 0x200000


    def __init__(self, chr, name, code, number, category, eawidth, *, shapecodes):
        super().__init__(chr, name, code, number, category, eawidth)
        self._shapecodes = shapecodes

    def constructor(self, context, value):
        """ @meta
        Params:
            Str|Int: name
        """
        if not isinstance(value, (int, str)):
            raise TypeError(value)

        codes = []
        for name in str(value).split("-"):
            code = Shape._component_names.get(name.lower())
            if code is None:
                raise ValueError("無効な要素: ".format(name))
            codes.append(code)
        
        chcode = Shape._components.search(codes)
        if chcode is None:
            raise ValueError("該当する文字はありません")

        return Shape.fromchar(chr(chcode), chcode, shapecodes=codes)

    def vary(self):
        """@method
        同じ特徴をもつ他の形を挙げる。
        Returns:
            Sheet[Shape](@):
        """
        chcodes = Shape._components.search_all(self._shapecodes)
        return [Shape.fromchar(chr(x), x, shapecodes=self._shapecodes) for x in chcodes]

    @DelayTable
    def _component_names():
        return {
            "triangle" : Shape.TRI,
            "square" : Shape.SQUARE,
            "diamond" : Shape.DIAMOND,
            "circle" : Shape.CIRCLE,
            "lozenge" : Shape.LOZENGE,
            "star" : Shape.STAR,
            "rect" : Shape.RECT,
            "arc" : Shape.ARC,
            "3" : Shape.TRI,
            "4" : Shape.SQUARE,
            "5" : Shape.STAR,
            "0" : Shape.CIRCLE,
            "up" : Shape.UP,
            "down" : Shape.DOWN,
            "left" : Shape.LEFT,
            "right" : Shape.RIGHT,
            "black" : Shape.BLACK,
            "white" : Shape.WHITE,
            "blackwhite" : Shape.BLACKWHITE,
            "hatch" : Shape.HATCH,
            "large" : Shape.LARGE,
            "small" : Shape.SMALL,
        }

    @DelayTable
    def _components():
        return [
            # 基本形
            (0x25B2, (Shape.BLACK, Shape.TRI, Shape.UP)), # BLACK UP-POINTING TRIANGLE
            (0x25A0, (Shape.BLACK, Shape.SQUARE)), # BLACK SQUARE
            (0x25C6, (Shape.BLACK, Shape.DIAMOND)), # BLACK DIAMOND
            (0x25CF, (Shape.BLACK, Shape.CIRCLE)), # BLACK CIRCLE
            (0x2605, (Shape.BLACK, Shape.STAR)), # BLACK STAR
            (0x25CA, (Shape.WHITE, Shape.LOZENGE)), # LOZENGE
            (0x25AC, (Shape.BLACK, Shape.RECT)), # BLACK RECTANGLE
            # バリエーション
            (0x25A1, (Shape.WHITE, Shape.SQUARE)), # WHITE SQUARE
            (0x25A2, (Shape.WHITE, Shape.SQUARE)), # WHITE SQUARE WITH ROUNDED CORNERS
            (0x25A3, (Shape.WHITE, Shape.SQUARE)), # WHITE SQUARE CONTAINING BLACK SMALL SQUARE
            (0x25A4, (Shape.HATCH, Shape.SQUARE)), # SQUARE WITH HORIZONTAL FILL
            (0x25A5, (Shape.HATCH, Shape.SQUARE)), # SQUARE WITH VERTICAL FILL
            (0x25A6, (Shape.HATCH, Shape.SQUARE)), # SQUARE WITH ORTHOGONAL CROSSHATCH FILL
            (0x25A7, (Shape.HATCH, Shape.SQUARE)), # SQUARE WITH UPPER LEFT TO LOWER RIGHT FILL
            (0x25A8, (Shape.HATCH, Shape.SQUARE)), # SQUARE WITH UPPER RIGHT TO LOWER LEFT FILL
            (0x25A9, (Shape.HATCH, Shape.SQUARE)), # SQUARE WITH DIAGONAL CROSSHATCH FILL
            (0x25AA, (Shape.BLACK, Shape.SQUARE, Shape.SMALL)), # BLACK SMALL SQUARE
            (0x25AB, (Shape.WHITE, Shape.SQUARE, Shape.SMALL)), # WHITE SMALL SQUARE
            (0x25AD, (Shape.WHITE, Shape.RECT)), # WHITE RECTANGLE
            (0x25AE, (Shape.BLACK, Shape.RECT)), # BLACK VERTICAL RECTANGLE
            (0x25AF, (Shape.WHITE, Shape.RECT)), # WHITE VERTICAL RECTANGLE
            (0x25B0, (Shape.BLACK, Shape.RECT)), # BLACK PARALLELOGRAM
            (0x25B1, (Shape.WHITE, Shape.RECT)), # WHITE PARALLELOGRAM
            (0x25B3, (Shape.WHITE, Shape.TRI, Shape.UP)), # WHITE UP-POINTING TRIANGLE
            (0x25B4, (Shape.BLACK, Shape.TRI, Shape.UP, Shape.SMALL)), # BLACK UP-POINTING SMALL TRIANGLE
            (0x25B5, (Shape.WHITE, Shape.TRI, Shape.UP, Shape.SMALL)), # WHITE UP-POINTING SMALL TRIANGLE
            (0x25B6, (Shape.BLACK, Shape.TRI, Shape.RIGHT)), # BLACK RIGHT-POINTING TRIANGLE
            (0x25B7, (Shape.WHITE, Shape.TRI, Shape.RIGHT)), # WHITE RIGHT-POINTING TRIANGLE
            (0x25B8, (Shape.BLACK, Shape.TRI, Shape.RIGHT, Shape.SMALL)), # BLACK RIGHT-POINTING SMALL TRIANGLE
            (0x25B9, (Shape.WHITE, Shape.TRI, Shape.RIGHT, Shape.SMALL)), # WHITE RIGHT-POINTING SMALL TRIANGLE
            (0x25BA, (Shape.BLACK, Shape.TRI, Shape.RIGHT)), # BLACK RIGHT-POINTING POINTER
            (0x25BB, (Shape.WHITE, Shape.TRI, Shape.RIGHT)), # WHITE RIGHT-POINTING POINTER
            (0x25BC, (Shape.BLACK, Shape.TRI, Shape.DOWN)), # BLACK DOWN-POINTING TRIANGLE
            (0x25BD, (Shape.WHITE, Shape.TRI, Shape.DOWN)), # WHITE DOWN-POINTING TRIANGLE
            (0x25BE, (Shape.BLACK, Shape.TRI, Shape.DOWN, Shape.SMALL)), # BLACK DOWN-POINTING SMALL TRIANGLE
            (0x25BF, (Shape.WHITE, Shape.TRI, Shape.DOWN, Shape.SMALL)), # WHITE DOWN-POINTING SMALL TRIANGLE
            (0x25C0, (Shape.BLACK, Shape.TRI, Shape.LEFT)), # BLACK LEFT-POINTING TRIANGLE
            (0x25C1, (Shape.WHITE, Shape.TRI, Shape.LEFT)), # WHITE LEFT-POINTING TRIANGLE
            (0x25C2, (Shape.BLACK, Shape.TRI, Shape.LEFT, Shape.SMALL)), # BLACK LEFT-POINTING SMALL TRIANGLE
            (0x25C3, (Shape.WHITE, Shape.TRI, Shape.LEFT, Shape.SMALL)), # WHITE LEFT-POINTING SMALL TRIANGLE
            (0x25C4, (Shape.BLACK, Shape.TRI, Shape.LEFT)), # BLACK LEFT-POINTING POINTER
            (0x25C5, (Shape.WHITE, Shape.TRI, Shape.LEFT)), # WHITE LEFT-POINTING POINTER
            (0x25C7, (Shape.WHITE, Shape.DIAMOND)), # WHITE DIAMOND
            (0x25C8, (Shape.WHITE, Shape.DIAMOND)), # WHITE DIAMOND CONTAINING BLACK SMALL DIAMOND
            (0x25CB, (Shape.WHITE, Shape.CIRCLE)), # WHITE CIRCLE
            (0x25CC, (Shape.HATCH, Shape.CIRCLE)), # DOTTED CIRCLE
            (0x25CD, (Shape.HATCH, Shape.CIRCLE)), # CIRCLE WITH VERTICAL FILL
            (0x25C9, (Shape.BLACKWHITE, Shape.CIRCLE)), # FISHEYE
            (0x25CE, (Shape.WHITE, Shape.CIRCLE)), # BULLSEYE
            (0x25D0, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.LEFT)), # CIRCLE WITH LEFT HALF BLACK
            (0x25D1, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.RIGHT)), # CIRCLE WITH RIGHT HALF BLACK
            (0x25D2, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.DOWN)), # CIRCLE WITH LOWER HALF BLACK
            (0x25D3, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.UP)), # CIRCLE WITH ABOVE HALF BLACK
            (0x25D4, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.UP, Shape.RIGHT)), # CIRCLE WITH UPPER RIGHT QUADRANT BLACK
            (0x25D5, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.UP, Shape.LEFT)),  # CIRCLE WITH ALL BUT UPPER LEFT QUADRANT BLACK
            (0x25D6, (Shape.BLACK, Shape.LEFT, Shape.CIRCLE)), # LEFT HALF BLACK CIRCLE
            (0x25D7, (Shape.BLACK, Shape.RIGHT, Shape.CIRCLE)), # RIGHT HALF BLACK CIRCLE
            (0x25D8, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.SMALL)), # INVERSE BULLET
            (0x25D9, (Shape.BLACKWHITE, Shape.CIRCLE)), # INVERSE WHITE CIRCLE
            (0x25DA, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.UP)), # UPPER HALF INVERSE WHITE CIRCLE
            (0x25DB, (Shape.BLACKWHITE, Shape.CIRCLE, Shape.DOWN)), # LOWER HALF INVERSE WHITE CIRCLE
            (0x25DC, (Shape.ARC, Shape.UP, Shape.LEFT)), # UPPER LEFT QUADRANT CIRCULAR ARC
            (0x25DD, (Shape.ARC, Shape.UP, Shape.RIGHT)), # UPPER RIGHT QUADRANT CIRCULAR ARC
            (0x25DE, (Shape.ARC, Shape.DOWN, Shape.LEFT)), # LOWER LEFT QUADRANT CIRCULAR ARC
            (0x25DF, (Shape.ARC, Shape.DOWN, Shape.RIGHT)), # LOWER RIGHT QUADRANT CIRCULAR ARC
            (0x25E0, (Shape.ARC, Shape.UP)), # UPPER HALF CIRCLE
            (0x25E1, (Shape.ARC, Shape.DOWN)), # LOWER HALF CIRCLE
            (0x25E2, (Shape.BLACK, Shape.TRI, Shape.DOWN, Shape.RIGHT)), # BLACK LOWER RIGHT TRIANGLE
            (0x25E3, (Shape.BLACK, Shape.TRI, Shape.DOWN, Shape.LEFT)), # BLACK LOWER LEFT TRIANGLE
            (0x25E4, (Shape.BLACK, Shape.TRI, Shape.UP, Shape.RIGHT)), # BLACK UPPER RIGHT TRIANGLE
            (0x25E5, (Shape.BLACK, Shape.TRI, Shape.UP, Shape.LEFT)), # BLACK UPPER LEFT TRIANGLE
            (0x25E6, (Shape.WHITE, Shape.CIRCLE, Shape.SMALL)), # WHITE BULLET
            (0x25E7, (Shape.BLACKWHITE, Shape.SQUARE, Shape.LEFT)), # SQUARE WITH LEFT HALF BLACK
            (0x25E8, (Shape.BLACKWHITE, Shape.SQUARE, Shape.RIGHT)), # SQUARE WITH RIGHT HALF BLACK
            (0x25E9, (Shape.BLACKWHITE, Shape.SQUARE, Shape.LEFT, Shape.UP)), # SQUARE WITH UPPER LEFT DIAGONAL BLACK
            (0x25EA, (Shape.BLACKWHITE, Shape.SQUARE, Shape.RIGHT, Shape.DOWN)), # SQUARE WITH LOWER RIGHT DIAGONAL BLACK
            (0x25EB, (Shape.WHITE, Shape.SQUARE)), # WHITE SQUARE WITH VERTICAL BISECTING LINE
            (0x25EC, (Shape.WHITE, Shape.TRI)), # WHITE UP-POINTING TRIANGLE WITH DOTS
            (0x25ED, (Shape.BLACKWHITE, Shape.TRI, Shape.LEFT)), # UP-POINTING TRIANGLE WITH LEFT HALF BLACK
            (0x25EE, (Shape.BLACKWHITE, Shape.TRI, Shape.RIGHT)), # UP-POINTING TRIANGLE WITH RIGHT HALF BLACK
            (0x25EF, (Shape.WHITE, Shape.CIRCLE, Shape.LARGE)), # LARGE CIRCLE
            (0x25F0, (Shape.WHITE, Shape.SQUARE, Shape.UP, Shape.LEFT)), # WHITE SQUARE WITH UPPER LEFT QUADRANT
            (0x25F1, (Shape.WHITE, Shape.SQUARE, Shape.DOWN, Shape.LEFT)), # WHITE SQUARE WITH LOWER LEFT QUADRANT
            (0x25F2, (Shape.WHITE, Shape.SQUARE, Shape.DOWN, Shape.RIGHT)), # WHITE SQUARE WITH LOWER RIGHT QUADRANT
            (0x25F3, (Shape.WHITE, Shape.SQUARE, Shape.UP, Shape.RIGHT)), # WHITE SQUARE WITH UPPER RIGHT QUADRANT
            (0x25F4, (Shape.WHITE, Shape.CIRCLE, Shape.UP, Shape.LEFT)), # WHITE CIRCLE WITH UPPER LEFT QUADRANT
            (0x25F5, (Shape.WHITE, Shape.CIRCLE, Shape.DOWN, Shape.LEFT)), # WHITE CIRCLE WITH LOWER LEFT QUADRANT
            (0x25F6, (Shape.WHITE, Shape.CIRCLE, Shape.DOWN, Shape.RIGHT)), # WHITE CIRCLE WITH LOWER RIGHT QUADRANT
            (0x25F7, (Shape.WHITE, Shape.CIRCLE, Shape.UP, Shape.RIGHT)), # WHITE CIRCLE WITH UPPER RIGHT QUADRANT
            (0x25F8, (Shape.WHITE, Shape.TRI, Shape.UP, Shape.LEFT)),  # UPPER LEFT TRIANGLE
            (0x25F9, (Shape.WHITE, Shape.TRI, Shape.UP, Shape.RIGHT)),  # UPPER RIGHT TRIANGLE
            (0x25FA, (Shape.WHITE, Shape.TRI, Shape.DOWN, Shape.LEFT)), # LOWER LEFT TRIANGLE
            (0x25FF, (Shape.WHITE, Shape.TRI, Shape.DOWN, Shape.RIGHT)), # LOWER RIGHT TRIANGLE
            (0x25FB, (Shape.WHITE, Shape.SQUARE)), # WHITE MEDIUM SQUARE
            (0x25FC, (Shape.BLACK, Shape.SQUARE)), # BLACK MEDIUM SQUARE
            (0x25FD, (Shape.WHITE, Shape.SQUARE, Shape.SMALL)), # WHITE MEDIUM SMALL SQUARE
            (0x25FE, (Shape.BLACK, Shape.SQUARE, Shape.SMALL)), # BLACK MEDIUM SMALL SQUARE
            (0x2606, (Shape.WHITE, Shape.STAR)), # WHITE STAR
        ]
        

    