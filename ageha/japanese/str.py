

class Replacer:
    """ 置換補助クラス """
    def __init__(self, replace_fn):
        self.buf = ""
        self.ret = ""
        self.replacer = replace_fn
    
    def replace(self):
        if self.buf:
            v = self.replacer(self.buf)
            self.buf = ""
            self.ret += v
    
    def hit(self, ch):
        self.buf += ch
    
    def unhit(self, ch):
        self.replace()
        self.ret += ch
    
    def finish(self):
        self.replace()
        return self.ret
        
        
#
#
#
class StrType:
    """ @type mixin
    文字列関数のコレクション
    MixinType:
        Str
    """
    def widen(self, s):
        """ @method [全角化]
        半角であれば全角にする。
        Returns:
            Str:
        """
        from ageha.japanese.zen_han import hankaku_to_zenkaku
        return "".join([hankaku_to_zenkaku(ch) for ch in s])

    def narrow(self, s):
        """ @method [半角化]
        全角であれば半角にする。
        Returns:
            Str:
        """
        from ageha.japanese.zen_han import zenkaku_to_hankaku
        return "".join([zenkaku_to_hankaku(ch) for ch in s])

    def tatefy(self, s):
        """ @method [縦化]
        約物を縦書き和文用に変換する。
        Returns:
            Str:
        """
        from ageha.japanese.punct import tate_convert
        return self.widen(tate_convert(s))

    def yokofy(self, s):
        """ @method [横化]
        全角を半角に、約物を横書き用に変換する。
        Returns:
            Str:
        """
        pass

    def nounit_kanjify(self, s):
        """ @method [〇式漢数字化]
        アラビア数字・十式漢数字を〇式漢数字に変換する。
        変換できない部分はそのまま。
        Returns:
            Str:
        """
        from ageha.japanese.numeric import kansuuji
        rep = Replacer(kansuuji.nounit_write)
        for ch in s:
            if ch.isdigit() or kansuuji.detect(ch):
                rep.hit(ch)
            else:
                rep.unhit(ch)
        return rep.finish()

    def unit_kanjify(self, s):
        """ @method [十式漢数字化]
        アラビア数字・〇式漢数字を十式漢数字に変換する。
        変換できない部分はそのまま。
        Returns:
            Str:
        """
        from ageha.japanese.numeric import kansuuji
        rep = Replacer(kansuuji.unit_write)
        for ch in s:
            if ch.isdigit() or kansuuji.detect(ch):
                rep.hit(ch)
            else:
                rep.unhit(ch)
        return rep.finish()

    def numerize(self, s):
        """ @method
        漢数字・全角数字・ローマ数字をアラビア数字に変換する。
        変換できない部分はそのまま。
        Returns:
            Str:
        """
        from ageha.japanese.numeric import kansuuji
        rep = Replacer(lambda x: str(kansuuji.parse(x)))
        for ch in s:
            if kansuuji.detect(ch):
                rep.hit(ch)
            else:
                rep.unhit(ch)
        return rep.finish()

    def page_kanjify(self, s):
        """ @method
        アラビア数字の頁を漢数字の頁に変換する。
        変換できない部分はそのまま。
        Returns:
            Str:
        """
        if s.startswith("p."):
            s = s[2:].lstrip()
        if s.startswith("pp."):
            s = s[3:].lstrip()
        
        from ageha.japanese.numeric import kansuuji
        from ageha.japanese.punct import tate_convert
        rep = Replacer(kansuuji.nounit_write)
        for ch in s:
            if ch.isdigit() or kansuuji.detect(ch):
                rep.hit(ch)
            else:
                tch = tate_convert(ch)
                rep.unhit(tch)
        
        return rep.finish() + "頁"
    
    def tate_nounit_kanjify(self, s):
        """ @method
        アラビア数字の頁を〇式漢数字に変換し、その他は縦書き用文字に変換する。
        変換できない部分はそのまま。
        Returns:
            Str:
        """
        from ageha.japanese.numeric import kansuuji
        from ageha.japanese.punct import tate_convert
        rep = Replacer(kansuuji.nounit_write)
        for ch in s:
            if ch.isdigit() or kansuuji.detect(ch):
                rep.hit(ch)
            else:
                tch = tate_convert(ch)
                rep.unhit(tch)
        return rep.finish()

    def tatefy_name(self, s):
        """ @method
        縦書きのイニシャル入り欧文名を横書きの表記に変換する。
        Returns:
            Str:
        """
        from ageha.japanese.punct import tate_convert
        ret = ""
        for ch in s:
            if ch == ".":
                ret += "・"
            elif ch == " ":
                continue # 半角スペースは無視する
            else:
                ret += tate_convert(ch)
        return ret

    def tatefy_biblelocation_1(s):
        """ @method
        聖書の章と節の漢数字化。
        Returns:
            Str:
        """
        from ageha.japanese.numeric import kansuuji
        ss = ""
        num = ""
        for ch in s:
            if ch.isdigit():
                num += ch
                continue
            elif num:
                ss += kansuuji.write(num)
                num = ""
            if ch == "," or ch == ".":
                ss += "・"
            elif ch == "-":
                ss += "‐"
            else:
                ss += ch
        if num:
            ss += kansuuji.write(num)
        return ss

    def uchars(self, s):
        """ @method
        ユニコード文字オブジェクトに分解する。
        Returns:
            Sheet[Uchar](char, code, name):
        """
        from ageha.charpad import Uchar
        return [Uchar.fromchar(c) for c in s]
    




