from flask import Flask, request, jsonify
from flask_cors import CORS
from farmscore import calculate_farm_score

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Farm Score API is Running"

@app.route('/calculate', methods=['POST'])
def calculate():

    data = request.json

    lat = float(data['lat'])
    lon = float(data['lon'])

    # TEMPORARY SAMPLE VALUES
    # Later replace with Earth Engine data

    gw = 32
    ndvi = 72
    ndmi = 55
    rainfall = 45
    temp = 36

    result = calculate_farm_score(
        gw,
        ndvi,
        ndmi,
        rainfall,
        temp
    )

    return jsonify({
        "latitude": lat,
        "longitude": lon,
        "groundwater": gw,
        "ndvi": ndvi,
        "ndmi": ndmi,
        "rainfall": rainfall,
        "temperature": temp,
        "rainfall_score": result["rainfall_score"],
        "temperature_score": result["temperature_score"],
        "final_score": result["final_score"]
    })

if __name__ == '__main__':
    app.run(debug=True)
