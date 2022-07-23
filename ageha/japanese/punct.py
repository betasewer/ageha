
#
#
#

WABUN    = 0x0001
OOBUN    = 0x0002
CONVERT  = 0x0004
L_PAREN  = 0x1000
R_PAREN  = 0x2000

#
# --------------------------------
# char, convert-char, name, bits
char_table = [
    # 和文句読点
    ("、",   ", ",      WABUN, "読点;てん", ),
    ("。",   "",        WABUN, "句点;まる", ),
    ("！",  "!",       WABUN, "感嘆符", ),
    ("？",  "?",       WABUN, "疑問符", ),
    ("；",   ";",      WABUN, "セミコロン", ),
    ("：",   ":",      WABUN, "コロン", ),
    (chr(0xFF61), "。", WABUN|CONVERT, "半角句点"),
    (chr(0xFF64), "、", WABUN|CONVERT, "半角読点"),
    (chr(0xFF0E), "。", WABUN|CONVERT, "全角ピリオド"), 
    (chr(0xFF0C), "、", WABUN|CONVERT, "全角コンマ"), 

    # 欧文句読点
    (",",   "、",     OOBUN, "comma", ),
    (".",   "",      OOBUN, "period", ), # 小数点などにも使われるので変換しない
    (";",   "；",    OOBUN, "semicolon", ),
    (":",   "：",    OOBUN, "colon", ),
    ("!",   "！",    OOBUN, "exclamation", ),
    ("?",   "？",    OOBUN, "interrogation", ),

    # 和文括弧
    ("「",   "",     L_PAREN|WABUN, "kakko;かっこ", ),
    ("」",   "",     R_PAREN|WABUN, "kakko;かっこ", ),
    ("『",   "",     L_PAREN|WABUN, "double-kakko;二重;にじゅう", ),
    ("』",   "",     R_PAREN|WABUN, "double-kakko;二重;にじゅう", ),
    ("（",  "(",    L_PAREN|WABUN, "maru-kakko;丸;まる", ),
    ("）",  ")",    R_PAREN|WABUN, "maru-kakko;丸;まる", ),
    ("〈",   "‹",    L_PAREN|WABUN, "yama-kakko;山;やま", ),
    ("〉",   "›",    R_PAREN|WABUN, "yama-kakko;山;やま", ),
    ("《",   "«",    L_PAREN|WABUN, "double-yama-kakko;二重山;にじゅうやま", ),
    ("》",   "»",    R_PAREN|WABUN, "double-yama-kakko;二重山;にじゅうやま", ),
    ("〔",   "",     L_PAREN|WABUN, "kikko-kakko;亀甲;きっこう", ),
    ("〕",   "",     R_PAREN|WABUN, "kikko-kakko;亀甲;きっこう", ),
    ("［",  "[",    L_PAREN|WABUN, "dai-kakko;bracket;角;大;かく;だい",),
    ("］",  "]",    R_PAREN|WABUN, "dai-kakko;bracket;角;大;かく;だい",),
    ("【",   "",     L_PAREN|WABUN, "sumi-kakko;隅付き;すみつき"),
    ("】",   "",     R_PAREN|WABUN, "sumi-kakko;隅付き;すみつき"),
    ("｛",  "{",    L_PAREN|WABUN, "nami-kakko;brace;波;なみ",),
    ("｝",  "}",    R_PAREN|WABUN, "nami-kakko;brace;波;なみ",),
    ("〝",  "“",    L_PAREN|WABUN, "tyontyon;ちょんちょん"),
    ("〟",  "”",    R_PAREN|WABUN, "tyontyon;ちょんちょん"),
    ("＜",  "〈",    L_PAREN|WABUN|CONVERT, ""),
    ("＞",  "〉",    R_PAREN|WABUN|CONVERT, ""),
    ("≺",  "〈",    L_PAREN|WABUN|CONVERT, ""),
    ("≻",  "〉",    R_PAREN|WABUN|CONVERT, ""),
    ("〈",  "〉",     R_PAREN|WABUN|CONVERT, ""),
    ("〉",  "〉",     R_PAREN|WABUN|CONVERT, ""),
    ("≪",  "《",    L_PAREN|WABUN|CONVERT, ""),
    ("≫",  "》",    R_PAREN|WABUN|CONVERT, ""),

    # 欧文括弧・引用符
    ("(",   "（",   L_PAREN|OOBUN, "paren", ),
    (")",   "）",   R_PAREN|OOBUN, "paren", ),
    ("«",    "《",   L_PAREN|OOBUN, "guillemet;ギュメ", ),
    ("»",    "》",   R_PAREN|OOBUN, "guillemet;ギュメ", ),
    ("‹",   "〈",    L_PAREN|OOBUN, "一重ギュメ", ),
    ("›",   "〉",    R_PAREN|OOBUN, "一重ギュメ", ),
    ("[",   "［",   L_PAREN|OOBUN, "bracket", ),
    ("]",   "］",   R_PAREN|OOBUN, "bracket", ),
    ("{",   "｛",   L_PAREN|OOBUN, "brace", ),
    ("}",   "｝",   R_PAREN|OOBUN, "brace", ),
    # ("‘",   "〝",    L_PAREN|OOBUN, "quotation", ),
    # ("’",   "",     R_PAREN|OOBUN, "quotation", ), # クォーテーションマークに使われうるので変換しない
    ("‚",   "〝",     L_PAREN|OOBUN, "reversed-quotation", ),
    ("‛",   "〟",     R_PAREN|OOBUN, "reversed-quotation", ),
    ("“",   "〝",   L_PAREN|OOBUN, "double-quotation", ),
    ("”",   "〟",   R_PAREN|OOBUN, "double-quotation", ),
    ("„",   "〝",   L_PAREN|OOBUN, "reversed-double-quotation", ),
    ("‟",   "〟",   R_PAREN|OOBUN, "reversed-double-quotation", ),
    #("'",   "‘",    R_PAREN|OOBUN|CONVERT, "", ),
    #("'",   "’",    L_PAREN|OOBUN|CONVERT, "", ),
    #('"',   "“",    R_PAREN|OOBUN|CONVERT, "", ),
    #('"',   "”",    L_PAREN|OOBUN|CONVERT, "", ),

    # 欧文引用符の和文への変換
    #("‘",   "〝",     L_PAREN|WABUN|CONVERT, "", ), 
    #("’",   "〟",     R_PAREN|WABUN|CONVERT, "", ), クォーテーションマークに使われうるので変換しない
    ("‚",   "〝",     L_PAREN|WABUN|CONVERT, "", ),
    ("‛",   "〟",     R_PAREN|WABUN|CONVERT, "", ),
    ("“",   "〝",     L_PAREN|WABUN|CONVERT, "", ),
    ("”",   "〟",     R_PAREN|WABUN|CONVERT, "", ),
    ("„",   "〝",     L_PAREN|WABUN|CONVERT, "", ),
    ("‟",   "〟",     R_PAREN|WABUN|CONVERT, "", ),
    ("'",   "＇",     L_PAREN|WABUN|CONVERT, "", ), # とりあえず目につきやすくする
    ('"',   "＂",     R_PAREN|WABUN|CONVERT, "", ), # とりあえず目につきやすくする

    # アポストロフィ
    (chr(0x2019), "", OOBUN, "apostrophe"),
    (chr(0x0027), chr(0x2019), OOBUN|CONVERT, ""),  # 楔形からオタマジャクシ形への変換 -> 2019 RIGHT SINGLE QUOTATION MARK 
    (chr(0x02BC), chr(0x2019), OOBUN|CONVERT, ""),  # 02BC MODIFIER LETTER APOSTROPHE

    # 短い棒
    (chr(0x2010),   "",   WABUN, "hyphen;ハイフン"),     # ‐ HYPHEN
    (chr(0x2010),   "",   OOBUN, "hyphen"),           # ‐ HYPHEN 
    ## 和文での変換　- 一括してHYPHENに
    (chr(0x2011),   chr(0x2010),  WABUN|CONVERT, ""), # ‑ NON-BREAKING HYPHEN
    (chr(0x2012),   chr(0x2010),  WABUN|CONVERT, ""), # ‒ FIGURE DASH
    (chr(0x2013),   chr(0x2010),  WABUN|CONVERT, ""), # – EN DASH
    ("︲",          chr(0x2010),  WABUN|CONVERT, ""), # PRESENTATION FORM FOR VERTICAL EN DASH 
    (chr(0x002D),   chr(0x2010),  WABUN|CONVERT, ""), # - HYPHEN MINUS
    (chr(0x2212),   chr(0x2010),  WABUN|CONVERT, ""), # − MINUS (MATH)
    (chr(0xFF0D),   chr(0x2010),  WABUN|CONVERT, ""), # － FULLWIDTH HYPHEN-MINUS
    ## 欧文での変換　- EN DASH, HYPHEN-MINUSに
    (chr(0x2011),   chr(0x2013),  OOBUN|CONVERT, ""), # ‑ NON-BREAKING HYPHEN
    (chr(0x2012),   chr(0x2013),  OOBUN|CONVERT, ""), # ‒ FIGURE DASH
    ("︲",          chr(0x2013),  OOBUN|CONVERT, ""), # PRESENTATION FORM FOR VERTICAL EN DASH 
    (chr(0x2212),   chr(0x002D),  OOBUN|CONVERT, ""), # − MINUS (MATH)
    (chr(0xFF0D),   chr(0x002D),  OOBUN|CONVERT, ""), # － FULLWIDTH HYPHEN-MINUS

    # 長い棒
    (chr(0x2015),   chr(0x2014),  WABUN, "dash;ダッシュ;ダーシ"),  # ― HORIZONTAL BAR 
    (chr(0x2014),   chr(0x2015),  OOBUN, "dash"),              # — EM DASH
    ## 和文での変換　- 一括してHORIZONTAL BARに
    (chr(0x2014),   chr(0x2015),  WABUN|CONVERT, ""),   # — EM DASH
    (chr(0x2E3A),   chr(0x2015),  WABUN|CONVERT, ""),   # ⸺ TWO EM DASH
    (chr(0x2E3B),   chr(0x2015),  WABUN|CONVERT, ""),   # ⸻ THREE EM DASH
    ("︱",          chr(0x2015),  WABUN|CONVERT, ""),   # PRESENTATION FORM FOR VERTICAL EM DASH 
    (chr(0xFF5C),   chr(0x2015),  WABUN|CONVERT, ""),   # ｜ FULLWIDTH VERTICAL LINE
    (chr(0xFFE8),   chr(0x2015),  WABUN|CONVERT, ""),   # ￨ HALFWIDTH FORMS LIGHT VERTICAL 
    (chr(0x2500),   chr(0x2015),  WABUN|CONVERT, ""),   # ─ BOX DRAWINGS LIGHT HORIZONTAL （罫線）
    (chr(0x2502),   chr(0x2015),  WABUN|CONVERT, ""),   # │ BOX DRAWINGS LIGHT VERTICAL （罫線）
    ## 欧文での変換　- EM DASHとHORIZONTAL BARに
    ("︱",          chr(0x2014),  OOBUN|CONVERT, ""),   # PRESENTATION FORM FOR VERTICAL EM DASH 
    (chr(0x2E3A),   chr(0x2015),  OOBUN|CONVERT, ""),   # ⸺ TWO EM DASH
    (chr(0x2E3B),   chr(0x2015),  OOBUN|CONVERT, ""),   # ⸻ THREE EM DASH
    (chr(0xFF5C),   chr(0x2015),  OOBUN|CONVERT, ""),   # ｜ FULLWIDTH VERTICAL LINE
    (chr(0xFFE8),   chr(0x2015),  OOBUN|CONVERT, ""),   # ￨ HALFWIDTH FORMS LIGHT VERTICAL 
    (chr(0x2500),   chr(0x2015),  OOBUN|CONVERT, ""),   # ─ BOX DRAWINGS LIGHT HORIZONTAL （罫線）
    (chr(0x2502),   chr(0x2015),  OOBUN|CONVERT, ""),   # │ BOX DRAWINGS LIGHT VERTICAL （罫線）

    # リーダ
    (chr(0x2026), "...", WABUN, "leader;リーダ"),         # … HORIZONTAL ELLIPSIS 
    ## 和文での変換
    (chr(0xFE19), chr(0x2026), WABUN|CONVERT, ""),      # PRESENTATION FORM FOR VERTICAL HORIZONTAL ELLIPSIS 
    (chr(0x221E), chr(0x2026), WABUN|CONVERT, ""),      # ⋮ VERTICAL ELLIPSIS 
    (chr(0x205D), chr(0x2026), WABUN|CONVERT, ""),      # ⁝ TRICOLON 
    (chr(0x205E), chr(0x2026), WABUN|CONVERT, ""),      # ⁞ VERTICAL DOTS
    (chr(0x22EF), chr(0x2026), WABUN|CONVERT, ""),      #  ⋯ MIDLINE HORIZONTAL ELLIPSIS (MATH) 
    (chr(0x2025), chr(0x2026), WABUN|CONVERT, ""),      # ‥ TWO DOT LEADER 
    ## 欧文での変換
    (chr(0xFE19), "...", OOBUN|CONVERT, ""),      # PRESENTATION FORM FOR VERTICAL HORIZONTAL ELLIPSIS 
    (chr(0x221E), "...", OOBUN|CONVERT, ""),      # ⋮ VERTICAL ELLIPSIS 
    (chr(0x205D), "...", OOBUN|CONVERT, ""),      # ⁝ TRICOLON 
    (chr(0x205E), "...", OOBUN|CONVERT, ""),      # ⁞ VERTICAL DOTS
    (chr(0x22EF), "...", OOBUN|CONVERT, ""),      #  ⋯ MIDLINE HORIZONTAL ELLIPSIS (MATH) 
    (chr(0x2025), "...", OOBUN|CONVERT, ""),      # ‥ TWO DOT LEADER 

    # 中黒
    (chr(0x30FB), "", WABUN, "nakaguro;中黒;なかぐろ"),               # KATAKANA MIDDLE DOT  
    (chr(0xFF65), chr(0x30FB), WABUN|CONVERT, "半角中黒"), # HALFWIDTH KATAKANA MIDDLE DOT
    
    # 音引き
    (chr(0x30FC), "", WABUN, "onbiki;音引き;おんびき"),            # ー KATAKANA-HIRAGANA PROLONGED SOUND MARK 
    (chr(0xFF70), chr(0x30FC), WABUN|CONVERT, ""),       # ｰ HALFWIDTH KATAKANA-HIRAGANA PROLONGED SOUND MARK 

    # 波ダッシュ・チルダ
    ("~", chr(0xFF5E), OOBUN, "tilde"),                 # 007E TILDE
    (chr(0x301C), "~", WABUN, "wave-dash;波ダッシュ"),     # 301C WAVE DASH
    ("~",         chr(0x301C), WABUN|CONVERT, ""),      # 007E
    (chr(0xFF5E), chr(0x301C), WABUN|CONVERT, ""),      # FF5E FULLWIDTH TILDE
    (chr(0x2053), chr(0x301C), WABUN|CONVERT, ""),      # 2053 SWUNG DASH
    (chr(0xFF5E), "~",         OOBUN|CONVERT, ""),      # FF5E FULLWIDTH TILDE
    (chr(0x2053), "~",         OOBUN|CONVERT, ""),      # 2053 SWUNG DASH

    # その他
    ("#", "＃", OOBUN, "sharp"),
    ("＃", "#", WABUN, "sharp;シャープ"),    
    ("$", "＄", OOBUN, "dollar"),
    ("＄", "$", WABUN, "dollar;ドル"),
    ("%", "％", OOBUN, "percent"),
    ("％", "%", WABUN, "percent;パーセント"),
    ("&", "＆", OOBUN, "ampersand;and"),
    ("＆", "&", WABUN, "ampersand;アンパサンド;アンド"),
    ("*", "＊", OOBUN, "asterisk"),
    ("＊", "*", WABUN, "asterisk;アステリ"),
    ("+", "＋", OOBUN, "plus"),
    ("＋", "+", WABUN, "plus;プラス"),
    ("/", "／", OOBUN, "solidus;slash"),
    ("／", "/", WABUN, "slash;スラッシュ"),
    ("\\", "＼", OOBUN, "reverse-solidus;backslash"),
    ("＼", "\\", WABUN, "backslash;バックスラッシュ"),
    ("=", "＝", OOBUN, "equal"),
    ("＝", "=", WABUN, "equal;イコール"),
    ("@", "＠", OOBUN, "atmark"),
    ("＠", "@", WABUN, "atmark;アットマーク"),
    ("^", "＾", OOBUN, "circumflex"),
    ("＾", "^", WABUN, "circumflex;サーカムフレックス"),
    ("`", "｀", OOBUN, "grave"),
    ("｀", "`", WABUN, "grave;グレーヴ"),
    ("|", "｜", OOBUN, "vertical-line"),
    ("｜", "|", WABUN, "vertical-line縦線"),
    ("_", "＿", OOBUN, "underscore"),
    ("＿", "_", WABUN, "underscode;アンダーバー"),

    # 縦書き用記号
    ("︵", "（",    L_PAREN|WABUN|CONVERT, ""),
    ("︶", "）",    R_PAREN|WABUN|CONVERT, ""),
    ("︷", "｛",    L_PAREN|WABUN|CONVERT, ""),
    ("︸", "｝",    R_PAREN|WABUN|CONVERT, ""),
    ("︹", "〔",     L_PAREN|WABUN|CONVERT, ""),
    ("︺", "〕",     R_PAREN|WABUN|CONVERT, ""),
    ("﹇", "［",    L_PAREN|WABUN|CONVERT, ""),
    ("﹈", "］",    R_PAREN|WABUN|CONVERT, ""),
    ("︻", "【",     L_PAREN|WABUN|CONVERT, ""),
    ("︼", "】",     R_PAREN|WABUN|CONVERT, ""),
    ("﹁", "「",     L_PAREN|WABUN|CONVERT, ""),
    ("﹂", "」",     R_PAREN|WABUN|CONVERT, ""),
    ("﹃", "『",     L_PAREN|WABUN|CONVERT, ""),
    ("﹄", "』",     R_PAREN|WABUN|CONVERT, ""),
    ("︿", "〈",     L_PAREN|WABUN|CONVERT, ""),
    ("﹀", "〉",     R_PAREN|WABUN|CONVERT, ""),
    ("︽", "《",     L_PAREN|WABUN|CONVERT, ""),
    ("︾", "》",     R_PAREN|WABUN|CONVERT, ""),
]

