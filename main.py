from math import floor
import scipy.io as sio

from bokeh.plotting import figure, show, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, CrosshairTool, PanTool, WheelZoomTool, UndoTool, \
    RedoTool, ResetTool, SaveTool, PolySelectTool

import numpy as np


# Different ways of extracting the matlab files - or their varying structure standards
def extract_old(filename):
    print("WARNING: YOU ARE USING THE OLD EXTRACTION CODE, WHICH IS REALLY SLOW AND BUGGY")
    file = sio.loadmat(filename)

    wave_timestamp = file['Sch_wav'][0][0][4]  # Neuron pop - milliseconds since trigger
    stim_timestamp = file['StimTrig'][0][0][4]  # Stimulus time into experiment - seconds
    stim_amplitude = file['StimTrig'][0][0][5]  # Amplitude of particular stimulus time

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

def extract_matlab_all(filename):
    ### --- STRUCTURE: xxxxxx_rec03_all.mat --- ###
    file = sio.loadmat(filename)

    wave_timestamp = file['Sch_wav'][0][0][4]  # Neuron pop - milliseconds since trigger
    stim_timestamp = file['StimTrig'][0][0][4]  # Stimulus time into experiment - seconds
    stim_amplitude = file['StimTrig'][0][0][5]  # Amplitude of particular stimulus time

    raw_values = []
    assorted_values = []
    final_values = []

    # Pair the amplitudes with stimulus time
    # Note: An Amplitude of 62 occurs between sets, null value
    for i in range(len(stim_timestamp)):
        raw_values += [[float("%.6f" % stim_timestamp[i][0]), stim_amplitude[i][0]]]

    # Calculates time difference between stimulus and pops for each group
    # then sorts them into sorted_values, before moving onto next group
    index = -1
    pops = []
    for j in wave_timestamp:
        if index < len(raw_values) - 1:
            if j > raw_values[index + 1][0]:
                # Add set to sorted_values
                if index > -1:
                    assorted_values.append([raw_values[index][0], raw_values[index][1], pops])
                # Move to next set of values
                index += 1
                pops = []

        if index > -1:
            # Compute time difference in ms, add to pops list
            difference = float("%.3f" % ((j - raw_values[index][0]) * 1000))
            if difference <= 50:
                pops += [difference]

    # Add final set to sorted_values
    assorted_values.append([raw_values[index][0], raw_values[index][1], pops])

    # Collate and order assorted_values into final_values
    # Each batch is separated by a None value in the final list
    batch = [[] for i in range(10)]
    for i in range(len(assorted_values)):
        if assorted_values[i][1] == 62:  # 62 separator
            # Append sorted batch, followed by a None to separate batches
            final_values += batch + [None]
        else:
            batch[assorted_values[i][1] - 1] = assorted_values[i]

    return final_values


# Sorts the values in separate sections to list of plot-able coordinates
def vals_to_coords(vals):
    values = []
    coords = []
    n = []

    for i in vals:
        if i == None:  # end row
            values += [n]
            n = []
        else:
            n += [i]

    for i in range(len(values)):
        for j in values[i]:
            for k in j[2]:
                coords += [(k, j[1]+(i/len(values)))]

    return coords


# Main plotting functions (call this from other code)
def bokeh_scatter(filename, auto_open=True, colour="black"):
    if type(filename) is not list:
        filename = [filename]

    for file in filename:
        extracted_file = extract_matlab_all(file)
        coordinates = vals_to_coords(extracted_file)
        print("data size: " + str(len(coordinates)))

        n = []
        x = []
        y = []
        for i in coordinates:
            n.append(floor(i[1]))
            x.append(i[0])
            y.append(i[1]-1)

        TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

        p = figure(tools=TOOLS, title="Scatter Plot: " + file[file.find('/')+1::])
        p.scatter(x, y, radius=0.1, fill_alpha=0.8, line_color=None, color=colour)

        p.sizing_mode = "stretch_both"
        p.border_fill_color = "whitesmoke"
        p.min_border_left = 80
        p.min_border_right = 80
        p.min_border_bottom = 80
        p.xaxis.axis_label = "Time (ms)"
        p.yaxis.axis_label = "Amplitude"

        for i in range(11):
            p.line((0, 50), (i, i), color=colour, alpha=0.5)

        name = file.replace('.mat', '') + '_scatter.html'
        title = "Scatter Plot: " + file[file.find('/')+1::]
        output_file(name, title)
        
        if auto_open:
            show(p)
        else:
            save(p)


