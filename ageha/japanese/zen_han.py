
zenkaku_abc = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
hankaku_abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
zenkaku_num = "０１２３４５６７８９"
hankaku_num = "0123456789"

def findtable(ch, t1, t2):
    fpos = t1.find(ch)
    if fpos > -1:
        return t2[fpos]
    return None

def zenkaku_to_hankaku(ch):
    """
    全角文字を半角文字に変換する。
    アルファベット、数字、カタカナに対応。
    Params:
        ch(str): 文字
    Returns:
        Str: 変換されなければそのまま返す
    """
    abc = findtable(ch, zenkaku_abc, hankaku_abc)
    if abc is not None:
        return abc
        
    num = findtable(ch, zenkaku_num, hankaku_num)
    if num is not None:
        return num

    from ageha.japanese.kana import zenkaku_to_hankaku_kana
    return zenkaku_to_hankaku_kana(ch)

    
def hankaku_to_zenkaku(ch):
    """
    半角文字を全角文字に変換する。
    アルファベット、数字、カタカナに対応。
    Params:
        ch(str): 文字
    Returns:
        Str: 変換されなければそのまま返す
    """
    abc = findtable(ch, hankaku_abc, zenkaku_abc)
    if abc is not None:
        return abc
    
    num = findtable(ch, hankaku_num, zenkaku_num)
    if num is not None:
        return num

    from ageha.japanese.kana import hankaku_to_zenkaku_kana
    return hankaku_to_zenkaku_kana(ch)

