# functions for common plots

# libraries
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sss

# functions


# Finds the area under a curve with a riemann sum
def integrate(xs, ys):
    h_first = 0.5*(xs[1]-xs[0])*ys[0]
    h_last = 0.5*(xs[-1]-xs[-2])*ys[-1]
    r_middle = sum([(xs[i]-xs[i-1])*ys[i] for i in range(1, len(xs)-1)])
    return h_first + h_last + r_middle


# Generates a kde and histogram for a list of points on a subplot (it is general(ish) but the variable names weren't worth changing)
def kde_and_hist(peak_time_differences, subplot, bin_width=0.1):
    peak_differences_xrange = [0, 2]
    peak_differences_xgrid = np.linspace(peak_differences_xrange[0], peak_differences_xrange[1], 1000)
    if len(peak_time_differences) > 1:
        bin_locs = np.arange(min(peak_time_differences), max(peak_time_differences) + bin_width, bin_width)
        subplot.hist(peak_time_differences, facecolor='green', alpha=0.1, bins=bin_locs, normed=1)
        density = sss.gaussian_kde(peak_time_differences)
        subplot.plot(peak_differences_xgrid, [density(peak_differences_xgrid)[i] for i in range(0, len(peak_differences_xgrid))])

'''
# dynamic plot example

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
su = fig.add_subplot(111)
su.axis([-1, 1, -1, 1])
plt.ion()

for i in range(1000):
    y = np.random.random()
    su.scatter(y**2, y)
    plt.pause(0.4)

while True:
    plt.pause(0.05)
'''


# Generates the ROC curve
def binary_roc_generator(vals, thresholds, answers):
    all_fps = []
    all_tps = []
    for j in range(0, len(thresholds)):
        positives = 0
        negitives = 0
        FPs = 0  # 1- specificity
        TPs = 0  # Sensitivity
        for i in range(0, len(vals)):
            if vals[i] != 'None':
                if answers[i] == 0:
                    negitives += 1
                    if vals[i] >= thresholds[j]:
                        FPs += 1
                elif answers[i] == 1:
                    positives += 1
                    if vals[i] >= thresholds[j]:
                        TPs += 1
        all_fps.append(FPs/negitives)
        all_tps.append(TPs/positives)
    return [all_fps, all_tps]


def sort_ascending_indices(array):  # not efficient # returns the indices, not the array
    sorted_array_indices = []
    not_placed = array.copy()
    for i in range(0, len(array)):
        min_index = exclusion_index_of(array, min(not_placed), sorted_array_indices)
        sorted_array_indices.append(min_index)
        not_placed.pop(not_placed.index(array[min_index]))
    return sorted_array_indices


def sorted_ascending_array(array):
    return [array[sort_ascending_indices(array)[i]] for i in range(0, len(sort_ascending_indices(array)))]


def exclusion_index_of(array, value, exclusion):
    index = 0
    for i in range(0, len(array)):
        if array[i] == value and i not in exclusion:
            index = i
    return index


def plot_roc(vals, thresholds, answers, fig):
    my_plot = fig.add_subplot(111)
    my_plot.set_xlabel("FPR")
    my_plot.set_title("ROC graph")
    my_plot.set_ylabel("TPR (Sensitivity)")
    my_plot.set_xlim(0, 1)
    my_plot.set_ylim(0, 1)
    points = binary_roc_generator(vals, thresholds, answers)
    point_order = sort_ascending_indices(points[0])
    points[0] = [points[0][point_order[i]] for i in range(0, len(point_order))]  # order them so the plot connects the points sequentially by FPR (the x value)
    points[1] = [points[1][point_order[i]] for i in range(0, len(point_order))]
    my_plot.scatter(points[0], points[1], s=100)
    my_plot.plot(points[0], points[1], linewidth=7, color='pink')
    my_plot.text(0.5, 0.2, "AUROC: " + str(round(integrate(points[0], points[1]), 3)))

    my_plot.plot(points[0], [0.5]*len(points[0]), color="green")
    my_plot.plot(points[0], [points[1][i] + 1 - points[0][i] - 0.5 for i in range(0, len(points[0]))], color="black")

    return integrate(points[0], points[1])


'''
# test data
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
random_binary_values = []
for i in range(0, 800):
    random_binary_values.append(round(np.random.rand()))

plot_roc(np.linspace(0, 9, 1000), np.linspace(0, 10, 100), [0]*100 + random_binary_values + [1]*100, fig)
plt.show()
'''
