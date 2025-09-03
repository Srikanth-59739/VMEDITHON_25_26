# Insulin Injection Tracking & Prediction (Essential Code)


> **Disclaimer**: This software is for research and educational purposes only and is **not** a medical device. Do not use it to make clinical decisions.


## Quickstart

```bash
# 1) set up env
python -m venv .venv && source .venv/bin/activate # on Windows: .venv\Scripts\activate
pip install -r requirements.txt


# 2) configure
cp .env.example .env # edit paths if needed


# 3) prepare a CSV (see `features.load_csv` docstring for required columns)
# drop your file into data/raw/doses.csv


# 4) train baseline model (RandomForest next-glucose prediction)
python train_baseline.py --csv data/raw/doses.csv --horizon-min 60


# 5) run API
uvicorn api.main:app --reload


# 6) run Streamlit dashboard
streamlit run dashboard/streamlit_app.py
