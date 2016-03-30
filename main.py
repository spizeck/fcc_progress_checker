#!/usr/bin/python3
import argparse
import csv
from bs4 import BeautifulSoup
import urllib.request as request
from datetime import datetime
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import pygal


def read_challenge_data(file_path, all_data=False):
    """Reads in a csv file from given path.

        :param file_path: file path to csv file.
        :param all_data: Boolean flag to return all data or latest 7.
        Defaults to false.
        :type file_path: str
        :type all_data: bool
        :returns: returns tuple containing day scores(list),
        total_score(int) and dates(list).
        :rtype: tuple
    """

    day_scores = list()
    dates = list()
    total_score = 0
    with open(file_path) as csv_f:
        reader = csv.reader(csv_f)
        if all_data:
            for row, data in enumerate(reader):
                if row != 0:
                    day_scores.append(int(data[0]))
                    dates.append(data[2])
                    total_score = (data[1])
        else:
            for row in list(reader)[-7:]:
                day_scores.append(int(row[0]))
                dates.append(row[2])
                total_score = (row[1])

    return day_scores, total_score, dates


def write_challenge_data(file_path, new_data):
    """appends a new line to the csv file containing the challenge data.

        :param file_path: file path to csv file.
        :param new_data: data to be written in the file.
        :type file_path: str
        :returns: True on success and False otherwise.
        :rtype: bool
    """

    try:
        with open(file_path, 'a') as csv_f:
            writer = csv.writer(csv_f)
            writer.writerow(new_data)
        return True
    except IOError:
        return False


def create_chart(data, x_labels, data_label='data',
                 title='', save_path='chart.png'):
    """creates a simple line chart based on input and saves it as png.

        :param data: Data to display on chart.
        :param x_labels: List of labels for x-axis.
        :param data_label: Name for the data on the chart,
        default is 'data'.
        :param title: Name of the chart, default is ''.
        :param save_path: Path for saving the chart as png,
        default is 'chart.png'.
        :type data: list
        :type x_labels: list
        :type data_label: str
        :type save_path: str
        :returns: None

    """

    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = x_labels
    line_chart.add(data_label, data)
    line_chart.render_to_png(save_path)


def get_challenge_score(username):
    """grabs the current challenge score from given FreeCodeCamp user.

        :param username: Username of a FreeCodeCamp user.
        :type username: str
        :returns: Current challenge score of given user.
        :rtype: int
    """
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


def get_new_day_score(username, file_path):
    """calculates a new day score for given FCC user

        :param username: Username of a FreeCodeCamp user.
        :param file_path: Path of csv data file.
        :type username: str
        :type file_path: str
        :returns: List containing new day score, new total score,
        and the current date.
        :rtype: list
    """

    s, total_score, d = read_challenge_data(file_path)
    new_total_score = get_challenge_score(username)
    new_day_score = new_total_score - int(total_score)
    date = datetime.now()
    date_string = '{:02d}.{:02d}.{:4}'.format(date.day, date.month, date.year)

    return [new_day_score, new_total_score, date_string]


def send_mail(file_path, sender, receivers, pw):
    """sends an email with image attached to a list of addresses.

        :param file_path: Path to the image to attach.
        :param sender: E-mail address to send from.
        :param receivers: List of strings containing the e-mail addresses
        to send to.
        :param pw: String containing the password for sending.
        :type file_path: str
        :type sender: str
        :type receivers: list
        :type pw: str
        :returns: None
    """
    email = MIMEMultipart()
    email['Subject'] = 'Progress on FCC'
    email['From'] = sender
    email['To'] = ', '.join(receivers)

    with open(file_path, 'rb') as f:
        email.attach(MIMEImage(f.read()))

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(sender, pw)
    server.send_message(email)
    server.quit()


def main(arg):
    # file path to data csv
    csv_f = './challenge_data.csv'
    # get new challenge data and write them to file
    write_challenge_data(csv_f, get_new_day_score('reddosaurus', csv_f))
    # read in the challenge data
    scores, total_score, dates = read_challenge_data(csv_f, arg.all)
    create_chart(scores, dates,
                 data_label='challenges',
                 title='Reddosaurus progress on FCC')
    # path to chart image
    # maybe returning it later from create_chart function?
    msg = './chart.png'
    # send mail
    receiver_list = arg.reciever_adresses.split(',')
    send_mail(msg, arg.login_email, receiver_list, arg.password)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checks the progress on FCC.')
    parser.add_argument('-a', '--all', action='store_true', help='Setting \
                        option to use all data for char generation')
    parser.add_argument('login_email', help='E-mail address to send from')
    parser.add_argument('password', help='Password of login-email')
    parser.add_argument('receiver_addresses', help='Comma separated list of \
                        receiver addresses. No whitespaces allowed!')
    argument = parser.parse_args()
    main(argument)
