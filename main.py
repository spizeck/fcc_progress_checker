#!/usr/bin/python3
import csv
from bs4 import BeautifulSoup
import urllib.request as request
from datetime import datetime
import smtplib
import pygal


def read_challenge_data(file_path):
    '''reads in a csv file from given path.

    params:
        file_path(string)       file path to csv file.

    returns:
        tupel                   returns tupel containg day scores(list),
                                total_score(int) and dates(list).

    '''

    day_scores = list()
    dates = list()
    total_score = 0
    with open(file_path) as csv_f:
        reader = csv.reader(csv_f)
        for row, data in enumerate(reader):
            if row != 0:
                day_scores.append(int(data[0]))
                dates.append(data[2])
                total_score = (data[1])

    return (day_scores, total_score, dates)


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
        username(string)        username of a FreeCodeCamp user.

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


def get_new_day_score(username):
    '''calculates a new day score for given FCC user

    params:
        username(string)        username of a FreeCodeCamp user.

    returns:
        list                    list containg new day score, new total score
                                and the current date.
    '''

    s, total_score, d = read_challenge_data(csv_f)
    new_total_score = get_challenge_score(username)
    new_day_score = new_total_score - int(total_score)
    date = datetime.now()
    date_string = '{:02d}.{:02d}.{:4}'.format(date.day, date.month, date.year)

    return [new_day_score, new_total_score, date_string]


def send_mail(msg, sender, recievers, pw):
    for reciever in recievers:
        email = '\r\n'.join([
            'From: ' + sender,
            'To: ' + reciever,
            'Subject: FCC Check',
            '',
            msg
        ])
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(sender, pw)
        server.sendmail(sender, reciever, email)
        server.quit()


if __name__ == '__main__':
    # ToDo: clean up this mess when all works.
    csv_f = './challenge_data.csv'
    scores, total_score, dates = read_challenge_data(csv_f)
    create_chart(scores, dates,
                 data_label='challenges',
                 title='Reddosaurus progress on FCC')
    # works
    write_challenge_data(csv_f, get_new_day_score('reddosaurus'))
    print(get_challenge_score('reddosaurus'))
    msg = 'Someone did something!'
    send_mail(msg, 'sender', ['resiever'], 'Passwort')