twochar_table = [
    (chr(0x002D)+chr(0x002D), chr(0x2014), OOBUN|CONVERT, ""),  # ハイフンマイナス二つでEM DASHに変換する
    (chr(0x30FC)+chr(0x30FC), chr(0x2015)+chr(0x2015), WABUN|CONVERT, ""), # 二倍の音引きは二倍ダッシュに変換する
]


# U+2000-206F 一般句読点
# U+3000-3030 CJKの記号（句読点、括弧）
# U+FF00-FFAF 半角形／全角形 Halfwidth and Fullwidth Forms

#
#
#
def glob_entry(text, *, dest=False):
    for entry in char_table:
        char, destchar, _f, _n = entry
        if text[-1] == char and (not dest or destchar):
            yield entry
    for entry in twochar_table:
        char, destchar, _f, _n = entry
        if text == char and (not dest or destchar):
            yield entry


def convert(this, text):
    """
    Params:
        this(int): 文のタイプを示す定数
        text(str): 
    Returns:
        str: 
    """
    result = ""

    buf = ""
    for ch in text:
        buf += ch
        
        convchar = None
        for entry in glob_entry(buf, dest=True):
            _curchar, destchar, flags, _name = entry
            if flags & (this|CONVERT):
                convchar = destchar
                break
            elif (flags & this) == 0:
                convchar = destchar
                break
        
        if convchar is not None:
            if len(convchar) > 1:
                off = len(convchar)-1
                result = result[:-off]
            result += convchar
        else:
            result += ch

        if len(buf) > 1:
            buf = buf[1:]

    return result


