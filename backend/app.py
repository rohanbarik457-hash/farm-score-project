"""
app.py
======
Flask REST API for the FarmScore agricultural-suitability platform.

Endpoints
---------
POST /calculate
    Accept ``{"lat": float, "lng": float}``, query Google Earth Engine
    for satellite data, compute the FarmScore, and return the result.

GET /health
    Lightweight health-check for load-balancers / uptime monitors.
"""

```python
from __future__ import annotations

import logging
import os
import sys
import time

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

from earth_engine_service import fetch_farm_data, initialise_earth_engine
from scoring import calculate_score

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
PORT = int(os.getenv("PORT", 10000))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------------
app = Flask(__name__)

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

# ---------------------------------------------------------------------------
# Earth Engine Initialisation
# ---------------------------------------------------------------------------
@app.before_request
def _ensure_ee_init():
    try:
        initialise_earth_engine()
    except Exception as exc:
        logger.error("Earth Engine init failed: %s", exc)

        if request.endpoint != "health_check":
            raise

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "FarmScore API",
        "status": "running"
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "service": "FarmScore API",
        "status": "ok"
    }), 200


@app.route("/calculate", methods=["POST", "OPTIONS"])
def calculate():

    # Handle CORS Preflight
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    # -----------------------------------------------------------------------
    # Parse Request
    # -----------------------------------------------------------------------
    body = request.get_json(silent=True)

    if not body:
        return jsonify({
            "error": "Request body must be valid JSON"
        }), 400

    lat = body.get("lat")
    lng = body.get("lng")

    if lat is None or lng is None:
        return jsonify({
            "error": "Both 'lat' and 'lng' are required"
        }), 400

    try:
        lat = float(lat)
        lng = float(lng)

    except (TypeError, ValueError):
        return jsonify({
            "error": "'lat' and 'lng' must be numbers"
        }), 400

    if not (-90 <= lat <= 90):
        return jsonify({
            "error": f"Latitude out of range: {lat}"
        }), 400

    if not (-180 <= lng <= 180):
        return jsonify({
            "error": f"Longitude out of range: {lng}"
        }), 400

    # -----------------------------------------------------------------------
    # Fetch Earth Engine Data
    # -----------------------------------------------------------------------
    t0 = time.time()

    logger.info(
        "▶ /calculate lat=%.5f lng=%.5f",
        lat,
        lng
    )

    try:
        satellite_data = fetch_farm_data(lat, lng)

    except Exception as exc:
        logger.exception("Earth Engine fetch failed")

        return jsonify({
            "error": "Failed to retrieve satellite data",
            "detail": str(exc)
        }), 502

    # -----------------------------------------------------------------------
    # Calculate Score
    # -----------------------------------------------------------------------
    try:
        result = calculate_score(
            ndvi=satellite_data.get("ndvi"),
            ndmi=satellite_data.get("ndmi"),
            rainfall=satellite_data.get("rainfall"),
            temperature=satellite_data.get("temperature"),
            groundwater=satellite_data.get("groundwater"),
        )

    except Exception as exc:
        logger.exception("Scoring computation failed")

        return jsonify({
            "error": "Scoring computation failed",
            "detail": str(exc)
        }), 500

    elapsed = round(time.time() - t0, 2)

    logger.info(
        "✓ Score=%d Grade=%s elapsed=%.2fs",
        result["final_score"],
        result["grade"],
        elapsed
    )

    # -----------------------------------------------------------------------
    # Response
    # -----------------------------------------------------------------------
    return jsonify({
        "score": result["final_score"],
        "grade": result["grade"],
        "components": result["components"],
        "coordinates": {
            "lat": lat,
            "lng": lng
        },
        "elapsed_seconds": elapsed
    }), 200


# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(_):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(_):
    return jsonify({
        "error": "Method not allowed"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Internal server error",
        "detail": str(error)
    }), 500


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info(
        "Starting FarmScore API on %s:%d",
        HOST,
        PORT
    )

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )
```

