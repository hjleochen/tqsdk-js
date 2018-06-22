function* sar (C) {
    C.DEFINE({
        type: "MAIN",
        cname: "抛物线指标",
        state: "KLINE",
    });

    let n = C.PARAM(4, "N"); // 计算周期
    let step = C.PARAM(0.02, "Step", {type: "DOUBLE"}); // 步长
    let max = C.PARAM(0.2, "Max", {type: "DOUBLE"}); // 极值

    let sar = C.OUTS("COLORDOT", "Sar");

    let af = 0; // 加速因子
    let uptrend = undefined;
    let isReverse = false;

    function setSar(i, isUp, val){
        sar[0][i] = val;
        if (isUp) {
            sar[1][i] = RED;
        } else {
            sar[1][i] = GREEN;
        }
    }

    while(true) {
        let i = yield;
        if(!sar[0][i]) {
            if (!sar[0][i - 1]) {
                uptrend = C.DS.close[i] - C.DS.open[i] > 0;
                uptrend ? setSar(i, uptrend, LOWEST(i-1, C.DS.low, n)) : setSar(i, uptrend, HIGHEST(i-1, C.DS.high, n));
            } else if (sar[1][i - 1] == RED) {
                // 上一次上升趋势
                if (C.DS[i - 1].low < sar[0][i - 1]) { // 本次需要转向
                    setSar(i, false, HIGHEST(i-1, C.DS.high, n));
                    af = 0;
                } else {
                    if (C.DS[i - 1].high > C.DS[i - 2].high) {
                        af = Math.min(af + step, max);
                    } else {
                        af = af == 0 ? step : af;
                    }
                    setSar(i, true, sar[0][i - 1] + af * (C.DS[i - 1].high - sar[0][i - 1]));
                }
            } else {
                if (C.DS[i - 1].high > sar[0][i - 1]) {
                    setSar(i, true, LOWEST(i-1, C.DS.low, n));
                    af = 0;
                } else {
                    if (C.DS[i - 1].low < C.DS[i - 2].low) {
                        af = Math.min(af + step, max);
                    } else {
                        af = af == 0 ? step : af;
                    }
                    setSar(i, false, sar[0][i - 1] - af * (sar[0][i - 1] - C.DS[i - 1].low));
                }
            }
        }
    }
}