import pytest
from ageha.numeric import compose_number
from ageha.japanese.numeric import kansuuji, write_kansuuji, write_unit_kansuuji

def test_composenum():
    composenum = compose_number
    assert composenum(0, [1,2,3]) == 123
    assert composenum(4, [1,2,3]) == 1230000
    assert composenum(0, []) == 0
    assert composenum(3, [4,0,5]) == 405000
    assert composenum(0, [1000,2000,3000]) == 123000
    assert composenum(0, [1111,3000,5000]) == 146100

def test_jp_write_numeric():
    assert "一九八四" == write_kansuuji(1984)
    assert "一〇八四" == write_kansuuji(1084)
    assert "三二〇一" == write_kansuuji(3201)
    assert "一一〇〇" == write_kansuuji(1100)
    assert "一〇〇〇" == write_kansuuji(1000)
    assert "一万" == write_kansuuji(10000)
    assert "一万七六" == write_kansuuji(10076)
    assert "一万二〇〇四" == write_kansuuji(12004)
    assert "二三四万五六七八" == write_kansuuji(2345678)
    assert "一億二三四五万六七八九" == write_kansuuji(123456789)
    assert "〇" == write_kansuuji(0)
    
    assert "千九百八十四" == write_unit_kansuuji(1984)
    assert "千八十四" == write_unit_kansuuji(1084)
    assert "三千二百一" == write_unit_kansuuji(3201)
    assert "千百" == write_unit_kansuuji(1100)
    assert "千" == write_unit_kansuuji(1000)
    assert "二百三十四万五千六百七十八" == write_unit_kansuuji(2345678)
    assert "一億二千三百四十五万六千七百八十九" == write_unit_kansuuji(123456789)
    assert "〇" == write_unit_kansuuji(0)

    assert "一九八四" == kansuuji.nounit_write(1984)
    assert "一〇八四" == kansuuji.nounit_write(1084)
    assert "三二〇一" == kansuuji.nounit_write(3201)
    assert "一一〇〇" == kansuuji.nounit_write(1100)
    assert "一〇〇〇" == kansuuji.nounit_write(1000)
    assert "一〇〇〇〇" == kansuuji.nounit_write(10000)
    assert "一〇〇七六" == kansuuji.nounit_write(10076)
    assert "一二〇〇四" == kansuuji.nounit_write(12004)
    assert "二三四五六七八" == kansuuji.nounit_write(2345678)
    assert "一二三四五六七八九" == kansuuji.nounit_write(123456789)
    assert "〇" == kansuuji.nounit_write(0)

def test_jp_parse_numeric():
    assert kansuuji.parse("一九八四") == 1984
    assert kansuuji.parse("一〇八四") == 1084
    assert kansuuji.parse("三二〇一") == 3201
    assert kansuuji.parse("一一〇〇") == 1100
    assert kansuuji.parse("一〇〇〇") == 1000
    assert kansuuji.parse("一万") == 10000
    assert kansuuji.parse("一万七六") == 10076
    assert kansuuji.parse("一万二〇〇四") == 12004
    assert kansuuji.parse("二三四万五六七八") == 2345678
    assert kansuuji.parse("一億二三四五万六七八九") == 123456789
    assert kansuuji.parse("〇") == 0
    
    assert kansuuji.parse("千九百八十四") == 1984
    assert kansuuji.parse("千八十四") == 1084
    assert kansuuji.parse("三千二百一") == 3201
    assert kansuuji.parse("千百") == 1100
    assert kansuuji.parse("千") == 1000
    assert kansuuji.parse("二百三十四万五千六百七十八") == 2345678
    assert kansuuji.parse("一億二千三百四十五万六千七百八十九") == 123456789
    assert kansuuji.parse("〇") == 0

    assert kansuuji.parse("一九八四") == 1984
    assert kansuuji.parse("一〇八四") == 1084
    assert kansuuji.parse("三二〇一") == 3201
    assert kansuuji.parse("一一〇〇") == 1100
    assert kansuuji.parse("一〇〇〇") == 1000
    assert kansuuji.parse("一〇〇〇〇") == 10000
    assert kansuuji.parse("一〇〇七六") == 10076
    assert kansuuji.parse("一二〇〇四") == 12004
    assert kansuuji.parse("二三四五六七八") == 2345678
    assert kansuuji.parse("一二三四五六七八九") == 123456789
    assert kansuuji.parse("〇") == 0

    assert kansuuji.parse("二那由他") == 2 * pow(10, 60)
    assert kansuuji.parse("千二百三十四恒河沙四千五百六十七極七千八百九十九正") == 1234 * pow(10, 52) + 4567 * pow(10, 48) + 7899 * pow(10, 40)


    