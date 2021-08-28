
zenkaku_katakana = "ァアィイゥウェエォオカキクケコサシスセソタチッツテトナニヌネノハヒフヘホマミムメモャヤュユョヨラリルレロワヲンー"
hankaku_katakana = "ｧｱｨｲｩｳｪｴｫｵｶｷｸｹｺｻｼｽｾｿﾀﾁｯﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓｬﾔｭﾕｮﾖﾗﾘﾙﾚﾛﾜｦﾝｰ"

daku_kana = "がぎくげござじずぜぞだぢづでどばびぶべぼガギグゲゴザジズゼゾダヂヅデドバビブベボヴ"
n_daku_kana = "かきくけこさしすせそたちつてとはひふへほカキクケコサシスセソタチツテトハヒフヘホウ"
hdaku_kana = "ぱぴぷべぼパピプペポ"
n_hdaku_kana = "はひふへほハヒフヘホ"

def findtable(ch, t1, t2):
    fpos = t1.find(ch)
    if fpos > -1:
        return t2[fpos]
    return None

def zenkaku_to_hankaku_kana(ch):
    """
    全角カタカナを半角カタカナに変換する。濁点・半濁点に対応する
    Params:
        ch(str): 文字
    Returns:
        Str: 変換されなければそのまま返す
    """
    kana = findtable(ch, zenkaku_katakana, hankaku_katakana)
    if kana is not None:
        return kana
    
    dkana = findtable(ch, daku_kana, n_daku_kana)
    if dkana is not None:
        h = hankaku_katakana[zenkaku_katakana.index(dkana)]
        return h + chr(65438) # 半角濁点
    
    hkana = findtable(ch, hdaku_kana, n_hdaku_kana)
    if hkana is not None:
        h = hankaku_katakana[zenkaku_katakana.index(hkana)]
        return h + chr(65439) # 半角半濁点
    
    return ch
    
def hankaku_to_zenkaku_kana(ch):
    """
    半角カタカナを全角カタカナに変換する。濁点・半濁点に対応する
    Params:
        ch(str): 文字
    Returns:
        Str: 変換されなければそのまま返す
    """
    kana = findtable(ch, hankaku_katakana, zenkaku_katakana)
    if kana is not None:
        return kana

    if ord(ch) == 65438: 
        return chr(0x3099) # 全角濁点
    elif ord(ch) == 65439:
        return chr(0x309A) # 全角半濁点

    return ch

 
#
#
#
kana_toupper_translation = str.maketrans({
    ord("ぁ"): "あ",
    ord("ぃ"): "い",
    ord("ぅ"): "う",
    ord("ぇ"): "え",
    ord("ぉ"): "お",
    ord("ゃ"): "や",
    ord("ゅ"): "ゆ",
    ord("ょ"): "よ",
    ord("っ"): "つ",
    ord("ゎ"): "わ",
    ord("ァ"): "ア",
    ord("ィ"): "イ",
    ord("ゥ"): "ウ",
    ord("ェ"): "エ",
    ord("ォ"): "オ",
    ord("ャ"): "ヤ",
    ord("ュ"): "ユ",
    ord("ョ"): "ヨ",
    ord("ッ"): "ツ",
    ord("ヮ"): "ワ",
    ord("ヶ"): "ケ",
    ord("ゖ"): "け",
    ord("ㇽ"): "ル",
})
def kana_toupper(text):
    return text.translate(kana_toupper_translation)

#
# -------------------------------------------------------------
# kana   bits(daku)   base(un-daku, upper)    kana     V    C
# 
#