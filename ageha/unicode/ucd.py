from ageha.unicode.init import (
    readlines_datatext, get_db_path, 
    parse_code, parse_code_range, OrderedCodeList
)


class Blocks:
    def __init__(self):
        self._li = OrderedCodeList()
    
    def init(self, app):
        p = get_db_path(app, "UCD", "Blocks.txt")
        
        for coderng, block in readlines_datatext(p, 2):
            rng = parse_code_range(coderng)
            self._li.append(rng, block)

    def find(self, code):
        return self._li.bisect_search(code)

    def items(self):
        return self._li.items()
    

class Scripts:
    def __init__(self):
        self._li = OrderedCodeList()
    
    def init(self, app):
        p = get_db_path(app, "UCD", "Scripts.txt")
        
        for coderng, script in readlines_datatext(p, 2):
            rng = parse_code_range(coderng)
            self._li.append(rng, script)
        
        self._li.sort()

    def find(self, code):
        return self._li.bisect_search(code)

    def names(self):
        history = set()
        for _, name in self._li.items():
            if name not in history:
                yield name
            history.add(name)
    
    def items(self):
        return self._li.items()

class Age:
    def __init__(self):
        self._li = OrderedCodeList()
    
    def init(self, app):
        p = get_db_path(app, "UCD", "DerivedAge.txt")
        
        for coderng, age in readlines_datatext(p, 2):
            rng = parse_code_range(coderng)
            self._li.append(rng, age)
        
        self._li.sort()

    def find(self, code):
        return self._li.bisect_search(code)

    def items(self):
        return self._li.items()
        
class NameAliases:
    def __init__(self):
        self._li = OrderedCodeList()
    
    def init(self, app):
        p = get_db_path(app, "UCD", "NameAliases.txt")
        
        section = []
        for acode, alias, atype in readlines_datatext(p, 3):
            code = parse_code(acode)
            if section:
                if section[0] == code:
                    section[1].append((alias, atype))
                else:
                    self._li.append(section[0], section[1])
                    section = [code, [(alias, atype)]]
            else:
                section = [code, [(alias, atype)]]
        
        if section:
            self._li.append(section[0], section[1])

    def find_and_gettop(self, code):
        sec = self._li.bisect_search(code)
        if sec is None:
            return None
        for alias, atype in sec:
            if atype in ("control", "figment"):
                return alias
        return None
    
    def items(self):
        return self._li.items()


class Brackets:
    def __init__(self):
        self._li = OrderedCodeList()
    
    def init(self, app):
        p = get_db_path(app, "UCD", "BidiBrackets.txt")
        
        for code, code2, btype in readlines_datatext(p, 3):
            c = parse_code(code)
            c2 = parse_code(code2)
            self._li.append(c, (c2, btype))

    def find_type(self, code):
        entry = self._li.bisect_search(code)
        if entry is not None:
            return entry[1]
        return None
    
    def find_another(self, code):
        entry = self._li.bisect_search(code)
        if entry is not None:
            return entry[0]
        return None

    def items(self):
        return self._li.items()


class VerticalOrientations:
    def __init__(self):
        self._li = OrderedCodeList()
    
    def init(self, app):
        p = get_db_path(app, "UCD", "VerticalOrientation.txt")
        
        for coderng, vtype in readlines_datatext(p, 2):
            crng = parse_code_range(coderng)            
            self._li.append(crng, vtype)

    def find(self, code):
        return self._li.bisect_search(code)

    def items(self):
        return self._li.items()