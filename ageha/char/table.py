


class CharValue:
    def __init__(self, c, bits):
        self.char: str = c
        self.bits: set = bits


class CharSelector:
    def __init__(self, tbits=None, fbits=None, index=None):
        self.tbits = tbits or set()
        self.fbits = fbits or set()
        self.index = index
        self.parent = None

    def add_klass(self, value, bit):
        if bit:
            self.tbits.add(value)
        else:
            self.fbits.add(value)

    def set_index(self, index):
        self.index = index
    
    def add_all_bits(self, bits):
        for b in bits:
            if b > 0:
                if b < KLASS_VALUE_START:
                    self.index = b
                else:
                    self.tbits.add(b)
            elif b < 0:
                self.fbits.add(-b)

    def get_all_bits(self):
        allbits = set()
        if self.tbits:
            allbits |= self.tbits
        if self.fbits:
            allbits |= set(-x for x in self.fbits)
        if self.index is not None:
            allbits.add(self.index)
        return allbits
        
    def select(self, chain):
        chs = []
        for ch in chain:
            if bool(self.fbits) and self.fbits.issubset(ch.bits):
                continue
            if not self.tbits or self.tbits.issubset(ch.bits):
                chs.append(ch)
        if self.index is not None:
            chs = [chs[self.index]]
        return chs

    def follow(self, parent):
        self.parent = parent
        return self

    def get_parts(self, table):
        parts = []
        if self.parent is not None:
            parts.extend(self.parent.get_parts(table))
        
        for bit in self.tbits:
            kls = table.get_klass_by_value(bit)
            if kls is None:
                raise ValueError(bit)
            parts.append(kls.name)
        
        for bit in self.fbits:
            kls = table.get_klass_by_value(-bit)
            if kls is None:
                raise ValueError(-bit)
            parts.append(kls.name)
        
        if self.index is not None:
            parts.append(str(self.index))
        
        return parts
    

class CharEntry:
    """ @type [Char]
    名前と性質を指定する文字
    """
    def __init__(self, table, name, selector, chain=None):
        self.table = table
        self.name = name
        self._selector = selector
        self._chain = chain or []

    @classmethod
    def copied(cls, right):
        return cls(right.table, right.name, right._selector, right._chain)

    #
    def adds(self, *entries):
        """ 文字を一括で定義する """
        for ent in entries:
            if isinstance(ent, tuple):
                self.add(*ent)
            elif isinstance(ent, str):
                self.add(None, ent)
        return self

    def add(self, chtype, char, antitype=None):
        """ 文字の定義を追加する """
        if chtype is None:
            chtype = set()
        elif isinstance(chtype, CharKlass):
            chtype = chtype.bits
        if not isinstance(chtype, set):
            raise TypeError("chtype must be CharKlass or set")
        
        if isinstance(char, str):
            ch = CharValue(char, chtype)
            self._chain.append(ch)
        elif isinstance(char, CharEntry):
            newchain = []
            for child in char._chain:
                ch = CharValue(child.char, child.bits|chtype)
                newchain.append(ch)
            if antitype is not None:
                char.add(antitype, self)
            self._chain.extend(newchain)
        else:
            raise TypeError("char")
        return self

    def append(self, ch: CharValue):
        """ 文字定義オブジェクトを追加する """
        self._chain.append(ch)

    def select(self, selector: CharSelector):
        """ 
        フラグ集合に適合する文字定義を取得する 
        Returns:
            CharEntry:
        """
        if self._selector is not None:
            selector.follow(self._selector)
        chs = selector.select(self._chain)
        return CharEntry(self.table, self.name, selector, chs)

    #
    #
    #
    @property
    def char(self):
        """ @method
        先頭の文字を取得する。
        Returns:
            Str:
        """
        return self._chain[0].char if self._chain else ""
    
    @property
    def chars(self):
        """ @method
        すべての文字を取得する。 
        Returns:
            Str:
        """
        return "".join(x.char for x in self._chain)

    def enum_chars(self):
        """ @method alias-name [list]
        文字エントリを列挙する。
        Returns:
            Sheet[](char, path):
        """
        for ch in self._chain:
            yield {
                "char" : ch.char,
                "path" : self.select(CharSelector(tbits=ch.bits)).path
            }

    @property
    def path(self):
        """ @method
        パスを取得する。
        Returns:
            Str:
        """
        parts = []
        parts.append(self.name)
        if self._selector is not None:
            parts.extend(self._selector.get_parts(self.table))
        return "/".join(parts)

    def get(self, klass: str):
        """ @method
        フラグの名前集合に適合する文字を取得する
        Params:
            klass(str):
        Returns:
            Char:
        """
        sel = self.table.parse_selector(klass)
        return self.select(sel)

    def __truediv__(self, left):
        return self.get(left)

    def copy(self, spirit):
        """ @task
        クリップボードにコピーする。
        """
        spirit.clipboard_copy(self.chars)  

    #
    #
    #
    def constructor(self, name):
        """ @meta
        Params:
            str:
        """
        tablename, sep, rest = name.partition("/")
        if not sep:
            raise ValueError("テーブル名を先頭に/で指定してください")
        if tablename == "punct":
            from ageha.japanese.punct import punctuations
            tbl = punctuations
        else:
            raise ValueError("不明なテーブル名です: " + tablename)
        return tbl.lookup(rest)
    
    def stringify(self):
        """ @meta """
        return "<{} '{}'>".format(self.path, self.chars)
        
