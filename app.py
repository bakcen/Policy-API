import os
from flask import Flask, request, jsonify
from datetime import datetime
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def render_and_extract(url: str) -> dict:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox"])
        page = browser.new_page()
        page.goto(url, wait_until="networkidle", timeout=45000)

        # Try to wait for a plausible content container (don’t fail if not found)
        for sel in ["article", "main", "#mainContent", ".content"]:
            try:
                page.wait_for_selector(sel, timeout=3000)
                break
            except:
                pass

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string.strip() if soup.title and soup.title.string else None)

    # Prefer real page body; fall back to all text if needed
    candidates = soup.select("article, main, #mainContent, .content")
    if not candidates:
        candidates = [soup]

    paras = []
    for node in candidates:
        for p in node.find_all("p"):
            t = p.get_text(" ", strip=True)
            if t:
                paras.append(t)

    summary = " ".join(paras)
    if not summary:
        summary = soup.get_text(" ", strip=True)

    return {
        "title": title,
        "summary": (summary[:5000] + "...") if len(summary) > 5000 else summary
    }

@app.route("/api/fetch-policy", methods=["GET"])
def fetch_policy():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    try:
        data = render_and_extract(url)
        return jsonify({
            "url": url,
            "title": data.get("title"),
            "summary": data.get("summary"),
            "last_updated": datetime.utcnow().isoformat() + "Z"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Optional: batch endpoint to fetch many at once
@app.route("/api/fetch-policies", methods=["POST"])
def fetch_policies():
    payload = request.get_json(silent=True) or {}
    urls = payload.get("urls", [])
    out = []
    for u in urls[:12]:  # safety cap
        try:
            data = render_and_extract(u)
            out.append({
                "url": u,
                "title": data.get("title"),
                "summary": data.get("summary"),
                "last_updated": datetime.utcnow().isoformat() + "Z"
            })
        except Exception as e:
            out.append({"url": u, "error": str(e)})
    return jsonify({"results": out})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
