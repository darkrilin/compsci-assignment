import scipy.io as sio

def extractmatlab(filename):
    # Fetch matlab data from the file
    file = sio.loadmat(filename)

    # Extract data into lists
    wave_timestamp = file['Sch_wav'][0][0][4]   # Timestamps of neurons firing
    stim_timestamp = file['StimTrig'][0][0][4]  # Timestamps of stimulus
    stim_amplitude = file['StimTrig'][0][0][5]  # Relative amplitude of stimulus
    sortedvals = []

    for i in range(len(stim_timestamp)): # Concatenating stimulus timestamp with amplitude
        sortedvals += [[float("%.6f" % stim_timestamp[i][0]), stim_amplitude[i][0]]]

    for i in range(len(sortedvals)): # Calculate neuron fires within 50ms of trigger, add to list
        stime = sortedvals[i][0]
        pops = []
        for j in wave_timestamp:
            if j>=stime:
                if j<=float(stime)+0.05:
                    pops += [float("%.3f" % ((j[0]-float(stime))*1000))]
                else:
                    break
        sortedvals[i] += [pops]

    # FORMAT OF ITEMS IN SORTEDVALS:
    # [stim timestamp, stim amplitude, [list of neurons firing within 50ms of stim]]
    return sortedvals

if __name__ == '__main__':
    data_extract = extractmatlab('659605_rec03_all.mat')
    for i in data_extract:
        print(i)