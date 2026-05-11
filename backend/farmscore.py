def calculate_farm_score(gw, ndvi, ndmi, rainfall, temp):

    rainfall_score = (
        100 - 100 * abs(50 - rainfall) / 50
    )

    temperature_score = (
        100 - 100 * abs(40 - temp) / 40
    )

    weighted_avg = (
        10 * gw +
        30 * ndvi +
        25 * ndmi +
        10 * rainfall_score +
        25 * temperature_score
    ) / 100

    final_score = round(weighted_avg) + 150

    return {
        "rainfall_score": round(rainfall_score, 2),
        "temperature_score": round(temperature_score, 2),
        "final_score": final_score
    }
