#!/usr/local/bin/python3

#we replaced it with json file, due to  cost

from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def format_response(city, month, day):
    weather_key = "b53f85e11c439a668fb9a6e3ac4424bc"
    url = "http://history.openweathermap.org/data/2.5/aggregated/day"
    params = {"APPID": weather_key, "id": city, "month": month, "day": day, "units": "Metric"}
    response = requests.get(url, params=params)
    weather = response.json()
    try:
        name = weather['code']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']

        final_str = "City: %s \nCondition: %s \nTemperature (C): %s" % (name, desc, temp)
    except:
        final_str = "There was a problem"
    return final_str


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

    if request.method == 'POST':
        city = request.form['city']
        weather_data = format_response(city, 6, 1)
        return render_template('home.html', data=weather_data)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)