def bokeh_composite(filename, auto_open=True, colour="black", w=500, h=250, radius=12):
    if type(filename) is not list:
        filename = [filename]

    for file in filename:
        extracted_file = extract_matlab_all(file)
        coordinates = vals_to_coords(extracted_file)
        print("data size: " + str(len(coordinates)))

        # Process data points for scatter plot
        n = []
        x = []
        y = []
        for i in coordinates:
            n.append(floor(i[1]))
            x.append(i[0])
            y.append(i[1] - 1)

        # Configure data and hovertext
        source = ColumnDataSource(data=dict(
            x=x,
            y=y,
            time=x,
            amp=n
        ))
        Hover = HoverTool(
            tooltips=[
                ("time", "@time ms"),
                ("amplitude", "@amp")
            ],
            names=["dots"]
        )


        # GENERATE PLOT WITH CUSTOM PROPERTIES
        TOOLS = [Hover, CrosshairTool(), PanTool(), WheelZoomTool(), UndoTool(), RedoTool(), ResetTool(), SaveTool(), PolySelectTool()]
        p = figure(tools=TOOLS, title="Composite Plot: " + file[file.find('/') + 1::], plot_width=50, plot_height=10)

        p.sizing_mode = "stretch_both"
        p.border_fill_color = "whitesmoke"
        p.min_border_left = 80
        p.min_border_right = 80
        p.min_border_bottom = 80
        p.xaxis.axis_label = "Time (ms)"
        p.yaxis.axis_label = "Amplitude"


        # ADD HEATMAP
        raw = np.zeros((h, w))
        top = 0

        # TODO: CLEAN UP CIRCLE CODE
        for pos in coordinates:
            x_pos = floor((pos[1]-1)/10*h)
            y_pos = floor(pos[0]/50*w)
            for i in range(-radius, radius+1):
                for j in range(-radius, radius+1):
                    x_pos_2 = x_pos+i
                    y_pos_2 = y_pos+j
                    if x_pos_2 >= 0 and x_pos_2 < h:
                        if y_pos_2 >= 0 and y_pos_2 < w:
                            if i*i + j*j < radius*radius:
                                raw[x_pos_2, y_pos_2] += 1
                                if raw[x_pos_2, y_pos_2] > top:
                                    top = raw[x_pos_2, y_pos_2]
        # Normalize
        for j in range(w):
            for i in range(h):
                raw[i, j] = (raw[i, j] / top)
                raw[i, j] = 1 - raw[i, j] #Invert data for colourmap

        p.image(image=[raw], x=0, y=0, dw=50, dh=10, palette="Inferno256")#"YlOrBr9")#


        # ADD SCATTER MAP
        p.scatter('x', 'y', radius=0.1, fill_alpha=0.8, line_color=None, color=colour, source=source, name="dots")


        # ADD AMPLITUDE LINES
        for i in range(11):
            p.line((0, 50), (i, i), color=colour, alpha=0.5)


        # SAVE AND SHOW PLOT
        name = file.replace('.mat', '') + '_composite.html'
        title = "Composite Plot: " + file[file.find('/') + 1::]
        output_file(name, title)

        if auto_open:
            show(p)
        else:
            save(p)





# --- TEMPORARY TESTING CODE; REMOVE IN FINAL BUILD --- #
if __name__ == '__main__':
    # print("Hello, World!")
    # help(go.XAxis)
    #plotly_scatter('temp/659601_rec03_all.mat')
    #plotly_heatmap('temp/659601_rec03_all.mat')

    #plotly_scatter('temp/659607_rec03_all.mat')
    bokeh_composite('temp/659607_rec03_all.mat')

    #print(extract_old('temp/659601_rec03_all.mat'))
    #print(extract_matlab_all('temp/659601_rec03_all.mat'))