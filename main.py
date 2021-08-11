import csv
import numpy
import json

if __name__=="__main__":
    with open('./data1.txt','r') as f:
        json_data = json.load(f)
    ticks = json_data.keys()
    results = {}
    currentTick = 195836
    currentSqrtPrice = 1416420785473901422353916045772284
    plusTick = []
    minusTick = []
    for tick in ticks:
        tickInfo = json_data[tick]
        results[int(tick)] = {
            'liquidity': int(tickInfo['liquidity']),
            'feeGrowthInside0LastX128': int(tickInfo['feeGrowthInside0X']),
            'feeGrowthInside1LastX128': int(tickInfo['feeGrowthInside1X'])
        }
        if (int(tick) - currentTick > 0):
            plusTick.append(int(tick))
        else:
            minusTick.append(int(tick))
    plusTick.sort()
    minusTick.sort(reverse = True)
    maxTotals = 0
    maxIdx = -1
    for i in range(0, 50):
        total = 0
        liquidityDelta = pow(10,20) / (currentSqrtPrice / pow(2,96) - pow(1.0001, minusTick[i]/2))

        for j in range(0, i+1):
            total += results[plusTick[j]]['feeGrowthInside1LastX128'] * numpy.exp(-pow(abs(plusTick[j]-currentTick) *numpy.log(1.0001),2)) * (liquidityDelta /(liquidityDelta + results[plusTick[j]]['liquidity']))
            total += results[minusTick[j]]['feeGrowthInside1LastX128']* numpy.exp(-pow(abs(minusTick[j]-currentTick)*numpy.log(1.0001), 2)) *(liquidityDelta /(liquidityDelta + results[minusTick[j]]['liquidity']))

        if (maxTotals < total):
            maxIdx = i
            maxTotals = total
    print(maxIdx)