from ageha.japanese.punct import (
    punctuations, tate_convert
)
from machaon.macatest import run

def test_lookup_char():
    ch = punctuations.lookup("hyphen")
    assert ch
    assert ch.char == chr(0x2010)

    ch = punctuations.lookup("ダッシュ")
    assert ch
    assert ch.char == chr(0x2015)


def test_lookup_kakko_cmd():
    ch = punctuations.lookup("sumi-kakko/open/yoko")
    assert ch.char == "【"

    ch = punctuations.lookup("maru-kakko/half/close")
    assert ch.char == ")"
    
    ch = punctuations.lookup("bracket/wide/tate/open")
    assert ch.char == "﹇"


def test_lookup_kakko():
    ch = punctuations.lookup("sumi-kakko")
    assert ch
    assert ch.get("open/yoko").char == "【"
    assert ch.get("close/yoko").char == "】"
    assert ch.get("close/yoko").path == "sumi-kakko/close/yoko"

    ch = punctuations.lookup("maru-kakko")
    assert ch
    assert ch.get("open/yoko").char == "（"
    assert ch.get("close/yoko").char == "）"
    assert ch.get("half").chars == "()"
    assert ch.get("half/open").char == "("
    assert ch.get("half/close").char == ")"
    assert ch.get("half").path == "maru-kakko/half"

    ch = punctuations.lookup("bracket")
    assert ch
    assert ch.get("open").char == "["
    assert ch.get("close").char == "]"
    assert ch.get("wide/yoko").chars == "［］"
    assert ch.get("wide/yoko/close").path == "bracket/close/wide/yoko"


def test_lookup_index():
    ch = punctuations.lookup("leader/0")
    assert ch.chars == "…"

    ch = punctuations.lookup("leader/2")
    assert ch.chars == chr(0xFE19)

    ch = punctuations.lookup("leader/tate/1")
    assert ch.chars == chr(0xFE19)



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


