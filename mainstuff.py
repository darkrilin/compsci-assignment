import parsematlab_rats
sortedvals = parsematlab_rats.extractmatlab('659605_rec03_all.mat')

experiment_group = [[]]*10
print(experiment_group)
for i in sortedvals:
    if i[1] == 62:
        break
    else:
        experiment_group[i[1]-1] = i

print(experiment_group)