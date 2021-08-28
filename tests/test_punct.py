from ageha.japanese.punct import tate_convert


def test_tate_convert():
    cvt = tate_convert
    assert cvt("(1986-2021)") == "（1986‐2021）" # HYPHEN-MINUS -> HYPHEN
    assert cvt("[1986–2021]") == "［1986‐2021］" # EN DASH -> HYPHEN
    assert cvt("{1986－2021}") == "｛1986‐2021｝" # FULLWIDTH MINUS -> HYPHEN
    assert cvt("＜ハローワーク＞") == "〈ハローワーク〉"

    assert cvt("まさかお前——") == "まさかお前――"          # EM DASH -> HORIZONTAL BAR
    assert cvt("｜｜何ッ!?") == "――何ッ！？"            # FULLWIDTH VERTICAL LINE -> HORIZONTAL BAR
    assert cvt("──それが答えか──") == "――それが答えか――"   # 罫線 -> HORIZONTAL BAR
    assert cvt("ーーワーテルローの戦いの真実") == "――ワーテルローの戦いの真実" # ダブル音引き -> ダブルHORIZONTAL BAR / 音引き一つでは変換は起こさない

    assert cvt("マタイ19.2-4") == "マタイ19.2‐4" # ピリオドは変換しない

    assert cvt("!@#$%^&*+?/") == "！＠＃＄％＾＆＊＋？／" # 各種記号の全角化


#test_wabun_convert()
#import codecs
#print(tate_convert("マタイ19.2‐4"))
#print(codecs.encode(tate_convert("マタイ19.2-4").encode("utf-32"), "hex"))
#print(codecs.encode("マタイ19.2‐4".encode("utf-32"), "hex"))


