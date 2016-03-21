#!/usr/bin/python3
import csv
from bs4 import BeautifulSoup
import urllib.request as request
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


def get_challenge_score(username):
    '''grabs the current challenge score from given FreeCodeCamp user.

    params:
        username(string)        username of a FreeCodeCamp user

    returns:
        int                     current challenge score of given user.
    '''
    score = ''
    url = 'https://www.freecodecamp.com/{}'.format(username)
    # build new Request object to provide a valid User-Agent
    req = request.Request(url,
                          data=None,
                          headers={'User-Agent':
                                   'Mozilla/5.0 (X11; U; Linux i686)\
                                    Gecko/20071127 Firefox/2.0.0.11'})

    with request.urlopen(req) as response:
        fcc_html = BeautifulSoup(response, 'html.parser')
        score_tag = fcc_html.find('h1', class_='flat-top text-primary')
        score = score_tag.get_text().translate({
            ord('['): '',
            ord(']'): '',
            ord(' '): ''
        })
    return int(score)


if __name__ == '__main__':
    # ToDo: clean up this mess when all works.
    csv_f = './challenge_data.csv'
    scores, dates = read_challenge_data(csv_f)
    create_chart(scores, dates,
                 data_label='challenges',
                 title='Reddosaurus progress on FCC')
    # works
    # write_challenge_data(csv_f, [10, 111, '21.03.16'])
    print(get_challenge_score('reddosaurus'))
