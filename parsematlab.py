import h5py
import numpy as np
import matplotlib.pyplot as plt

with h5py.File('data/DPW1258PPG.mat', 'r') as f:
    key = list(f.keys())
    for i in key:
        data = f.get(i)
        a = list(data.keys())
        print(i, a)
        for x in list(data.values()):
            print(x.name.split('/')[-1], x.shape)
            for y in x:
                print(y)
