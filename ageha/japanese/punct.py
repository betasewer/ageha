
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
    ("「",   "",     L_PAREN|WABUN, "かっこ", ),
    ("」",   "",     R_PAREN|WABUN, "かっこ", ),
    ("『",   "",     L_PAREN|WABUN, "二重;にじゅう", ),
    ("』",   "",     R_PAREN|WABUN, "二重;にじゅう", ),
    ("（",  "(",    L_PAREN|WABUN, "丸;まる", ),
    ("）",  ")",    R_PAREN|WABUN, "丸;まる", ),
    ("〈",   "‹",    L_PAREN|WABUN, "山;やま", ),
    ("〉",   "›",    R_PAREN|WABUN, "山;やま", ),
    ("《",   "«",    L_PAREN|WABUN, "二重山;にじゅうやま", ),
    ("》",   "»",    R_PAREN|WABUN, "二重山;にじゅうやま", ),
    ("〔",   "",     L_PAREN|WABUN, "亀甲;きっこう", ),
    ("〕",   "",     R_PAREN|WABUN, "亀甲;きっこう", ),
    ("［",  "[",    L_PAREN|WABUN, "角;大;かく;だい",),
    ("］",  "]",    R_PAREN|WABUN, "角;大;かく;だい",),
    ("【",   "",     L_PAREN|WABUN, "隅付き;すみつき"),
    ("】",   "",     R_PAREN|WABUN, "隅付き;すみつき"),
    ("｛",  "{",    L_PAREN|WABUN, "波;なみ",),
    ("｝",  "}",    R_PAREN|WABUN, "波;なみ",),
    ("〝",  "“",    L_PAREN|WABUN, "ちょんちょん"),
    ("〟",  "”",    R_PAREN|WABUN, "ちょんちょん"),
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

    # 引用符の和文への変換
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

    # 棒
    (chr(0x2010),   "",   WABUN, "ハイフン"),            # ‐ HYPHEN
    (chr(0x2010),   "",   OOBUN, "hyphen"),           # ‐ HYPHEN 
    (chr(0x2011),   chr(0x2010),  WABUN|CONVERT, ""), # ‑ NON-BREAKING HYPHEN
    (chr(0x2012),   chr(0x2010),  WABUN|CONVERT, ""), # ‒ FIGURE DASH
    (chr(0x2013),   chr(0x2010),  WABUN|CONVERT, ""), # – EN DASH
    ("︲",          chr(0x2010),  WABUN|CONVERT, ""), # PRESENTATION FORM FOR VERTICAL EN DASH 
    (chr(0x002D),   chr(0x2010),  WABUN|CONVERT, ""), # - HYPHEN MINUS
    (chr(0x2212),   chr(0x2010),  WABUN|CONVERT, ""), # − MINUS (MATH)
    (chr(0xFF0D),   chr(0x2010),  WABUN|CONVERT, ""), # － FULLWIDTH HYPHEN-MINUS

    (chr(0x2015),   chr(0x2014),  WABUN, "ダッシュ;ダーシ"), # ― HORIZONTAL BAR 
    (chr(0x2014),   chr(0x2015),  OOBUN, "dash"),       # — EM DASH
    (chr(0x2014),   chr(0x2015),  WABUN|CONVERT, ""),   # — EM DASH
    (chr(0x2E3A),   chr(0x2015),  WABUN|CONVERT, ""),   # ⸺ TWO EM DASH
    (chr(0x2E3B),   chr(0x2015),  WABUN|CONVERT, ""),   # ⸻ THREE EM DASH
    ("︱",          chr(0x2015),  WABUN|CONVERT, ""),   # PRESENTATION FORM FOR VERTICAL EM DASH 
    (chr(0xFF5C),   chr(0x2015),  WABUN|CONVERT, ""),   # ｜ FULLWIDTH VERTICAL LINE
    (chr(0xFFE8),   chr(0x2015),  WABUN|CONVERT, ""),   # ￨ HALFWIDTH FORMS LIGHT VERTICAL 
    (chr(0x2500),   chr(0x2015),  WABUN|CONVERT, ""),   # ─ BOX DRAWINGS LIGHT HORIZONTAL （罫線）
    (chr(0x2502),   chr(0x2015),  WABUN|CONVERT, ""),   # │ BOX DRAWINGS LIGHT VERTICAL （罫線）

    # リーダ
    (chr(0x2026), "...", WABUN, "リーダ"),           # … HORIZONTAL ELLIPSIS 
    (chr(0xFE19), chr(0x2026), WABUN|CONVERT, ""), # PRESENTATION FORM FOR VERTICAL HORIZONTAL ELLIPSIS 
    (chr(0x221E), chr(0x2026), WABUN|CONVERT, ""), # ⋮ VERTICAL ELLIPSIS 
    (chr(0x205D), chr(0x2026), WABUN|CONVERT, ""), # ⁝ TRICOLON 
    (chr(0x205E), chr(0x2026), WABUN|CONVERT, ""), # ⁞ VERTICAL DOTS
    (chr(0x22EF), chr(0x2026), WABUN|CONVERT, ""), #  ⋯ MIDLINE HORIZONTAL ELLIPSIS (MATH) 
    (chr(0x2025), chr(0x2026), WABUN|CONVERT, ""), # ‥ TWO DOT LEADER 

    # 中黒
    (chr(0x30FB), "", WABUN, "中黒;なかぐろ"),               # KATAKANA MIDDLE DOT  
    (chr(0xFF65), chr(0x30FB), WABUN|CONVERT, "半角中黒"), # HALFWIDTH KATAKANA MIDDLE DOT
    
    # 音引き
    (chr(0x30FC), "", WABUN, "音引き;おんびき"),            # ー KATAKANA-HIRAGANA PROLONGED SOUND MARK 
    (chr(0xFF70), chr(0x30FC), WABUN|CONVERT, ""),       # ｰ HALFWIDTH KATAKANA-HIRAGANA PROLONGED SOUND MARK 

    # 波ダッシュ・チルダ
    ("~", chr(0xFF5E), OOBUN, "tilde"),                 # 007E TILDE
    (chr(0x301C), "~", WABUN, "波ダッシュ"),               # 301C WAVE DASH
    ("~", chr(0x301C), WABUN|CONVERT, ""),              # 007E
    (chr(0xFF5E), chr(0x301C), WABUN|CONVERT, ""),      # FF5E FULLWIDTH TILDE
    (chr(0x2053), chr(0x301C), WABUN|CONVERT, ""),      # 2053 SWUNG DASH

    # その他
    ("#", "＃", OOBUN, "sharp"),
    ("＃", "#", WABUN, "シャープ"),    
    ("$", "＄", OOBUN, "dollar"),
    ("＄", "$", WABUN, "ドル"),
    ("%", "％", OOBUN, "percent"),
    ("％", "%", WABUN, "パーセント"),
    ("&", "＆", OOBUN, "ampersand;and"),
    ("＆", "&", WABUN, "アンパサンド;アンド"),
    ("*", "＊", OOBUN, "asterisk"),
    ("＊", "*", WABUN, "アステリ"),
    ("+", "＋", OOBUN, "plus"),
    ("＋", "+", WABUN, "プラス"),
    ("/", "／", OOBUN, "solidus;slash"),
    ("／", "/", WABUN, "スラッシュ"),
    ("\\", "＼", OOBUN, "reverse-solidus;backslash"),
    ("＼", "\\", WABUN, "バックスラッシュ"),
    ("=", "＝", OOBUN, "equal"),
    ("＝", "=", WABUN, "イコール"),
    ("@", "＠", OOBUN, "atmark"),
    ("＠", "@", WABUN, "アットマーク"),
    ("^", "＾", OOBUN, "circumflex"),
    ("＾", "^", WABUN, "サーカムフレックス"),
    ("`", "｀", OOBUN, "grave"),
    ("｀", "`", WABUN, "グレーヴ"),
    ("|", "｜", OOBUN, "verticalline"),
    ("｜", "|", WABUN, "縦線"),
    ("_", "＿", OOBUN, "underscore"),
    ("＿", "_", WABUN, "アンダーバー"),

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
