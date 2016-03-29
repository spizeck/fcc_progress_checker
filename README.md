# Progress checker for FreeCodeCamp User

So this is a little Python script I wrote to check the progress of my girlfriend
on FreeCodeCamp. This is based on the completed challenges, so it's not a really
meaningful analysis of the progress.

Based on the completed challenges the script generates a line chart and sends it
to given email addresses. The line chart normally contains data of the last 7
days. With a command line flag you can create a chart based on all collected data.

This is one of my first little programming projects so it if you see problems,
errors or something that could be done better feel free to contribute or help.


## Install

After downloading it from Github you will need to install the requirements.

    pip install -r requirements.txt

And your done.


## Usage

The usage is pretty simple.

    python3 main.py [-a] sending-mail password list-of-receivers

The -a (--all) flag is optional. When set the generated chart uses
all collected data.

###### Example:
    python3 main.py test@test.com 123456 test1@test.com,test2@test.com

The example above sends a mail containing the chart image to the both mail
addresses via the test@test.com mail address.
