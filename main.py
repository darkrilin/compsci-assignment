from math import floor
import scipy.io as sio

from bokeh.plotting import figure, show, output_file, save, ColumnDataSource
from bokeh.models import HoverTool, CrosshairTool, PanTool, WheelZoomTool, ResetTool, SaveTool, CustomJS

from bokeh.models.widgets import Button
from bokeh.layouts import widgetbox, row, column

import matplotlib as plt
import matplotlib.cm as cm

import numpy as np


# Different ways of extracting the matlab files - or their varying structure standards
def extract_matlab(filename):
    '''
    --- SUPPORTED FILES ---

    - ******_rec03.mat
    - ******_rec03_all.mat
    - ******_rec03_f**.mat
    '''
    file = sio.loadmat(filename)
    wave_key = ""
    trig_key = "StimTrig"

    # Due to naming convention variations, it must search for the right keys
    schmitt = ["Schmitt", "Sch_wav"]
    for i in schmitt:
        if i in file.keys():
            wave_key = i

    if wave_key == "":
        raise KeyError("Can't find the schmitt wave data")

    # Extract data using keys
    file_comments  = file[wave_key][0][0][1][0]
    wave_timestamp = file[wave_key][0][0][4]  # Neuron pop - milliseconds since trigger
    stim_timestamp = file[trig_key][0][0][4]  # Stimulus time into experiment - seconds
    stim_amplitude = file[trig_key][0][0][5]  # Amplitude of particular stimulus time

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
        if not i:  # end row
            values += [n]
            n = []
        else:
            n += [i]

    for i in range(len(values)):
        for j in values[i]:
            for k in j[2]:
                coords += [(k, j[1]+(i/len(values)))]

    return coords


