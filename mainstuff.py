import parsematlab_rats
sortedvals = parsematlab_rats.extractmatlab('659605_rec03_all.mat')

experiment_group = [[]]*10
for i in sortedvals:
    if i[1] == 62:
        break
    else:
        experiment_group[i[1]-1] = i

for i in experiment_group:
    print(i)