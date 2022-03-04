import csv
import re
import os
from pathlib import Path
from datetime import date, timedelta
import matplotlib.pyplot as plt
today = date(2002, 12, 31)
one_day = timedelta(1)

current_dir = os.path.dirname(__file__)

start_date = date(2022, 2, 12)

def getBofa():
    bofa_stmt = {}
    dir = str(Path(current_dir) / "bofa")
    for statement in os.listdir(dir):
        with open(str(Path(dir) / statement)) as file:
            data = file.read().split("\n")
            for line in data:
                m = re.match(r"\d+/\d+/\d+", line)
                if m:
                    parts = line.split(",")
                    date_parts = parts[0].split("/")
                    bal = parts[len(parts) - 1]
                    bal = float(bal[1:len(bal) - 1])
                    month = int(date_parts[0])
                    day = int(date_parts[1])
                    year = int(date_parts[2])
                    date_str = date(year, month, day).strftime(r"%m/%d/%y")
                    bofa_stmt[date_str] = bal
    
    balances = {"02/11/22": 1344.63}
    current_date = start_date
    while current_date != date.today():
        cur_date_str = current_date.strftime(r"%m/%d/%y")
        prev_day = (current_date - one_day).strftime(r"%m/%d/%y")

        if cur_date_str in bofa_stmt:
            balances[cur_date_str] = bofa_stmt[cur_date_str]
        else:
            balances[cur_date_str] = balances[prev_day]
        current_date = current_date + one_day
    return balances

def getCapitalOne():

    dir = str(Path(current_dir) / "capital-one")
    transactions = {}
    for statement in os.listdir(dir):
        with open(str(Path(dir) / statement)) as file:
            data = file.read().split("\n")
            for line in data:
                m = re.match(r"\d+-\d+-\d+", line)
                if m:
                    parts = line.split(",")
                    date_parts = parts[1].split("-")
                    month = int(date_parts[1])
                    day = int(date_parts[2])
                    year = int(date_parts[0])
                    date_str = date(year, month, day).strftime(r"%m/%d/%y")
                    credit = float(parts[6]) if parts[6] else 0
                    debit = float(parts[5]) if parts[5] else 0
                    transactions[date_str] = (transactions[date_str] if date_str in transactions else 0) + debit - credit

    balances = {"02/11/22": -54.68}
    current_date = start_date
    while current_date != date.today():
        cur_date_str = current_date.strftime(r"%m/%d/%y")
        prev_day = (current_date - one_day).strftime(r"%m/%d/%y")

        if cur_date_str in transactions:
            balances[cur_date_str] = balances[prev_day] + transactions[cur_date_str]
        else:
            balances[cur_date_str] = balances[prev_day]

        current_date = current_date + one_day
    return balances

def netWorth():
    net = {}
    bofa = getBofa()
    capitalOne = getCapitalOne()
    for date in bofa:
        net[date] = float("{:.2f}".format(bofa[date] - capitalOne[date]))

    return net



def makePlot():
    values = netWorth()
    x = []
    y = []

    current_date = start_date
    while current_date != date.today():
        cur_date_str = current_date.strftime(r"%m/%d/%y")
        x.append(cur_date_str)
        y.append(values[cur_date_str])
        current_date = current_date + one_day



    plt.plot(x, y)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.title("Net Worth")
    plt.xlabel("Date")
    plt.ylabel("USD ($)")
 
    plt.show()


if __name__ == "__main__":
    makePlot()