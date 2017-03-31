import pandas as pd
import numpy as np


def meanRowFun(row, inputDf, start_range):
    # row.name (index)
    return round(inputDf[row.name - start_range:row.name + 1]['Share Price'].mean(),2)


def crossoverRowFun(row, sma, lma):
    crossover = False
    prevSma = sma.shift(1)[row.name]
    prevLma = lma.shift(1)[row.name]
    if np.isnan(prevSma) or np.isnan(prevLma):
        return np.nan
    if prevSma > prevLma and row['SMA'] <= row['LMA']:
        crossover = True
    elif prevSma < prevLma and row['SMA'] >= row['LMA']:
        crossover = True
    elif prevSma == prevLma and row['SMA'] != row['LMA']:
        crossover = True
    return crossover


def calculateMovingAverages(inputDf, sma=30, lma=300):
    avgDf = inputDf[lma - 1:].copy()
    avgDf['SMA'] = avgDf.apply(meanRowFun, args=(inputDf, sma - 1), axis=1)
    avgDf['LMA'] = avgDf.apply(meanRowFun, args=(inputDf, lma - 1), axis=1)
    avgDf['Crossover'] = avgDf.apply(crossoverRowFun, args=(avgDf['SMA'], avgDf['LMA']), axis=1)
    return avgDf


n = int(input().strip())
p = list(map(int, input().strip().split(' ')))

while len(p) < n:
    print("Not enough share prices")
    print('Enter {} values'.format(n))
    p = list(map(int, input().strip().split(' ')))

df = pd.DataFrame(data=[range(1, n + 1), p]).transpose()
df.columns = ['Days', 'Share Price']
res = calculateMovingAverages(df, 60, 300)
res.dropna(inplace=True)
res = res[res['Crossover'] == True]
res.apply(lambda row: print('{} {:0.5f} {:0.5f}'.format(row['Days'], row['SMA'], row['LMA'])), axis=1)
