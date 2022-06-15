
#
#
#
def is_kanji(ch):
    # CJK統合漢字＋拡張A、互換漢字
    c = ord(ch)
    return (0x3400 <= c and c <= 0x9FFF) or (0xF900 <= c and c <= 0xFA6F)

def is_cjk_symbol(ch):
    # CJKシンボル
    c = ord(ch)
    return (0x3000 <= c and c <= 0x303F)

def classified(text, *classes):
    for ch in text:
        if not any(tester(ch) for tester in classes):
            return False
    return True
