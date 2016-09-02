import scipy.io as sio

all_659602 = sio.loadmat('659602_rec03_all.mat')

print(all_659602['__header__'])
print(all_659602.keys())
print()
sch_wave = all_659602['Sch_wav'][0][0][4]
for i in sch_wave:
    print(i)
    #pass
stimtrig = all_659602['StimTrig'][0][0][4]
for i in stimtrig:
    #print(i)
    pass