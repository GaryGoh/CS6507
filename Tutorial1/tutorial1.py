__author__ = 'GaryGoh'

import sys
import math
from pandas import read_csv
import numpy
import matplotlib.pyplot as plt




def main(argv):
    file_ngram = argv[0]
    file_happy = argv[1]
    year_start = 1900
    year_end = 2000

    print 'Data will be for years between %d and %d' % (year_start, year_end)

    data_ngram = read_csv(file_ngram)
    data_happy = read_csv(file_happy)

    for index, row in data_ngram.iterrows():
        # data_ngram.ix[index, 'word'] = row['word'].split("_")[0].lower()
        data_ngram.ix[index, 'word'] = row['word'].split("_")[0].lower()
    #

    years = range(year_start, year_end + 1)
    total_counts = [0] * len(years)
    scores = [0.0] * len(years)

    for yy in years:
        total_counts[years.index(yy)] = numpy.sum(data_ngram[data_ngram['year'].isin([yy])]['count'])

    h_avg = numpy.mean(data_happy['happiness_average'])

    for index, row in data_happy.iterrows():
        h_word = row['word']
        h_level = row['happiness_average']
        # Sanity check, print to terminal out current position
        print "Current word: %s (%d of %d) -> %.3f" % (h_word, index + 1, data_happy.shape[0], h_level)
        # Find the indecis of the rows of the word of interest
        word_info = data_ngram[data_ngram['word'].isin([h_word])]
        for yy in years:
            count = numpy.sum(word_info[word_info['year'].isin([yy])]['count'])
            if math.isnan(count):
                count = 0
            scores[years.index(yy)] = scores[years.index(yy)] + 1000 * (h_level - h_avg) * count / total_counts[
                years.index(yy)]

    temp = scores
    for ii in range(1, len(years) - 1):
        temp[ii] = sum(scores[ii - 1:ii + 2]) / 3

    scores = temp

    print scores  # Create the plot
    plt.plot(years, scores, 'r-')
    plt.ylabel('score')
    plt.xlabel('year')
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])