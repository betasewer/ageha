import datetime

from machaon.types.meta import meta

def as_date_string(d: datetime.date):
    return meta.Date.joined(d, "-")

#
#
#
def parse_py_datetime(s):
    """ pythonのdatetime表現からオブジェクトを復元する """
    if not s.startswith("datetime.datetime"):
        return None
    parts = s[len("datetime.datetime"):].strip("()").split(",")
    digits = [int(x) for x in parts]
    return datetime.datetime(digits[0], digits[1], digits[2], digits[3], digits[4])

def parse_py_date(s):
    """ pythonのdate表現からオブジェクトを復元する """
    if not s.startswith("datetime.date"):
        return None
    parts = s[len("datetime.date"):].strip("()").split(",")
    digits = [int(x) for x in parts]
    return datetime.date(digits[0], digits[1], digits[2])


def split_date(s):
    # 代表的な区切り文字で区切る
    parts = [""]
    for ch in s:
        if ch in "/-.,:／・、":
            parts.append("")
            continue
        parts[-1] += ch
    return parts

def parse_date_string(s, *, year_month=False, month_day=False, default=None):
    """ 文字列からdatetimeオブジェクトを作る。高い精度の入力を期待する """
    # reprから復元
    if s.startswith("datetime"):
        dt = parse_py_datetime(s)
        if dt is not None:
            return dt.date()

        dt = parse_py_date(s)
        if dt is not None:
            return dt

    # 区切り文字による表現
    parts = split_date(s)
    if len(parts) == 2:
        if year_month:
            parts.append(default or 1)
        elif month_day:
            parts.insert(default or datetime.date.today().year)
    if len(parts) < 3:
        raise ValueError("日付の要素が足りません: " + s)
    
    try:
        return DateLike(*parts).as_date()
    except Exception as _e:
        return None

#
#
#
class DateLike:
    def __init__(self, year=None, month=None, day=None):
        for x in (year, month, day):
            if not isinstance(x, (int, str)) and x is not None:
                raise TypeError(x)
        self.year = year
        self.month = month
        self.day = day

    def as_date(self, *, default=1, default_year=None, default_month=None, default_day=None):
        def select(v, default2):
            if v is None:
                v = default2 if default2 is not None else default
            if isinstance(v, str):
                v = int(v)
            elif not isinstance(v, int):
                raise TypeError(v)
            return v
        return datetime.date(
            select(self.year, default_year), 
            select(self.month, default_month), 
            select(self.day, default_day)
        )

    def as_date_string(self, *, default="?", default_year=None, default_month=None, default_day=None):
        def select(v, default2):
            if v is None:
                v = default2 if default2 is not None else default
            if isinstance(v, int):
                return "{:02}".format(v)
            elif isinstance(v, str):
                return v
            else:
                raise TypeError(v)
        return "{}/{}/{}".format(
            select(self.year, default_year), 
            select(self.month, default_month), 
            select(self.day, default_day)
        )
    
    def __repr__(self):
        if not hasattr(self, "year"):
            return object.__repr__(self)
        return self.as_date_string()


def stringify_dateval(date_or_digits):
    """ datetimeまたは数値リストの日付オブジェクトを/区切りの日付表現に変換する """
    if isinstance(date_or_digits, (datetime.date, datetime.datetime)):
        return date_or_digits.strftime("%Y/%m/%d")
    elif isinstance(date_or_digits, DateLike):
        return date_or_digits.as_date_string()
    elif isinstance(date_or_digits, (list, tuple)):
        #if any(x is None for x in date_or_digits):
        #    return None # Noneが含まれる場合は全体をNoneにする
        if len(date_or_digits) != 3:
            raise ValueError("digits must have 3 value")
        return DateLike(*date_or_digits).as_date_string()
    else:
        raise TypeError(date_or_digits)
