
import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/api/fetch-policy", methods=["GET"])
def fetch_policy():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Title + paragraph text
        title = soup.title.string if soup.title else "No title found"
        paragraphs = " ".join(p.get_text(" ", strip=True) for p in soup.find_all("p"))
        text = paragraphs if paragraphs else soup.get_text(" ", strip=True)

        # Trim large pages
        summary = text[:2000] + "..." if len(text) > 2000 else text

        return jsonify({
            "url": url,
            "title": title,
            "summary": summary,
            "last_updated": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
