from flask import Flask, jsonify

app = Flask(__name__)

# Your list of policies
policies = [
    {
        "name": "What happens when an ad policy is violated",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60210/0-500"
    },
    {
        "name": "Legal, privacy, and personalization",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60212/0-500"
    },
    {
        "name": "Disallowed content",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60208/0-500"
    },
    {
        "name": "Relevance and quality",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60215/0-500"
    },
    {
        "name": "Restricted content",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60216/0-500"
    },
    {
        "name": "Product ads policies",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60214/0-500"
    },
    {
        "name": "Ad extensions policies",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60206/0-500"
    },
    {
        "name": "Microsoft Services Agreement",
        "url": "https://www.microsoft.com/en-us/servicesagreement?FromAdsEmail=1"
    },
    {
        "name": "Microsoft – Terms of Use",
        "url": "https://www.microsoft.com/en-us/legal/terms-of-use?FromAdsEmail=1"
    },
    {
        "name": "Pharmacy and healthcare",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60379/-1"
    },
    {
        "name": "Information integrity and misleading content",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60357/-1"
    },
    {
        "name": "Promotion of third-party products and services",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/60382/-1"
    },
    {
        "name": "Introduction to Microsoft Advertising Network policies",
        "url": "https://help.ads.microsoft.com/#apex/ads/en/52023/1"
    }
]

# ✅ Route for root path `/`
@app.route('/')
def get_policies():
    return jsonify({"policies": policies})

# ✅ Optional: health check
@app.route('/health')
def health():
    return "Policy API is running!", 200
