# AI for Smart Waste Management

A Streamlit dashboard that summarizes waste collection records by area and waste type.

## Features
- Summary metrics for total and recorded recycled waste
- Interactive filters for area and waste category
- Charts by waste type and area
- Upload a CSV file and download filtered records
- Basic waste sorting guidance

## Tech stack
- Python 3.10+
- Streamlit
- Pandas

## Run locally
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens in your browser. Use `sample_waste_data.csv` as a sample upload.

## Project scope
This is a data-analysis prototype using sample or uploaded CSV data. It does not currently connect to physical sensors, predict bin fullness, or train a machine-learning model. The name describes the project theme; do not claim a trained AI model unless one is added and evaluated.
