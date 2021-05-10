#!/usr/local/bin/python3
import string
import json
from flask import Flask, render_template, request

app = Flask(__name__)


def data_load():
    try:
        with open('/Users/nursatsaduahasov/Downloads/Weather-App/data.json') as json_file:
            data = json.load(json_file)
    except:
        data = "There was a problem"
    return data


from ctypes import cdll, c_int
import numpy

lib = cdll.LoadLibrary('/Users/nursatsaduahasov/Downloads/Weather-App/libcalculation.so')


def get_day_temps(data):
    array = []
    for i in data:
        array.append(i["dayTemp"])
    return array


def get_night_temps(data):
    array = []
    for i in data:
        array.append(i["nightTemp"])
    return array


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        data = data_load()
        return render_template('home.html', data=data)
        # return render_template('home.html')

    if request.method == 'POST':
        lib.maxTemp.restype = c_int
        lib.minTemp.restype = c_int
        lib.averageTemp.restype = c_int
        lib.maxTemp.argtypes = [numpy.ctypeslib.ndpointer(dtype=numpy.int32)]
        lib.minTemp.argtypes = [numpy.ctypeslib.ndpointer(dtype=numpy.int32)]
        lib.averageTemp.argtypes = [numpy.ctypeslib.ndpointer(dtype=numpy.int32)]

        data = data_load()

        count = len(data)
        dayTemps = get_day_temps(data)
        nightTemps = get_night_temps(data)

        typedDayTemps = numpy.array(dayTemps, dtype=numpy.int32)
        typedNightTemps = numpy.array(nightTemps, dtype=numpy.int32)

        #HIGH button
        if request.form.get('submit_button') == 'Show max':
            maxDayTemp = lib.maxTemp(typedDayTemps, count)
            maxNightTemp = lib.maxTemp(typedNightTemps, count)
            result = "Maximum day temperature in June is " + str(maxDayTemp) + ", Maximum night temperature in June is " + str(maxNightTemp)
        # MIN button
        elif request.form.get('submit_button') == 'Show min':
            minDayTemp = lib.minTemp(typedDayTemps, count)
            minNightTemp = lib.minTemp(typedNightTemps, count)
            result = "Minimum day temperature in June is " + str(minDayTemp) + ", Minimum night temperature in June is " + str(minNightTemp)
        # AVG button
        elif request.form.get('submit_button') == 'Show avg':
            aveDayTemp = lib.averageTemp(typedDayTemps, count)
            aveNightTemp = lib.averageTemp(typedNightTemps, count)
            result = "Average day temperature in June is " + str(aveDayTemp) + ", Average night temperature in June is " + str(aveNightTemp)
        else:
            result = "No result yet!"
        return render_template('home.html', data=data, result=result)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)