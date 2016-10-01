import parsematlab_rats
import plotly.plotly as py
import plotly.graph_objs as go
sortedvals = parsematlab_rats.extractmatlab('659605_rec03_all.mat')
py.sign_in('tay0008', '9f03ec53cm')

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

trace = go.Scatter(
    x = [i[0] for i in coordinates],
    y = [i[1] for i in coordinates],
    mode = 'markers'
)

data = [trace]

py.iplot(data, filename='test-scatter_02')