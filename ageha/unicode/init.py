
from ageha.charpad import Uchar


def get_db_path(app, *paths):
    # データファイルのパス
    p = app.get_local_dir("ageha").join(*paths)
    if not p.isfile():
        raise ValueError("データファイル'{}'がありません".format("/".join(paths)))
    return p
    
def readlines_datatext(path, column):
    # 行の各要素をリストにして返す
    with open(path, "r", encoding="utf-8") as fi:
        for line in fi:
            body, _sep, _comment = line.partition("#")
            body = body.strip()
            if not body:
                continue

            elems = body.split(";")
            if len(elems) < column:
                continue
            yield [x.strip() for x in elems]


def parse_code(text):
    # コード一つをパースする
    return int(text.strip(), 16)

def parse_code_range(text):
    # コードの範囲をパースする
    start, sep, end = text.partition("..")
    if not sep:
        end = start
    
    s = int(start, 16)
    e = int(end, 16)
    return (s, e)

def to_code_range(code):
    if isinstance(code, int):
        return (code, code)
    elif isinstance(code, tuple):
        return code
            
def uchar_from_code_range(start, end):
    for code in range(start, end):
        c = Uchar.fromchar(chr(code), code)
        yield c


class OrderedCodeList:
    def __init__(self):
        self._entries = []
        
    def append(self, range, value):
        self._entries.append((range, value))

    def items(self):
        return iter(self._entries)
    
    def bisect_search(self, key):
        c, _ = self._entries[-1]
        _, le = to_code_range(c)
        if key < 0 or le < key:
            return None

        imin = 0
        imax = len(self._entries)
        while imin <= imax:
            imid = imin + (imax - imin) // 2
            c, value = self._entries[imid]
            s, e = to_code_range(c)
            if s <= key and key <= e:
                return value # 見つかった
            elif key < s:
                # 左にある
                imax = imid - 1
            elif e < key:
                # 右にある
                imin = imid + 1
        return None

    def sort(self):
        self._entries.sort(key=lambda x:x[0])
        


class Unicodes:
    """ @type
    """
    def __init__(self):
        self._databases = {}

    def open(self, app, name):
        if name not in self._databases:
            mod, sep, klassname = name.partition(".")
            if not sep:
                raise ValueError("module must be specified")
            import importlib
            mod = importlib.import_module("ageha.unicode." + mod)
            klass = getattr(mod, klassname)
            if not isinstance(klass, type):
                raise TypeError("")

            db = klass()
            db.init(app)
            self._databases[name] = db
            return db
        else:
            return self._databases[name]  

    #
    # UCD
    #
    def blocks(self, app):
        """ @task
        Returns:
            Sheet[ObjectCollection](name, range):
        """
        for (s, e), block in self.open(app.root, "ucd.Blocks").items():
            yield {
                "name" : block,
                "range" : "{:04X} - {:04X}".format(s, e)
            }

    def block(self, app, name):
        """ @task 
        Params:
            name(str):
        Returns:
            Sheet[Uchar](char, name, code):
        """
        for (s, e), block in self.open(app.root, "ucd.Blocks").items():
            if name in block:
                yield from uchar_from_code_range(s, e)

    def scripts(self, app):
        """ @task
        Returns:
            Sheet[ObjectCollection](name):
        """
        for name in self.open(app.root, "ucd.Scripts").names():
            yield {
                "name" : name,
            }

    def script(self, app, name):
        """ @task 
        Params:
            name(str):
        Returns:
            Sheet[Uchar](char, name, code):
        """
        for (s, e), scr in self.open(app.root, "ucd.Scripts").items():
            if name in scr:
                yield from uchar_from_code_range(s, e)
    
    def name_aliases(self, app):
        """ @task
        Returns:
            Sheet[ObjectCollection](range, alias):
        """
        for (s, e), section in self.open(app.root, "ucd.NameAliases").items():
            yield {
                "range" : "{:04X} - {:04X}".format(s, e),
                "alias" : ", ".join("{}({})".format(n,t) for n,t in section)
            }
    
    def constructor(self, value=None):
        """ @meta
        """
        return unicode_database

unicode_database = Unicodes()
        


        
