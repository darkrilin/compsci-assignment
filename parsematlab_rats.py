import scipy.io as sio

file = sio.loadmat('659605_rec03_all.mat')

#print(file['__header__'])
print(file['__header__'])
print(file.keys())

wave_timestamp = file['Sch_wav'][0][0][4]
stim_timestamp = file['StimTrig'][0][0][4]
stim_amplitude = file['StimTrig'][0][0][5]

stufflist = []

#print(len(wave_timestamp))
#print(len(stim_timestamp))
#print(len(stim_amplitude))

for i in range(len(stim_timestamp)):
    stufflist += [[float("%.6f" % stim_timestamp[i][0]), stim_amplitude[i][0]]]

for i in range(len(stufflist)):
    stime = stufflist[i][0]
    pops = []
    for j in wave_timestamp:
        if j>=stime:
            if j<=float(stime)+0.05:
                pops += [float("%.3f" % ((j[0]-float(stime))*1000))]
                #print((j[0]-float(stime))*1000)
            else:
                break
    stufflist[i] += [pops]

for i in stufflist:
    print(i)