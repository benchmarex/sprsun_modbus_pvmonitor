import datetime
#import requests
import json
#import sys


def pobranie_czasu():
    # pobranie czasu systemowego
    teraz = datetime.datetime.now()
    pm_solartime = teraz.strftime("%Y-%m-%dT%H:%M:%S")
    return pm_solartime

def data_converter(param):  # funkcja sprawdzajaca czy dodatnia czy ujemna

    if param > 0x8000:  # jest na minusie wartości
        par = param - 0x10000
        return par
    par = param
    return par






