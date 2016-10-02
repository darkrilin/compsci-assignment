import parsematlab_rats
import plotly.plotly as py
import plotly.graph_objs as go
from os import path, makedirs
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def plot_with_plotly(filename):
    files = [filename]
    trace = {}

    for filename in files: #allfiles:
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

        trace[filename] = go.Scatter(
            x = [i[0] for i in coordinates],
            y = [i[1] for i in coordinates],
            mode = 'markers',
            name = filename
        )

        print(filename + " graphed successfully")

    for i in trace:
        plot([trace[i]], filename=i+'.html')