def tate_convert(text):
    """
    縦書きの和文に適した約物に変換する。
    Params:
        text(str): 
    Returns:
        str: 
    """
    return convert(WABUN, text)


def wabun_convertible_chars(chars):
    """
    和文上で変換すべき文字である場合はエントリを返す。
    """
    for entry in glob_entry(chars):
        _curchar, destchar, flags, _name = entry
        if flags & (WABUN|CONVERT) == (WABUN|CONVERT):
            yield entry
        #if (flags & OOBUN and flags & CONVERT == 0):
        #    yield entry

def oobun_convertible_chars(chars):
    """
    欧文上で変換すべき文字である場合はエントリを返す。
    """
    for entry in glob_entry(chars):
        _curchar, destchar, flags, _name = entry
        if (flags & (OOBUN|CONVERT) == (OOBUN|CONVERT)):
            yield entry
        if (flags & WABUN and flags & CONVERT == 0):
            yield entry

def lookup_chars(instruction):
    """
    名前で文字を探し出す。
    """
    cf = 0
    flags, sep, name = instruction.partition("/")
    if sep:
        if "ou" in flags or "欧" in flags:
            cf |= OOBUN
        if "wa" in flags or "和" in flags:
            cf |= WABUN
        if "convert" in flags:
            cf |= CONVERT
        if "left" in flags or "左" in flags:
            cf |= L_PAREN
        if "right" in flags or "右" in flags:
            cf |= R_PAREN
    else:
        name = instruction
    
    if cf == 0:
        cf = WABUN|OOBUN
    
    chars = {}
    for entry in char_table:
        char, _dest, f, cname = entry
        if cf & f == 0:
            continue
        if name in cname.split(";"):
            if L_PAREN & f:
                chars["l"] = char
                continue
            elif R_PAREN & f:
                chars["r"] = char
                break
            else:
                chars["c"] = char
                break

    if len(chars) == 0:
        raise ValueError("Unknown")
    return chars

    
