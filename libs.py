import datetime
#import requests
import json
#import sys


def solar_time():
    # pobranie czasu systemowego
    teraz = datetime.datetime.now()
    return str(teraz.strftime("%Y-%m-%dT%H:%M:%S"))

def data_converter(param):  # funkcja  sprawdzajaca i przeliczająca czy dodatnia czy ujemna

    if param > 0x8000:  # jest na minusie wartości
       return param - 0x10000

    return param