# Graphing and plotting functions
def generate_graph(extracted_file=None, raw_file="", scatter=False, heatmap=False,
                   hm_width=250, hm_height=125, hm_radius=10, widgets=False):

    # Initialise basic plot data
    plot_title = "Plot: "
    scatter_plot = None
    heatmap_plot = None
    toggle_scatter = None
    toggle_heatmap = None

    if (extracted_file == None and raw_file != ""):
        extracted_file = extract_matlab(raw_file)

    coordinates = vals_to_coords(extracted_file)
    tools = [CrosshairTool(), PanTool(), WheelZoomTool(), ResetTool(), SaveTool()]

    print("data size: " + str(len(coordinates)))

    # Process individual data points
    n = []
    x = []
    y = []
    for i in coordinates:
        n.append(floor(i[1]))
        x.append(i[0])
        y.append(i[1] - 1)

    # Configure hovertext for individual data points
    data_source = ColumnDataSource(data=dict(
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
    tools.append(Hover)

    # Determine plot title
    if (scatter and heatmap):
        plot_title = "Composite Plot: "
    elif (scatter):
        plot_title = "Scatter Plot: "
    elif (heatmap):
        plot_title = "Heatmap Plot: "

    # Initialise plot figure
    p = figure(tools=tools, title=plot_title + raw_file.split("/")[-1], plot_width=50, plot_height=10)

    p.sizing_mode = "stretch_both"
    p.border_fill_color = "whitesmoke"
    p.min_border_left = 40
    p.min_border_right = 40
    p.min_border_bottom = 50
    p.min_border_top = 20
    p.xaxis.axis_label = "Time (ms)"
    p.yaxis.axis_label = "Amplitude"
    p.width = 160
    p.height = 70

    # Add graphs to plot -- note: the order is important for layering
    if heatmap:
        heatmap_plot = add_heatmap(p, coordinates, w=hm_width, h=hm_height, radius=hm_radius)
    if scatter:
        scatter_plot = add_scatter(p, x, y, radius=0.06, source=data_source, name="dots")

    # Add amplitude lines to plot
    for i in range(11):
        p.line((0, 50), (i, i), color="black", alpha=0.5)

    # Widgets to toggle visibility of layers
    if widgets:
        if scatter:
            toggle_scatter = Button(
                label="Toggle Scatter Plot")
            toggle_scatter.width = 100
            toggle_scatter.js_on_click(CustomJS(args=dict(scatter_plot=scatter_plot),
                                                code="scatter_plot.visible=!scatter_plot.visible"))
        if heatmap:
            toggle_heatmap = Button(
                label="Toggle Heatmap")
            toggle_heatmap.width = 100
            toggle_heatmap.js_on_click(CustomJS(args=dict(heatmap_plot=heatmap_plot),
                                              code="heatmap_plot.visible=!heatmap_plot.visible"))

    # Return plot w/ widgets
    return p, toggle_scatter, toggle_heatmap


def add_scatter(p, x, y, radius=0.1, fill_alpha=0.8, line_color=None, color="black", source=None, name=""):
    if source != None:
        scatter = p.scatter(x, y, radius=radius, fill_alpha=fill_alpha, line_color=line_color, color=color, name=name)
    else:
        scatter = p.scatter(x, y, radius=radius, fill_alpha=fill_alpha, line_color=line_color, color=color, name=name)
    return scatter


def add_heatmap(p, coordinates, w=500, h=250, radius=10):
    # TODO: OPTIMISE THE CIRCLE CODE (there has to be a quicker way)
    raw = np.zeros((h, w))

    # Plot circles
    for pos in coordinates:
        x_pos = floor((pos[1] - 1) / 10 * h)
        y_pos = floor(pos[0] / 50 * w)
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                x_pos_2 = x_pos + i
                y_pos_2 = y_pos + j
                if x_pos_2 >= 0 and x_pos_2 < h:
                    if y_pos_2 >= 0 and y_pos_2 < w:
                        if i * i + j * j < radius * radius:
                            raw[x_pos_2, y_pos_2] += 1

    # Generate colour map
    colormap = cm.get_cmap("RdPu")
    bokeh_palette = [plt.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

    # Render image
    heatmap = p.image(image=[raw], x=0, y=0, dw=50, dh=10, palette=bokeh_palette)
    return heatmap


# Plotting for the website
def graph_single(file_name, widgets=True, width=500, height=250, radius=10, auto_open=True, dir=""):
    plot = generate_graph(raw_file=file_name, scatter=True, heatmap=True,
                          hm_width=width, hm_height=height, hm_radius=radius, widgets=widgets)

    file_dir = file_name.split("/")[0]
    file_name = file_name.split("/")[-1]

    if dir != "":
        file_dir = dir
        print(file_dir)

    name = file_dir + file_name.replace('.mat', '') + '.html'
    print(name)
    title = "Composite Plot: " + file_name
    output_file(name, title)

    show_me = plot[0]

    if widgets:
        doc_layout = column(
            [plot[0],
             row([widgetbox([plot[1], plot[2]], width=10)], height=50, sizing_mode="fixed")],
            sizing_mode="scale_width")
        show_me = doc_layout

    if auto_open:
        show(show_me)
    else:
        save(show_me)


def graph_multiple(file_names, scatter=True, heatmap=True, auto_open=False):
    pass


"""
def bokeh_scatter(filename, auto_open=True, colour="black"):

    if type(filename) is not list:
        filename = [filename]

    for file in filename:
        extracted_file = extract_matlab(file)
        coordinates = vals_to_coords(extracted_file)
        print("data size: " + str(len(coordinates)))

        n = []
        x = []
        y = []
        for i in coordinates:
            n.append(floor(i[1]))
            x.append(i[0])
            y.append(i[1]-1)

        tools = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo, \
                 reset,tap,save,box_select,poly_select,lasso_select,"

        p = figure(tools=tools, title="Scatter Plot: " + file[file.find('/')+1::])
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


def bokeh_composite(filename, auto_open=True, colour="black", w=500, h=250, radius=10):

    if type(filename) is not list:
        filename = [filename]

    print(filename)

    for file in filename:
        extracted_file = extract_matlab(file)
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
        tools = [Hover, CrosshairTool(), PanTool(), WheelZoomTool(), ResetTool(), SaveTool()]
        p = figure(tools=tools, title="Composite Plot: " + file.split("/")[-1], plot_width=50, plot_height=10)

        p.sizing_mode = "stretch_both"
        p.border_fill_color = "whitesmoke"
        p.min_border_left = 80
        p.min_border_right = 80
        p.min_border_bottom = 50
        p.min_border_top = 20
        p.xaxis.axis_label = "Time (ms)"
        p.yaxis.axis_label = "Amplitude"
        p.width = 160
        p.height = 70

        # ADD HEATMAP
        raw = np.zeros((h, w))

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

        # Fetch matplotlib colourmaps, convert to bokeh
        colormap = cm.get_cmap("RdPu")
        bokehpalette = [plt.colors.rgb2hex(m) for m in colormap(np.arange(colormap.N))]

        # Render image
        image = p.image(image=[raw], x=0, y=0, dw=50, dh=10, palette=bokehpalette)#"Inferno256")#"YlOrBr9")

        # ADD SCATTER MAP
        scatter = p.scatter('x', 'y', radius=0.07, fill_alpha=0.8, line_color=None, color=colour, source=source, name="dots")

        # ADD AMPLITUDE LINES
        for i in range(11):
            p.line((0, 50), (i, i), color=colour, alpha=0.5)

        # ADD WIDGETS TO TOGGLE VISIBILITY OF LAYERS
        toggle_image = Button(
            label="Toggle Heatmap")
        toggle_image.width = 100
        toggle_image.js_on_click(CustomJS(args=dict(image=image),
                                          code="image.visible=!image.visible"))

        toggle_scatter = Button(
            label="Toggle Scatter Plot")
        toggle_scatter.width = 100
        toggle_scatter.js_on_click(CustomJS(args=dict(scatter=scatter),
                                          code="scatter.visible=!scatter.visible"))

        # SAVE AND SHOW PLOT
        name = file.replace('.mat', '') + '_composite.html'
        title = "Composite Plot: " + file[file.find('/') + 1::]
        output_file(name, title)

        # OPEN / SHOW
        doc_layout = column(
            [p,
            row([widgetbox([toggle_image, toggle_scatter], width=10)], height=50, sizing_mode="fixed")],
            sizing_mode="scale_width")

        if auto_open:
            show(doc_layout)
        else:
            save(doc_layout)
"""


# --- TEMPORARY TESTING CODE; REMOVE IN FINAL BUILD --- #
if __name__ == '__main__':
    print("Make sure you're running app.py if you want the web interface")
    print("This code is just for debugging functions")

    graph_single("temp/659607_rec03_all.mat", widgets=True, width=500, height=200, radius=9)