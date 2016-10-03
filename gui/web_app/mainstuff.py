import parsematlab_rats
import plotly.plotly as py
import plotly.graph_objs as go
import os
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def ensure_dir(f):
    d = os.path.dirname(os.getcwd() + f)
    if not os.path.exists(d):
        os.makedirs(d)

def plot_with_plotly(filename):
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

        trace[filename] = go.Scatter(
            x = [i[0] for i in coordinates],
            y = [i[1] for i in coordinates],
            mode = 'markers',
            name = filename
        )

        print(filename + " graphed successfully")

    for i in trace:
        plot([trace[i]], filename=i+'.html', auto_open=False)


# TEMPORARY TESTING CODE; REMOVE IN FINAL BUILD
if __name__ == '__main__':
    files = ['659601_rec03_all.mat']
    for i in files:
        plot_with_plotly(i)