#
#
#
KLASS_VALUE_START = 10000

class CharKlass:
    def __init__(self, names, value, truth=True):
        self.names = names
        self.value = value
        self.truth = truth

    @property
    def name(self):
        return self.names[0]

    @property
    def bits(self):
        return {self.value}

    def __or__(self, right):
        return {self.value, right.value}


class CharTable:
    def __init__(self, loader):
        self._table = {}
        self._loader = loader
        self._klass = {}

    def add(self, *names):    
        """ 文字エントリを追加する """
        entry = CharEntry(self, names[0], None)
        for name in names:
            self._table[name] = entry
        return entry

    def get(self, namerow):
        """ 文字エントリを取得する """
        return self._table[namerow]

    def klass(self, *names, negate=None):
        """ 性質値を定義する """
        if negate is not None:
            k = CharKlass(names, negate.value, False)
        else:
            v = KLASS_VALUE_START + len(self._klass)
            k = CharKlass(names, v)
        for name in names:
            self._klass[name] = k
        return k

    def get_klass_by_value(self, bit):
        """ 定数値からクラスを取得する """
        if 0 < bit and bit < KLASS_VALUE_START:
            return None
        for v in self._klass.values():
            if bit > 0:
                if v.value == bit and v.truth:
                    return v
            elif bit < 0:
                if v.value == -bit and not v.truth:
                    return v
        return None

    def parse_selector(self, path) -> CharSelector:
        """ 文字列からクラス値集合を生成する """
        sel = CharSelector()
        parts = path.split("/")
        if parts and parts[-1].isdigit():
            sel.set_index(int(parts[-1]))
            parts.pop()
        
        for flag in parts:
            kls = self._klass.get(flag)
            if kls is None:
                raise ValueError(flag)
            sel.add_klass(kls.value, kls.truth)
        return sel

    def lookup(self, instruction) -> CharEntry:
        """
        テーブルをロードし、名前で文字を探し出す。
        (klass-name).../(char-name)
        Returns:
            List[PunctChar]:
        """
        if not self._table:
            self._loader(self)
        
        name, sep, path = instruction.partition("/")
        if sep:
            sel = self.parse_selector(path)
        else:
            sel = None
        
        char = self._table.get(name)
        if char is None:
            raise ValueError("不明な約物です: '{}'".format(name))

        if sel is not None:
            char = char.select(sel)
            if char is None:
                raise ValueError("不明な約物です: '{}'({})".format(name, path))
    
        return char

