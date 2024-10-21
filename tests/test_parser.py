import datetime
from ageha.dateandtime import stringify_dateval, DateLike
from ageha.japanese.parsers import norm_date_string, parse_int_numeric

def test_date():
    assert stringify_dateval(datetime.datetime(1991,7,31)) == "1991/07/31"
    assert stringify_dateval([1991,7,31]) == "1991/07/31"
    assert stringify_dateval(("1991","7","31")) == "1991/7/31" # 文字列はそのままになる
    assert stringify_dateval([1991,7,None]) == "1991/07/?"

    assert DateLike(1992, None, None).as_date(default=1) == datetime.date(1992, 1, 1)
    assert DateLike(1992, 1, None).as_date(default_day=7) == datetime.date(1992, 1, 7)
    assert DateLike(1992, 8, 2).as_date_string() == "1992/08/02"
    assert DateLike(1992, None, None).as_date_string(default=1) == "1992/01/01"
    assert DateLike(1992, 1, None).as_date_string() == "1992/01/?"

    assert DateLike("2002","5","10").as_date() == datetime.date(2002, 5, 10)


def test_normalnum():  
    assert parse_int_numeric("1987") == 1987
    assert parse_int_numeric("１９８７") == 1987
    assert parse_int_numeric("一九八七") == 1987
    assert parse_int_numeric("千九百八十七") == 1987
    assert parse_int_numeric("①②③④") == 1234
    assert parse_int_numeric("123,789,012") == 123789012
    assert parse_int_numeric("１２３，５６７８") == 1235678
    assert parse_int_numeric("一、五〇〇、九〇〇") == 1500900


def test_date_parsers():  
    assert norm_date_string("二〇〇八年九月二五日") == "2008/09/25"
    assert norm_date_string("二〇〇八年九月二五日発表") =="2008/09/25"
    assert norm_date_string("二〇〇八年九月〓日") =="2008/09/?"

    def ps(s):
        return norm_date_string(s)

    assert ps(r"1991/12/9") == "1991/12/09"
    assert ps(r"1991.12.9") == "1991/12/09"
    assert ps(r"1991-12-9") == "1991/12/09"
    assert ps(r"1991.12:9") == "1991/12/09"
    assert ps(r"1991 / 12 / 9") == "1991/12/09"
    assert ps(r"1991/12/9 朝一") == "1991/12/09"
    assert ps(r"1991/12/9夕方") == "1991/12/09"
    assert ps(r"1991/12/ 9夕方") == "1991/12/09"
    assert ps(r"1991/12/〓") == "1991/12/?"
    assert ps(r"1991/〓/〓") == "1991/?/?"

    assert ps(r"１９９１/12/９") == "1991/12/09"
    assert ps(r"一九九一/十二/九") == "1991/12/09"
    assert ps(r"一九九一/〓/〓") == "1991/?/?"
    assert ps(r"2022.3.30 朝一") == "2022/03/30"
    assert ps(r"2022.3.30夕方まで") == "2022/03/30"
