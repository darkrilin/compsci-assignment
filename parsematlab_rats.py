import scipy.io as sio

file = sio.loadmat('659605_rec03_all.mat')

print(file['__header__'])
print(file.keys())

wave_timestamp = file['Sch_wav'][0][0][4]
stim_timestamp = file['StimTrig'][0][0][4]
stim_amplitude = file['StimTrig'][0][0][5]

sortedvals = []

for i in range(len(stim_timestamp)):
    sortedvals += [[float("%.6f" % stim_timestamp[i][0]), stim_amplitude[i][0]]]

for i in range(len(sortedvals)):
    stime = sortedvals[i][0]
    pops = []
    for j in wave_timestamp:
        if j>=stime:
            if j<=float(stime)+0.05:
                pops += [float("%.3f" % ((j[0]-float(stime))*1000))]
            else:
                break
    sortedvals[i] += [pops]

for i in sortedvals:
    print(i)
"""
experiment_group = [[]]*10
print(experiment_group)
for i in sortedvals:
    if i[1] == 62:
        break
    else:
        experiment_group[i[1]-1] = i

print(experiment_group)
"""