def lookup_langtype(ch):
    """
    文字で検索して欧文・和文の別を調べる。
    """
    for entry in char_table:
        char, _dest, f, cname = entry
        if ch == char:
            if WABUN & f and (CONVERT & f) == 0:
                return "wa"
            elif OOBUN & f and (CONVERT & f) == 0:
                return "ou"
    return None


#
#
#
class Punct:
    """ @type
    約物に素早くアクセスする。
    """
    def __init__(self, entry):
        self._entry = entry
        
    def char(self):
        """ @method
        Returns:
            Str:
        """
        if "c" in self._entry:
            return self._entry["c"]
        elif "l" in self._entry and "r" in self._entry:
            return self._entry["l"] + " " + self._entry["r"]
        else:
            raise ValueError("No entry")
        
    def enclose(self, text):
        """ @method
        Params:
            text(Str):
        Returns:
            Str:
        """
        if "c" in self._entry:
            return self._entry["c"] + text + self._entry["c"]
        elif "l" in self._entry and "r" in self._entry:
            return self._entry["l"] + text + self._entry["r"]
        else:
            raise ValueError("No entry")
    
    def copy(self, spirit):
        """ @task
        クリップボードにコピーする。
        """
        spirit.clipboard_copy(self.char())    
        
    def constructor(self, value):
        """ @meta
        Params:
            Str:
        """
        chars = lookup_chars(value)
        return Punct(chars)
        
    def stringify(self):
        """ @meta
        """
        return "{}".format(self.char())
        
