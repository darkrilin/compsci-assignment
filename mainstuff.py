import parsematlab_rats
sortedvals = parsematlab_rats.extractmatlab('659601_rec03_all.mat')

for i in sortedvals:
    print(i)