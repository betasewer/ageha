#!/usr/bin/env python3
# coding: utf-8
import unicodedata
import datetime
import math
from typing import Optional, Union

from ageha.japanese.numeric import kansuuji, NumeralParseError
from ageha.japanese.zen_han import zenkaku_num, hankaku_num, zenkaku_to_hankaku, findtable
from ageha.dateandtime import split_date, DateLike

#
#
#
def parse_int_numeric(text) -> Optional[int]:
    """ 漢数字・全角半角の整数表現を抽出し、数値に変換する """
    num = ""
    mode = 0 # 1 : int 2 : kansuuji
    sign = 1
    for ch in text:
        if ch in hankaku_num:
            num += ch
            mode |= 0x01
            continue
        elif ch in zenkaku_num:
            nch = findtable(ch, zenkaku_num, hankaku_num) # 全角を半角に変換する
            num += nch
            mode |= 0x01
            continue
        elif kansuuji.detect(ch): # 漢数字
            num += ch
            mode |= 0x02
            continue
        elif ch in ("-","+") and mode & 0x01:
            num += ch
            continue
        
        val = unicodedata.digit(ch, None)
        if val is not None:
            num += str(val)
            mode |= 0x01
        elif not num or ch in (" ","　",".",",","、","，","．"):
            continue # 数字が開始するまで進める、または桁を示す役物と空白をスキップする
        else:
            break # 数字が終わったとみなし離脱する　単位など
    try:
        if mode == 0x01:
            return int(num)
        elif mode == 0x02:
            return sign * kansuuji.parse(num, strict=False)
    except:
        return None


#
#
#
def norm_date_element(v: Union[str,int,None]):
    if v is None:
        return None
    elif isinstance(v, int):
        return v
    elif isinstance(v, str):
        v = v.strip()
        if "〓" in v or "？" in v or "?" in v:
            return None
        # 様々な数字
        return parse_int_numeric(v) # int | None
    else:
        raise TypeError(v)

def parse_date_like(s: str, *, year_month=False, month_day=False, day=None, year=None):
    """ 様々な形式の日付表現を/区切りの形式に統一する """
    # 代表的な区切り文字を探す
    parts = split_date(s)
    if len(parts) == 2:
        if year_month:
            parts.append(day or 1)
        elif month_day:
            parts.insert(year or datetime.date.today().year)
    if len(parts) == 3:
        y, m, d = parts[0:3]
        digits = [norm_date_element(x) for x in (y,m,d)]
        if any(x is not None for x in digits):
            return DateLike(*digits)
        
    # 漢字による区切り文字
    text = s
    year, sep, text = text.partition("年")
    if not sep:
        text = year
        year = None
    
    month, sep, text = text.partition("月")
    if not sep:
        text = month
        month = None

    day, sep, text = text.partition("日")
    if not sep:
        text = day
        day = None

    if any(x is not None for x in (year, month, day)):
        digits = [norm_date_element(x) for x in (year,month,day)]
        if any(x is not None for x in digits):
            return DateLike(*digits)
        
    # 数字のみ、固定長の日付
    if len(s) == 8:
        y = parse_int_numeric(s[0:4])
        m = parse_int_numeric(s[4:6])
        d = parse_int_numeric(s[6:8])
        if all(x is not None for x in (y,m,d)):
            return DateLike(year=y, month=m, day=d)

    return None

def norm_date_string(s: str, *, year_month=False, month_day=False, day=None, year=None):
    d = parse_date_like(s, year_month=year_month, month_day=month_day, day=day, year=year)
    if d is None:
        return None
    return d.as_date_string()

