# Alexandre Erich Sebastien Georges 111079942
# Stony Brook University

from soil import Soil
import pandas

samples = []
df = pandas.read_csv('hw3.csv')

for i in range(len(df.index)):
    data = df.values[i]
    if data[4] == -1 and data[5] == -1:
        s = Soil(i, data[0], data[1], data[2], data[3], data[4], data[5], True)
    else:
        s = Soil(i, data[0], data[1], data[2], data[3], data[4], data[5], False)
    samples.append(s)

# Classifying samples from data csv
for sample in samples:
    print("Sample No.", sample.id)
    sample.classify()
    sample.plot()
    print("Classifies as ", sample.symbol, ", ", sample.name, "\n")

