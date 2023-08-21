from flask import Flask, jsonify
from whitenoise import WhiteNoise
import json
from oanda_api import OandaAPI

app = Flask(__name__)
app.wsgi_app = WhiteNoise(
    app.wsgi_app, root="static/", index_file=True, autorefresh=True
)

@app.route("/hello")
def hello():
    return("Hello")

@app.route("/kpi_data")
def get_kpi_data():
    # TODO:  Add robustness to this.
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
        return data              
    
@app.route("/kpi_data/<pair>")
def get_price_data(pair):
    data = OandaAPI.pricing_api(pair)
    return jsonify(data)

@app.route("/dumb_test")
def dumb_test():
    # return "Are we going to hit OandaAPI here?"
    return OandaAPI.dumb_test()

if __name__ == "__main__":
    app.run()
