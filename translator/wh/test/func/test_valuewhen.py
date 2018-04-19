#!/usr/bin/env python
#coding=utf-8

import unittest
from wh.test.base import TestConvert



class TestConvertIndicator(TestConvert):
    """
    VALUEWHEN(COND,X) 当COND条件成立时，取X的当前值。如COND条件不成立，则取上一次COND条件成立时X的值。

    注：
    X可以是数值也可以是条件。

    例1
    VALUEWHEN(HIGH>REF(HHV(HIGH,5),1),HIGH);表示当前最高价大于前五个周期最高价的最大值时返回当前最高价
    例2：
    VALUEWHEN(DATE<>REF(DATE,1),O);表示取当天第一根k线的开盘价（即当天开盘价）
    例3：
    VALUEWHEN(DATE<>REF(DATE,1),L>REF(H,1));//表示在当天第一根k线上判断当前最低价是否大于昨天最后一根K线的最高价。返回1，说明当天跳空高开。返回0，说明当天不满足跳空高开条件。
    """
    def test_dmi(self):
        case = {
            "id": "FUNC",
            "cname": "FUNC",
            "type": "SUB",
            "src": """
        VALUEWHEN(HIGH>REF(HHV(HIGH,5),1),HIGH);
        VALUEWHEN(DATE<>REF(DATE,1),O);
        VALUEWHEN(DATE<>REF(DATE,1),L>REF(H,1));
        """,
            "params": [
            ],
            "expected": """
            
function* FUNC(C){
C.DEFINE({
type: "SUB",
cname: "FUNC",
state: "KLINE",
yaxis: [],
});
//定义指标参数

//输入序列
let HIGH = C.SERIAL("HIGH");
let DATE = C.SERIAL("DATE");
let OPEN = C.SERIAL("OPEN");
let LOW = C.SERIAL("LOW");
//输出序列
let S_1 = C.OUTS("LINE", "S_1", {color: RED});
let S_4 = C.OUTS("LINE", "S_4", {color: GREEN});
let S_6 = C.OUTS("LINE", "S_6", {color: BLUE});
//临时序列
let S_2 = [];
let S_3 = [];
let S_5 = [];
let S_7 = [];
let S_8 = [];
//指标计算
while(true){
let i = yield;
S_3[i]=HIGHEST(i, HIGH, 5);
S_2[i]=HIGH[i] > REF(i, S_3, 1);
S_1[i]=HIGH[NEAREST(i, S_2)];
S_5[i]=DATE[i] <> REF(i, DATE, 1);
S_4[i]=OPEN[NEAREST(i, S_5)];
S_7[i]=DATE[i] <> REF(i, DATE, 1);
S_8[i]=LOW[i] > REF(i, HIGH, 1);
S_6[i]=S_8[NEAREST(i, S_7)];
}
}        
                """,
        }

        self.assert_convert(case)


if __name__ == '__main__':
    unittest.main()