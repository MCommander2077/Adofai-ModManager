# file: current_date_time.py
# !/usr/bin/python

from PyQt6.QtCore import QDate, QTime, QDateTime, Qt


def get_date_time():
    now = QDate.currentDate()
    list = []
    list.append(now.toString(Qt.DateFormat.ISODate))
    list.append(now.toString(Qt.DateFormat.RFC2822Date))

    datetime = QDateTime.currentDateTime()

    list.append(datetime.toString())

    time = QTime.currentTime()
    list.append(time.toString(Qt.DateFormat.ISODate)
    return list
