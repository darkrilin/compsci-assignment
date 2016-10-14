from math import floor, hypot
import scipy.io as sio

import plotly.graph_objs as go
from plotly.offline import plot
from plotly import tools


# Color scales
cs_default = ['#EB3821', '#DDE22A', '#67BB47', '#6FCBD5', '#354D9D', '#D2D0E9']
cs_magma = ['#FBFABD', '#FD9A69', '#E85461', '#842681', '#360F6B', '#000000']
cs_heatmap = ['rgb(165,0,38)', 'rgb(215,48,39)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(254,224,144)',
              'rgb(224,243,248)', 'rgb(171,217,233)', 'rgb(116,173,209)', 'rgb(69,117,180)', 'rgb(49,54,149)']
cs_greyscale = ['rgb(0,0,0)', 'rgb(255,255,255)']


# Extract files from provided matlab structure
def extractmatlab(filename):
    file = sio.loadmat(filename)

    wave_timestamp = file['Sch_wav'][0][0][4]
    stim_timestamp = file['StimTrig'][0][0][4]
    stim_amplitude = file['StimTrig'][0][0][5]
    randomvals = []
    sortedvals = []

    for i in range(len(stim_timestamp)):
        randomvals += [[float("%.6f" % stim_timestamp[i][0]), stim_amplitude[i][0]]]

    for i in range(len(randomvals)):
        stime = randomvals[i][0]
        pops = []
        for j in wave_timestamp:
            if j >= stime:
                if j <= float(stime)+0.05:
                    pops += [float("%.3f" % ((j[0]-float(stime))*1000))]
                else:
                    break
        randomvals[i] += [pops]

    experimentbatch = [[]]*10
    for i in range(len(randomvals)):
        if randomvals[i][1] == 62:
            sortedvals += experimentbatch + [62]
        else:
            experimentbatch[randomvals[i][1]-1] = randomvals[i]

    return sortedvals


# Sorts the values in separate sections to list of plot-able coordinates
def vals_to_coords(vals):
    sortedvals = []
    coords = []
    n = []

    for i in vals:
        if i == 62:  # end row
            sortedvals += [n]
            n = []
        else:
            n += [i]

    for i in range(len(sortedvals)):
        for j in sortedvals[i]:
            for k in j[2]:
                coords += [(k, j[1]+(i/len(sortedvals)))]

    return coords


# Main plotting functions (call this from other code)
def plotly_scatter(filename, auto_open=True):
    if type(filename) is not list:
        filename = [filename]

    for file in filename:
        extractedfile = extractmatlab(file)
        coordinates = vals_to_coords(extractedfile)

        x = [[] for i in range(10)]
        y = [[] for i in range(10)]
        fig = tools.make_subplots(rows=10, cols=1, shared_xaxes=True, shared_yaxes=True, vertical_spacing=0)

        for i in coordinates:
            n = floor(i[1])-1
            x[n].append(i[0])
            y[n].append(i[1])

        for i in range(len(x)):
            fig.append_trace(
                go.Scatter(
                    x = x[i],
                    y = y[i],
                    yaxis = 'y'+str(i+1),
                    mode = "markers",
                    hoverinfo = "x",
                    marker = dict(
                        color = ["#000000"]
                    )),
                len(x)-i, 1
            )

        fig['layout'].update(title = "Scatter: "+file[file.find('/')+1::],
                             showlegend = False,
                             yaxis1 = dict(showticklabels = False),
                             yaxis2 = dict(showticklabels = False),
                             yaxis3 = dict(showticklabels = False),
                             yaxis4 = dict(showticklabels = False),
                             yaxis5 = dict(showticklabels = False, title = "Amplitude"),
                             yaxis6 = dict(showticklabels = False),
                             yaxis7 = dict(showticklabels = False),
                             yaxis8 = dict(showticklabels = False),
                             yaxis9 = dict(showticklabels = False),
                             yaxis10 = dict(showticklabels = False),
                             annotations = [
                                 dict(
                                     x = -0.015, y = 0.965-i*0.1035,
                                     text = str(10-i), showarrow = False,
                                     xref = 'paper', yref = "paper", align = "center") for i in range(10)
                             ])

        # TODO: Fix y axis labels, perhaps use annotations

        name = file.replace('.mat', '') + '_scatter.html'
        plot(fig, filename=name, auto_open=auto_open)
        print(name + " graphed - scatter")


def plotly_heatmap(filename, w=800, h=-1, radius=60, smooth=False, auto_open=True):

    if type(filename) is not list:
        filename = [filename]
    radius = int(radius * (w / 2500))
    width = w

    for file in filename:

        extractedfile = extractmatlab(file)
        if h == -1:
            height = len(extractedfile)
        else:
            height = h

        heatmap = [[0 for i in range(width)] for j in range(height)]
        for k in vals_to_coords(extractedfile):
            _x = floor(k[0] * width // 50)
            _y = floor(k[1] * height // 11)
            x1, x2 = max(0, min(width, _x - radius)), max(0, min(width, _x + radius))
            y1, y2 = max(0, min(height, _y - radius)), max(0, min(height, _y + radius))
            for i in range(x1, x2):
                for j in range(y1, y2):
                    pythag = hypot(_x - i, _y - j)
                    if pythag <= radius:
                        if smooth:
                            heatmap[j][i] += 1 - (pythag / radius) ** 1 / 2
                        else:
                            heatmap[j][i] += 1

        trace = [{
            'type': 'heatmap',
            'z': heatmap,
            'x': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
            'hoverinfo': 'z',
            'colorscale': -1,
        }]
        layout = go.Layout(
            title="Heatmap: "+file[file.find('/')+1::]
        )

        # TODO: fix axis labels

        name = file.replace('.mat', '') + '_heatmap.html'
        plot(go.Figure(data=trace, layout=layout), filename=name, auto_open=auto_open)
        print(name + " graphed - heatmap")





# --- TEMPORARY TESTING CODE; REMOVE IN FINAL BUILD --- #
if __name__ == '__main__':
    # plotly_heatmap('temp/659605_rec03_all.mat')
    # help(go.XAxis)
    plotly_scatter('temp/659601_rec03_all.mat')
