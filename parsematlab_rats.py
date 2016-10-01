import scipy.io as sio

def extractmatlab(filename):
    # Fetch matlab data from the file
    file = sio.loadmat(filename)

    # Extract data into lists
    wave_timestamp = file['Sch_wav'][0][0][4]   # Timestamps of neurons firing
    stim_timestamp = file['StimTrig'][0][0][4]  # Timestamps of stimulus
    stim_amplitude = file['StimTrig'][0][0][5]  # Relative amplitude of stimulus
    randomvals = []
    sortedvals = []

    # Concatenating stimulus timestamp with amplitude
    for i in range(len(stim_timestamp)):
        randomvals += [[float("%.6f" % stim_timestamp[i][0]), stim_amplitude[i][0]]]

    # Calculate neuron fires within 50ms of trigger, add to list
    for i in range(len(randomvals)):
        stime = randomvals[i][0]
        pops = []
        for j in wave_timestamp:
            if j>=stime:
                if j<=float(stime)+0.05:
                    pops += [float("%.3f" % ((j[0]-float(stime))*1000))]
                else:
                    break
        randomvals[i] += [pops]

    # Sort batches of data based on amplitude
    experimentbatch = [[]]*10
    for i in range(len(randomvals)):
        if randomvals[i][1] == 62:
            sortedvals += experimentbatch + [62]
        else:
            experimentbatch[randomvals[i][1]-1] = randomvals[i]

    # FORMAT OF ITEMS IN SORTEDVALS:
    # [stim timestamp, stim amplitude, [list of neurons firing within 50ms of stim]]
    # WITH ITEMS OF [62] SEPARATING DATASETS
    return sortedvals