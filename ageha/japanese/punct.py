from ageha.char.table import CharEntry, CharTable

"""
name: punctuations

[klass]
    OPEN: open 開
    CLOSE: close 閉
    WIDE: wide 全
    HALF: half 半
    TATE: tate 縦
    YOKO: !TATE yoko 横

[読点 てん ten]
WIDE: 、
HALF: 0xFF64

[hyphen ハイフン]
char: -

[exclamation 感嘆符]
char: 

[interrogation 疑問符]
char: 

[semicolon セミコロン]
char: 

[sumi-kakko 隅付き括弧 すみつきかっこ]
OPEN: 【
CLOSE: 】
TATE+OPEN: ︻
TATE+CLOSE: ︼

[paren]
OPEN: (
CLOSE: )
*WIDE: maru-kakko
"""


@CharTable
def punctuations(t):
    _punct = t.add
    _punctat = t.get

    OPEN  = t.klass("open", "開")
    CLOSE = t.klass("close", "閉")
    WIDE  = t.klass("wide", "全")
    HALF  = t.klass("half", "半")
    TATE  = t.klass("tate", "縦")
    t.klass("yoko", "横", negate=TATE)

    # 句読点
    _punct("読点","てん").adds(
        (WIDE, "、"), (HALF, chr(0xFF64)),
    )
    _punct("句点","まる").adds(
        (WIDE, "。"), (HALF, chr(0xFF61)),
    )
    _punct("exclamation", "感嘆符").adds(
        (WIDE, "！"), (HALF, "!")
    )
    _punct("interrogation", "疑問符").adds(
        (WIDE, "？"), (HALF, "?")
    )
    _punct("semicolon","セミコロン").adds(
        (HALF, ";"), (WIDE, "；"), 
    )
    _punct("colon","コロン").adds(
        (HALF, ":"), (WIDE, "：")
    )
    _punct("comma").adds(
        (HALF, ","), (WIDE, chr(0xFF0C))
    )
    _punct("period").adds(
        (HALF, "."), (WIDE, chr(0xFF0E)), # 小数点などにも使われるので変換しない
    )
    
    # 和文括弧
    _punct("kakko","かっこ").adds(
        (OPEN, "「"), (CLOSE, "」"),
        (TATE|OPEN, "﹁"), (TATE|CLOSE, "﹂"),
    )
    _punct("double-kakko","二重括弧","にじゅうかっこ").adds(
        (OPEN, "『"), (CLOSE, "』"),
        (TATE|OPEN, "﹃"), (TATE|CLOSE, "﹄"),
    )
    _punct("maru-kakko","丸括弧","まるかっこ").adds(
		(OPEN, "（"), (CLOSE, "）"),
        (TATE|OPEN, "︵"), (TATE|CLOSE, "︶"),
	)
    _punct("yama-kakko","山括弧","やまかっこ").adds(
		(OPEN, "〈"), (CLOSE, "〉"),
        (TATE|OPEN, "︿"), (TATE|CLOSE, "﹀")
	)
    _punct("double-yama-kakko","二重山括弧","にじゅうやまかっこ").adds(
		(OPEN, "《"), (CLOSE, "》"),
        (TATE|OPEN, "︽"), (TATE|CLOSE, "︾")
	)
    _punct("kikko-kakko","亀甲括弧","きっこうかっこ").adds(
		(OPEN, "〔"), (CLOSE, "〕"),
        (TATE|OPEN, "︹"), (TATE|CLOSE, "︺")
	)
    _punct("dai-kakko","bracket","角括弧","大括弧","かくかっこ","だいかっこ").adds(
		(OPEN, "［"), (CLOSE, "］"),
        (TATE|OPEN, "﹇"), (TATE|CLOSE, "﹈"),
	)
    _punct("sumi-kakko","隅付き括弧","すみつきかっこ").adds(
		(OPEN, "【"), (CLOSE, "】"),
        (TATE|OPEN, "︻"), (TATE|CLOSE, "︼")
	)
    _punct("nami-kakko","brace","波括弧","なみかっこ").adds(
		(OPEN, "｛"), (CLOSE, "｝"),
        (TATE|OPEN, "︷"), (TATE|CLOSE, "︸")
	)
    _punct("tyontyon","ちょんちょん").adds(
		(OPEN, "〝"), (CLOSE, "〟")
	)
    _punct("greater", "大なり").adds(
        "＜"    # FF1C FULLWIDTH LESS-THAN SIGN 
    )
    _punct("less", "小なり").adds(
        "＞"    # FF1E FULLWIDTH GREATER-THAN SIGN 
    )
    _punct("precedes").adds(
        "≺"
    )
    _punct("succeeds").adds(
        "≻"
    )
    _punct("angle-bracket").adds(
		(OPEN, "〈"), (CLOSE, "〉")
	)
    _punct("much-greater").adds(
        "≫" 
    )
    _punct("much-less").adds(
		"≪"
	)

    # 欧文括弧・引用符
    _punct("paren").adds(
        (OPEN, "("), (CLOSE, ")"),
        (WIDE, _punctat("maru-kakko"), HALF)
    )
    _punct("guillemet","ギュメ").adds(
		(OPEN, "«"), (CLOSE, "»")
	)
    _punct("一重ギュメ").adds(
		(OPEN, "‹"), (CLOSE, "›")
	)
    _punct("bracket").adds(
		(OPEN, "["), (CLOSE, "]"),
        (WIDE, _punctat("dai-kakko"), HALF)
	)
    _punct("brace").adds(
		(OPEN, "{"), (CLOSE, "}"),
        (WIDE, _punctat("nami-kakko"), HALF)
	)
    _punct("quotation").adds( # クォーテーションマークに使われうるので変換しない
		(OPEN, "‘"), (CLOSE, "’")
	)  
    _punct("reversed-quotation").adds(
		(OPEN, "‚"), (CLOSE, "‛")
	)
    _punct("double-quotation").adds(
		(OPEN, "“"), (CLOSE, "”")
	)
    _punct("reversed-double-quotation").adds(
		(OPEN, "„"), (CLOSE, "‟")
	)
    _punct("solid-quotation").adds(
        '"'
    )
    
    # アポストロフィ
    _punct("solid-apostrophe","アポストロフィ").adds(
        "'"  # 楔形からオタマジャクシ形への変換 -> 2019 CLOSE SINGLE QUOTATION MARK 
    )
    _punct("apostrophe","アポストロフィ").adds(
        chr(0x2019)
    )
    _punct("mod-apostrophe").adds(
        chr(0x02BC),  # 02BC MODIFIER LETTER APOSTROPHE
    )
    
    # 短い棒
    _punct("hyphen","ハイフン").adds(
        chr(0x2010), # ‐ HYPHEN
    )
    _punct("non-breaking-hyphen").adds(
        chr(0x2011),  # ‑ NON-BREAKING HYPHEN
    )
    _punct("figure-dash").adds(
        chr(0x2012),   # ‒ FIGURE DASH
    )
    _punct("en-dash","ENダッシュ").adds(
        (None, chr(0x2013)),   # – EN DASH
        (TATE, "︲")           # PRESENTATION FORM FOR VERTICAL EN DASH
    )
    _punct("hyphen-minus","ハイフンマイナス").adds(
        chr(0x002D),  # - HYPHEN MINUS
    )
    _punct("hyphen-bullet","ハイフンバレット").adds(
        chr(0x2043),  # ⁃  HYPHEN MINUS
    )
    _punct("minus","マイナス").adds(
        (HALF, chr(0x2212)),  # − MINUS (MATH) ; 
        (WIDE, chr(0xFF0D)),  # － FULLWIDTH HYPHEN-MINUS
    )
    _punct("double-hyphen", "ダブルハイフン").adds(
        (WIDE, "゠"),           # 30A0 KATAKANA-HIRAGANA DOUBLE HYPHEN
        #(HALF, chr(0x2E40)),    # 2E40 DOUBLE HYPHEN (non standard punctuation)
    )
    
    # 長い棒
    _punct("dash","ダッシュ","ダーシ").adds(
        chr(0x2015),  # ― HORIZONTAL BAR 
    )
    _punct("em-dash", "EMダッシュ").adds(
        (None, chr(0x2014)),  # — EM DASH
        (TATE, "︱")       # PRESENTATION FORM FOR VERTICAL EM DASH
    )
    _punct("two-em-dash").adds(
		chr(0x2E3A),   # ⸺ TWO EM DASH
    )
    _punct("three-em-dash").adds(
		chr(0x2E3B),   # ⸻ THREE EM DASH
    )
    _punct("box-light-horizontal").adds(
		chr(0x2500)    # ─ BOX DRAWINGS LIGHT HORIZONTAL （罫線）
    )
    _punct("box-light-vertical").adds(
		(WIDE, chr(0x2502)),    # │ BOX DRAWINGS LIGHT VERTICAL （罫線）
        (HALF, chr(0xFFE8))     # ￨ HALFWIDTH FORMS LIGHT VERTICAL
    )
    _punct("vertical-line").adds(
        (HALF, "|"),
		(WIDE, chr(0xFF5C))  # ｜ FULLWIDTH VERTICAL LINE
    )
    
    # リーダ
    _punct("leader","リーダ").adds(
        (None, chr(0x2026)),  # … HORIZONTAL ELLIPSIS 
        (TATE, chr(0x221E)),  # ⋮ VERTICAL ELLIPSIS 
        (TATE, chr(0xFE19)),  # PRESENTATION FORM FOR VERTICAL HORIZONTAL ELLIPSIS 
    )
    _punct("tricolon").adds(
		chr(0x205D),  # ⁝ TRICOLON 
    )
    _punct("vertical-dots").adds(
		chr(0x205E),  # ⁞ VERTICAL DOTS
    )
    _punct("midline-horitonztal-ellipsis").adds(
		chr(0x22EF),  # ⋯ MIDLINE HORIZONTAL ELLIPSIS (MATH) 
    )
    _punct("two-dot-leader").adds(
		chr(0x2025),  # ‥ TWO DOT LEADER 
    )

    # 中黒
    _punct("nakaguro","中黒","ナカグロ").adds(
        (WIDE, chr(0x30FB)), # KATAKANA MIDDLE DOT 
        (HALF, chr(0xFF65))  # HALFWIDTH KATAKANA MIDDLE DOT
    )

    # 音引き
    _punct("onbiki","音引き","オンビキ").adds(
        (WIDE, chr(0x30FC)),  # ー KATAKANA-HIRAGANA PROLONGED SOUND MARK
        (HALF, chr(0xFF70))   # ｰ HALFWIDTH KATAKANA-HIRAGANA PROLONGED SOUND MARK 
    )

    # 波ダッシュ・チルダ
    _punct("tilde","チルダ").adds(
        (HALF, "~"),            # 007E TILDE
        (WIDE, chr(0xFF5E)),    # FF5E FULLWIDTH TILDE
    )
    _punct("wave-dash","波ダッシュ").adds(
        chr(0x301C),            # 301C WAVE DASH
    )
    _punct("swung-dash").adds(
		chr(0x2053),            # 2053 SWUNG DASH
    )
    
    # その他
    _punct("sharp","シャープ").adds(
		(HALF, "#"), (WIDE, "＃")
	)
    _punct("dollar","ドル").adds(
		(HALF, "$"), (WIDE, "＄")
	)
    _punct("percent","パーセント").adds(
		(HALF, "%"), (WIDE, "％")
	)
    _punct("ampersand","and","アンパサンド","アンド").adds(
		(HALF, "&"), (WIDE, "＆")
	)
    _punct("asterisk","アステリ").adds(
		(HALF, "*"), (WIDE, "＊")
	)
    _punct("plus","プラス").adds(
		(HALF, "+"), (WIDE, "＋")
	)
    _punct("solidus","slash","スラッシュ").adds(
		(HALF, "/"), (WIDE, "／")
	)
    _punct("reverse-solidus","backslash", "バックスラッシュ").adds(
		(HALF, "\\"), (WIDE, "＼")
	)
    _punct("equal","イコール").adds(
		(HALF, "="), (WIDE, "＝")
	)
    _punct("atmark","アットマーク").adds(
		(HALF, "@"), (WIDE, "＠")
	)
    _punct("circumflex","サーカムフレックス").adds(
		(HALF, "^"), (WIDE, "＾")
	)
    _punct("grave","グレーヴ").adds(
		(HALF, "`"), (WIDE, "｀")
	)
    _punct("vertical-line", "縦線").adds(
		(HALF, "|"), (WIDE, "｜")
	)
    _punct("underscore", "アンダースコア").adds(
		(HALF, "_"), (WIDE, "＿")
	)


