__author__ = 'GaryGoh'

import sys
import math
import pandas
import numpy
import random
from operator import itemgetter
import matplotlib.pyplot as plt


def distance(x, x_medoid, y, y_medoid):
    return math.sqrt((x - x_medoid) ** 2 + (y - y_medoid) ** 2)


def main(argv):
    # Getting data from csv files
    data_points = pandas.read_csv(argv[0])
    data_sol = pandas.read_csv(argv[1])

    # Re-format the data in order to plot out the solution.
    # One more column for storing index to save searching time.
    data_points = pandas.DataFrame(data_points, columns=['x', 'y', 'cost', 'index_medoid'])


    # data-preparation
    # pre-compute mean-value for each columns
    x_mean = numpy.mean(data_points['x'])
    y_mean = numpy.mean(data_points['y'])

    # Handling missing value, a naive way.
    # Detecting non-numeric value and transform, also with a naive way.
    for points_index, points_row in data_points.iterrows():
        if (data_points.ix[points_index, 'x'] is None) or (
                not isinstance(data_points.ix[points_index, 'x'], (int, float, long, complex))):
            data_points.ix[points_index, 'x'] = x_mean
        if (data_points.ix[points_index, 'y'] is None) or (
                not isinstance(data_points.ix[points_index, 'y'], (int, float, long, complex))):
            data_points.ix[points_index, 'y'] = y_mean

    # Choosing medoid from data_sol and labeling them on data_points.
    for points_index, points_row in data_points.iterrows():
        sorted_medoids = []
        for sol_index, sol_row in data_sol.iterrows():
            # calculating the euclidean distance for each medoid, including medoids themselves.
            sorted_medoids.append((distance(data_points.ix[points_index, 'x'], data_points.ix[sol_row['medoid'], 'x'],
                                            data_points.ix[points_index, 'y'], data_points.ix[sol_row['medoid'], 'y']),
                                   sol_index))

            # update column in order to sum up cost and plot points.
        data_points.ix[points_index, 'cost'] = min(sorted_medoids, key=itemgetter(0))[0]
        data_points.ix[points_index, 'index_medoid'] = min(sorted_medoids, key=itemgetter(0))[1]

        # Release the list to free memory.
        del sorted_medoids

    # Sum up the cost
    print numpy.sum(data_points['cost'])

    # Write to CSV file.
    data_points.to_csv('points.csv', model='a', header=True, index=False, columns=['x', 'y', 'cost'])


    # Plot out
    # generate the different color to represent the point belongs to which closest medoid.
    color_medoid = []
    for i in range(0, len(data_sol.index)):
        # (R, G, B) from range of 0 to 1 in each element.
        color_medoid.append([(random.random(), random.random(), random.random())])

    for points_index, points_row in data_points.iterrows():
        plt_index_medoid = int(points_row['index_medoid'])
        plt_x = points_row['x']
        plt_y = points_row['y']

        plt.plot(plt_x, plt_y, 'o',
                 color=color_medoid[plt_index_medoid][0])
    plt.plot(data_points.ix[data_sol['medoid'], 'x'], data_points.ix[data_sol['medoid'], 'y'], "rs", label='medoid',
             markersize=10)
    plt.title("Project1 by Mingqian Gao")
    plt.legend()
    plt.show()
    return


if __name__ == "__main__":
    main(sys.argv[1:])