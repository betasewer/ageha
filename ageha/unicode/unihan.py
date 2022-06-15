from collections import defaultdict
from ageha.unicode.init import (
    readlines_datatext, get_db_path, 
    parse_code, parse_code_range, OrderedCodeList
)


def readlines_unihan(path):
    with open(path, "r", encoding="utf-8") as fi:
        for line in fi:
            body, _sep, _comment = line.partition("#")
            body = body.strip()
            if not body:
                continue

            elems = [x.strip() for x in body.split("\t")]
            if len(elems) < 2:
                continue

            code = elems[0]
            if not code.startswith("U+"):
                continue
            code = int(code[2:], 16)

            key = elems[1]
            value = elems[2]

            yield code, key, value

class UnihanData:
    def __init__(self, name):
        self._name = name
        self._di = {}
        self._codedi = {}

    def init(self, app): 
        p = get_db_path(app, "Unihan", self._name)
        section = None
        for code, key, value in readlines_unihan(p):
            if section is None:
                section = [code, {}]
            elif section[0] != code:
                self._di[section[0]] = section[1]
                section = [code, {}]
            
            section[1][key] = value

    def item(self, code):
        return self._di.get(code, {})

    def get(self, code, key):
        return self._di.get(code, {}).get(key, None)

    def _init_codedict(self, itemname, getter):
        di = defaultdict(list)
        for code, di in self._di.items():
            v = di.get(itemname)
            if v is None:
                continue
            value = getter(v)
            di[value].append(code)
        self._codedi[itemname] = di
        return di

    def search_code(self, itemname, getter, value):
        if itemname not in self._codedi:
            di = self._init_codedict(itemname, getter)
        else:
            di = self._codedi[itemname]
        return di.get(value, None)


class DictIndices(UnihanData):
    def __init__(self):
        super().__init__("Unihan_DictionaryIndices.txt")
    
class DictLikeData(UnihanData):
    def __init__(self):
        super().__init__("Unihan_DictionaryLikeData.txt")

    def get_strange(self, code):
        r = self.get(code, "kStrange")
        if r:
            return parse_strange(r)

        
class IRGSoruces(UnihanData):
    def __init__(self):
        super().__init__("Unihan_IRGSoruces.txt")
    
    
class Numerics(UnihanData):
    def __init__(self):
        super().__init__("Unihan_NumericValues.txt")


class OtherMappings(UnihanData):
    def __init__(self):
        super().__init__("Unihan_OtherMappings.txt")

    def get_ibmjapan(self, code):
        r = self.get(code, "kIBMJapan")
        if r:
            return r[1:]

    def searchby_ibmjapan(self, value):
        return self.search_code("kIBMJapan", lambda x:x[1:], value)

    def get_JoyoKanji(self, code):
        r = self.get(code, "kJoyoKanji")
        if r:
            return parse_JoyoKanji(r)
            
    def get_JinmeiyoKanji(self, code):
        r = self.get(code, "kJinmeiyoKanji")
        if r:
            return parse_JinmeiyoKanji(r)

    def get_jis(self, code):
        jis0 = self.get(code, "kJis0")
        if jis0:
            return {"jis" : "0208", "code" : jis0}
        jis1 = self.get(code, "kJis1")
        if jis1:
            return {"jis" : "0212", "code" : jis1}
        jis2 = self.get(code, "kJIS0213")
        if jis2:
            return {"jis" : "0213", "code" : jis2}
            
    def searchby_jis(self, value):
        rs0 = self.search_code("kJis0", lambda x:x[1:], value)
        if rs0:
            return rs0
        rs1 = self.search_code("kJis1", lambda x:x[1:], value)
        if rs1:
            return rs1
        rs2 = self.search_code("kJIS0213", lambda x:x[1:], value)
        if rs2:
            return rs2
        return []
    

class RadicalStroke(UnihanData):
    def __init__(self):
        super().__init__("Unihan_RadicalStrokeCounts.txt")

    def get_RSAdobe_Japan1_6(self, code):
        r = self.get(code, "kRSAdobe_Japan1_6")
        if r:
            return parse_RSAdobe_Japan1_6(r)

    def from_RSAdobe_Japan1_6(self, radical, stroke):
        def key(x):
            v = parse_RSAdobe_Japan1_6(x)
            return (v["radical"], v["rest_stroke"])
        return self.search_code("kRSAdobe_Japan1_6", key, (radical, stroke))

    
class Readings(UnihanData):
    def __init__(self):
        super().__init__("Unihan_Readings.txt")
    
class Variants(UnihanData):
    def __init__(self):
        super().__init__("Unihan_Variants.txt")


def parse_RSAdobe_Japan1_6(text):
    _code, _sep, tail = text.split()[0].rpartition("+")
    nums = [int(x) for x in tail.split(".")]
    return {
        "radical" : nums[0],
        "radical_stroke" : nums[1],
        "rest_stroke" : nums[2],
        "stroke" : nums[1] + nums[2]
    }

def parse_strange(text):
    t, sep, p = text.partition(":")
    return {
        "type" : t,
        "param" : p
    }

def parse_JinmeiyoKanji(text):
    if text.startswith("U"):
        return {
            "variant" : text[2:],
        }
    else:
        return {
            "year" : int(text),
        }

def parse_JoyoKanji(text):
    y, _sep, co = text.partition(":")
    return {
        "year" : int(y),
        "standard" : co[2:]
    }