WABUN = 1
OOBUN = 2
CONVERT = 4
L_PAREN = 0x10
R_PAREN = 0x20

char_convert_table = [
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
    (chr(0x0027), chr(0x2019), OOBUN|CONVERT, ""),  # 楔形からオタマジャクシ形への変換 -> 2019 CLOSE SINGLE QUOTATION MARK 
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

twochar_convert_table = [
    (chr(0x002D)+chr(0x002D), chr(0x2014), OOBUN|CONVERT, ""),  # ハイフンマイナス二つでEM DASHに変換する
    (chr(0x30FC)+chr(0x30FC), chr(0x2015)+chr(0x2015), WABUN|CONVERT, ""), # 二倍の音引きは二倍ダッシュに変換する
]


# U+2000-206F 一般句読点
# U+3000-3030 CJKの記号（句読点、括弧）
# U+FF00-FFAF 半角形／全角形 Halfwidth and Fullwidth Forms

#
#
#
#
#
def glob_entry(text, *, dest=False):
    """ ! """
    for entry in char_convert_table:
        char, destchar, _f, _n = entry
        if text[-1] == char and (not dest or destchar):
            yield entry
    for entry in twochar_convert_table:
        char, destchar, _f, _n = entry
        if text == char and (not dest or destchar):
            yield entry


def convert(this, text):
    """ !
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
    """ !
    縦書きの和文に適した約物に変換する。
    Params:
        text(str): 
    Returns:
        str: 
    """
    return convert(WABUN, text)


def wabun_convertible_chars(chars):
    """ !
    和文上で変換すべき文字である場合はエントリを返す。
    """
    for entry in glob_entry(chars):
        _curchar, destchar, flags, _name = entry
        if flags & (WABUN|CONVERT) == (WABUN|CONVERT):
            yield entry
        #if (flags & OOBUN and flags & CONVERT == 0):
        #    yield entry

def oobun_convertible_chars(chars):
    """ !
    欧文上で変換すべき文字である場合はエントリを返す。
    """
    for entry in glob_entry(chars):
        _curchar, destchar, flags, _name = entry
        if (flags & (OOBUN|CONVERT) == (OOBUN|CONVERT)):
            yield entry
        if (flags & WABUN and flags & CONVERT == 0):
            yield entry



def lookup_langtype(ch):
    """ !
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
class Punct(CharEntry):
    """ @type 
    約物に素早くアクセスする。
    """
    def enclose(self, text):
        """ @method
        Params:
            text(Str):
        Returns:
            Str:
        """
        o = self.get("open")
        c = self.get("close")
        if o is None or c is None:
            o = self
            c = self
        return o.char + text + c.char
    
    def constructor(self, value):
        """ @meta
        Params:
            Str:
        """
        chars = punctuations.lookup(value)
        return Punct.copied(chars)
        
