import settings
import requests
import pickle
import json
import math

from . import ml_api
from flask_restplus import Resource
from flask import abort, request

@ml_api.route("/")
class MachineLearningModel(Resource):

    def get(self):

        lat = request.args.get("lat")
        lon = request.args.get("lon")

        if not lat or not lon:
            abort(400, "Missing Latitude and Longitude")

        response = self.weatherData(lat, lon)
        filename = 'app/modules/ml/finalized_model.sav'
        logreg = pickle.load(open(filename, 'rb'))

        #Format for array ['HourlyDewPointTemperature', 'HourlyDryBulbTemperature', 'HourlyPrecipitation','RA',
        #                   'HourlyRelativeHumidity','HourlyWetBulbTemperature','HourlyWindSpeed']

        HourlyRelativeHumidity = response["current"]["humidity"]
        HourlyWindSpeed = response["current"]["wind_speed"]
        HourlyPrecipitation = response["current"]["rain"] if "rain" in response["current"] else 0
        RA = 1 if "rain" in response else 0
        HourlyDryBulbTemperature = response["current"]["temp"]
        HourlyDewPointTemperature = response["current"]["dew_point"]
        HourlyWetBulbTemperature = self.GetTWetBulbFromRelHum(HourlyDryBulbTemperature, HourlyRelativeHumidity/100)

        sample = [[HourlyDewPointTemperature,HourlyDryBulbTemperature,HourlyPrecipitation,RA,HourlyRelativeHumidity,HourlyWetBulbTemperature,HourlyWindSpeed]]
        q = logreg.predict(sample)
        print("q", q)
        print (q[0])

        resp = {
            "MLOutput": int(q[0]),
            "message": "Successful calculation of prediction"
        }

        return resp, 200

    def weatherData(self, lat, long):

        API_KEY = settings.API_KEY
        print(API_KEY)

        api_url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon=-{long}&exclude=hourly,daily&appid={API_KEY}&units=imperial"
        response = requests.get(api_url)

        print(json.dumps(response.json(), indent=2))
        return response.json()

    def GetTWetBulbFromRelHum(self, TDryBulb: float, RelHum: float) -> float:
        TWetBulb = TDryBulb * math.atan(0.151977 * math.pow((RelHum + 8.313659),0.5)) + math.atan(TDryBulb + RelHum) - math.atan(RelHum - 1.676331) + 0.00391838 *math.pow(RelHum,1.5) * math.atan(0.023101 * RelHum) - 4.686035
        return TWetBulb
