
#
#
#
def is_kanji(text):
    # CJK統合漢字＋拡張A、互換漢字をカバー
    m = re.match(r"([\u3400-\u9FFF]|[\uF900-\uFA6F])+", text)
    if m:
        mlen = len(m.group(0))
        return mlen == len(text)
    return False
