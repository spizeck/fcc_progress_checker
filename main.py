#!/usr/bin/python3
import csv
import pygal


def read_challenge_data(file_path):
    '''reads in a csv file from given path.

    params:
        file_path(string)       file path to csv file.

    returns:
        tupel                   returns tupel of day scores(list) and
                                dates(list).

    '''

    day_scores = list()
    dates = list()
    with open(file_path) as csv_f:
        reader = csv.reader(csv_f)
        for row, data in enumerate(reader):
            if row != 0:
                day_scores.append(int(data[0]))
                dates.append(data[2])
    return (day_scores, dates)


def write_challenge_data(file_path, new_data):
    '''appends a new line to the csv file containg the challenge data.

    params:
        file_path(string)       file path to csv file.
        new_data                data to be written in the file.

    returns:
        bool                    True on success and False otherwise.
    '''

    try:
        with open(file_path, 'a') as csv_f:
            writer = csv.writer(csv_f)
            writer.writerow(new_data)
        return True
    except e:
        return False


def create_chart(data, x_labels, data_label='data',
                 title='', save_path='chart.png'):
    '''creates a simple line chart based on input and saves it as png.

    params:
        data(list)              data to display on chart.
        x_labels(list)          list of labels for x-achsis.
        data_label(str)         name for the data on the chart.
                                default: 'data'
        title(str)              name of the chart. default: ''
        save_path               path for saving the char as png.
                                default: 'chart.png'

    returns:
        none
    '''

    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = x_labels
    line_chart.add(data_label, data)
    line_chart.render_to_png(save_path)


if __name__ == '__main__':
    # ToDo: clean up this mess when all works.
    csv_f = './challenge_data.csv'
    scores, dates = read_challenge_data(csv_f)
    create_chart(scores, dates,
                 data_label='challenges',
                 title='Reddopanda progress on FCC')
    # works
    # write_challenge_data(csv_f, [10, 111, '21.03.16'])
