from flask import Flask, request, jsonify
from farmscore import calculate_farm_score

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])

def calculate():

    data = request.json

    lat = data['lat']
    lon = data['lon']

    # Temporary sample values
    gw = 32
    ndvi = 72
    ndmi = 55
    rainfall = 45
    temp = 36

    final_score = calculate_farm_score(
        gw,
        ndvi,
        ndmi,
        rainfall,
        temp
    )

    return jsonify({
        "final_score": final_score
    })

if __name__ == '__main__':
    app.run(debug=True)
