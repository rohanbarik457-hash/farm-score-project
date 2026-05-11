# 🌾 Farm Score Project

A web application to evaluate and score farms based on various agricultural and sustainability metrics.

## Project Structure

```
farm-score-project/
│
├── frontend/
│   ├── index.html       # Main HTML page
│   ├── style.css        # Styling
│   └── app.js           # Frontend logic & API calls
│
├── backend/
│   ├── app.py           # Flask API server
│   ├── farmscore.py     # Core scoring logic
│   └── requirements.txt # Python dependencies
│
└── README.md
```

## Features

- Submit farm data through a clean web interface
- Calculate farm scores based on multiple criteria
- View detailed scoring breakdown
- REST API for programmatic access

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will start at `http://localhost:5000`.

### Frontend Setup

Open `frontend/index.html` in your browser, or serve it with any static file server:

```bash
# Using Python
cd frontend
python -m http.server 8080
```

Then visit `http://localhost:8080`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/score` | Submit farm data and get a score |
| `GET` | `/score/<id>` | Retrieve a previously calculated score |

### Example Request

```bash
curl -X POST http://localhost:5000/score \
  -H "Content-Type: application/json" \
  -d '{
    "farm_name": "Green Valley Farm",
    "area_hectares": 50,
    "crop_type": "wheat",
    "irrigation_type": "drip",
    "soil_health": 8,
    "water_usage_efficiency": 7,
    "biodiversity_score": 6
  }'
```

### Example Response

```json
{
  "farm_name": "Green Valley Farm",
  "total_score": 78.5,
  "grade": "B+",
  "breakdown": {
    "soil_health": 24.0,
    "water_efficiency": 21.0,
    "biodiversity": 18.0,
    "practices": 15.5
  },
  "recommendations": [
    "Consider increasing crop rotation diversity",
    "Explore cover cropping to boost soil organic matter"
  ]
}
```

## Scoring Criteria

| Criterion | Weight | Max Points |
|-----------|--------|------------|
| Soil Health | 30% | 30 |
| Water Efficiency | 25% | 25 |
| Biodiversity | 20% | 20 |
| Sustainable Practices | 25% | 25 |

**Total: 100 points**

### Grade Scale

| Score | Grade |
|-------|-------|
| 90–100 | A |
| 80–89 | B |
| 70–79 | C |
| 60–69 | D |
| < 60 | F |

## Tech Stack

- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Backend**: Python, Flask
- **Data**: JSON (extendable to SQLite/PostgreSQL)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

MIT License — feel free to use and adapt this project.
