
# Policy API (Render-ready)

A tiny Flask API to fetch and summarize Microsoft Ads policy pages in real time.

## Local run
```bash
pip install -r requirements.txt
python app.py
# Then open: http://localhost:5000/api/fetch-policy?url=https://help.ads.microsoft.com/#apex/ads/en/60214/0-500
```

## Render deployment
- Create a new Web Service, connect this repo.
- Start command: `python app.py`
- Free plan is fine.
