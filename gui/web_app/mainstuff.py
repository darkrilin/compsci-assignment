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

# Main plotting function
def plot_with_plotly(filename, colorscale=cs_default):
    files = [filename]
    trace = {}

    for filename in files:
        sortedvals = parsematlab_rats.extractmatlab(filename)

        cheesarinoes = []
        n = []
        for i in sortedvals:
            if i == 62:
                cheesarinoes += [n]
                n = []
            else:
                n += [i]

        coordinates = []
        scale = len(cheesarinoes)

        for i in range(scale):
            for j in cheesarinoes[i]:
                y = j[1]+i/scale
                for n in j[2]:
                    x = n
                    coordinates += [(x,y)]

        trace[filename] = FF.create_2D_density (
            x = [i[0] for i in coordinates],
            y = [i[1] for i in coordinates],
            width = 800,
            height = 800,
            colorscale = colorscale,
            point_color = (0,0,0,0),
            point_size = 1,
            ncontours = 20
        )

        print(filename + " graphed successfully")

    for i in trace:
        plot(trace[i], filename=i+'.html', auto_open=False)


# TEMPORARY TESTING CODE; REMOVE IN FINAL BUILD
if __name__ == '__main__':
    files = ['659609_rec03_all.mat']
    for i in files:
        plot_with_plotly(i)