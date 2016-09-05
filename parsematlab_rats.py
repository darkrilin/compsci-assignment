import scipy.io as sio

all_659602 = sio.loadmat('659602_rec03_all.mat')

#print(all_659602['__header__'])
print(all_659602.keys())
print(all_659602['__header__'])

wave_timestamp = all_659602['Sch_wav'][0][0][4]
stim_timestamp = all_659602['StimTrig'][0][0][4]
stim_amplitude = all_659602['StimTrig'][0][0][5]

print(len(wave_timestamp))
print(len(stim_timestamp))
print(len(stim_amplitude))
"""
for i in range(len(stim_timestamp)):
    print(stim_timestamp[i], stim_amplitude[i])
"""
for i in wave_timestamp:
    print(i)

#print(sch_wave)

#print(sch_wave[0], sch_wave[-1])
#print(stimtrig[0], stimtrig[-1])