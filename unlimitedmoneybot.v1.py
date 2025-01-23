import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ForexRate API Config
API_KEY = "bef4eed23eac385f7b676439a819b110"
API_URL = "https://api.forexrateapi.com/v1/latest"

def fetch_forex_rate(base_currency, target_currencies):
    try:
        # Build the request URL
        url = f"{API_URL}?api_key={API_KEY}&base={base_currency}&currencies={','.join(target_currencies)}"
        response = requests.get(url)
        data = response.json()
        
        # Check for errors
        if "rates" in data:
            return {"base_currency": base_currency, "rates": data["rates"]}
        else:
            return {"error": data.get("error", "Unknown error")}
    except Exception as e:
        return {"error": f"Failed to fetch rate: {str(e)}"}

@app.route('/forex_rate', methods=['POST'])
def forex_rate():
    # Get JSON data from the POST request
    request_data = request.get_json()
    base_currency = request_data.get("base_currency", "USD")
    target_currencies = request_data.get("target_currencies", ["EUR", "INR", "JPY"])
    
    # Fetch the forex rates
    result = fetch_forex_rate(base_currency, target_currencies)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
