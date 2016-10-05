import os
import parsematlab_rats
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
from plotly.offline import download_plotlyjs, plot, init_notebook_mode

init_notebook_mode()

# Color scales
cs_default = ['#EB3821', '#DDE22A', '#67BB47', '#6FCBD5', '#354D9D', '#D2D0E9']
cs_magma = ['#FBFABD', '#FD9A69', '#E85461', '#842681', '#360F6B', '#000000']
cs_heatmap = ['rgb(165,0,38)', 'rgb(215,48,39)', 'rgb(244,109,67)', 'rgb(253,174,97)', 'rgb(254,224,144)', 'rgb(224,243,248)', 'rgb(171,217,233)', 'rgb(116,173,209)', 'rgb(69,117,180)', 'rgb(49,54,149)']


# Create new folder if one doesn't already exist
def ensure_dir(f):
    d = os.path.dirname(os.getcwd() + f)
    if not os.path.exists(d):
        os.makedirs(d)
        return True
    return False

# Sorts the values in separate sections to list of plot-able coordinates
def vals_to_coords(vals):
    sortedvals = []
    coords = []
    n = []

    for i in vals:
        if i == 62:
            sortedvals += [n]
            n = []
        else:
            n += [i]

    for i in range(len(sortedvals)):
        for j in sortedvals[i]:
            for k in j[2]:
                coords += [(k, j[1]+(i/len(sortedvals)))]

    return coords

# Main plotting function (call this from other code)
def plot_with_plotly(filename, colorscale=cs_default):
    files = [filename]
    trace = {}

    for file in files:
        coordinates = vals_to_coords(parsematlab_rats.extractmatlab(file))

        trace[file] = FF.create_2D_density (
            x = [i[0] for i in coordinates],
            y = [i[1] for i in coordinates],
            width = 800,
            height = 800,
            colorscale = colorscale,
            point_color = (0,0,0,0),
            point_size = 1,
            ncontours = 20
        )

        print(file + " graphed successfully")

    for i in trace:
        plot(trace[i], filename=i+'.html')#, auto_open=False)





### --- TEMPORARY TESTING CODE; REMOVE IN FINAL BUILD --- ###
if __name__ == '__main__':
    files = ['659601_rec03_all.mat']
    for i in files:
        plot_with_plotly(i, cs_magma)