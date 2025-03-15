import os
import requests
import json

# Configuration
symbol = "AAPL"
base_folder = "Financial Position"
os.makedirs(base_folder, exist_ok=True)
output_json_path = os.path.join(base_folder, f"{symbol}_comparable_analysis.json")

fmp_api_key = ""
openai_api_key = ""

def fetch_fmp_financials(ticker):
    financials = {}

    income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=1&apikey={fmp_api_key}"
    financials['income_statement'] = requests.get(income_url).json()[0]

    balance_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=1&apikey={fmp_api_key}"
    financials['balance_sheet'] = requests.get(balance_url).json()[0]

    profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={fmp_api_key}"
    profile_response = requests.get(profile_url).json()
    financials['overview'] = profile_response[0] if profile_response else {}

    return financials

def get_value_safe(data, key):
    value = data.get(key, 0)
    try:
        if isinstance(value, str):
            return float(value.replace(',', '').replace('$', '').strip())
        return float(value)
    except:
        return 0

def calculate_financial_metrics(financials):
    income = financials['income_statement']
    balance = financials['balance_sheet']
    overview = financials['overview']

    price = get_value_safe(overview, "price")
    market_cap = get_value_safe(overview, "mktCap")

    total_debt = get_value_safe(balance, "shortTermDebt") + get_value_safe(balance, "longTermDebt")
    cash_and_equivalents = get_value_safe(balance, "cashAndCashEquivalents")

    ev = market_cap + total_debt - cash_and_equivalents
    sales = get_value_safe(income, "revenue")
    ebitda = get_value_safe(income, "ebitda")
    ebit = get_value_safe(income, "operatingIncome")
    earnings = get_value_safe(income, "netIncome")

    return {
        "Price ($/share)": price,
        "Market Cap ($M)": market_cap / 1_000_000,
        "Enterprise Value ($M)": ev / 1_000_000,
        "Sales ($M)": sales / 1_000_000,
        "EBITDA ($M)": ebitda / 1_000_000,
        "EBIT ($M)": ebit / 1_000_000,
        "Earnings ($M)": earnings / 1_000_000
    }

def fetch_peers_from_openai(target_company, market_cap_usd):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    min_cap = market_cap_usd * 0.5
    max_cap = market_cap_usd * 1.5

    prompt = (
        f"List 5-7 publicly traded companies that are direct competitors to {target_company}. "
        f"Only include companies in the same industry as {target_company}. "
        f"Only include companies with a market capitalization between ${min_cap:,.0f} and ${max_cap:,.0f} USD. "
        f"Return only the tickers in a JSON array like this: [\"NIO\", \"RIVN\", \"LCID\", \"GM\", \"F\"]. "
        f"No explanations, no backticks, no markdown. Only the array."
    )

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=payload)
    response_json = response.json()

    try:
        content = response_json['choices'][0]['message']['content']

        # Clean and force double quotes to match JSON expectations
        cleaned_content = content.strip().replace("'", '"')

        peers = json.loads(cleaned_content)

        if not isinstance(peers, list):
            raise ValueError("Response was not a list")

        return peers
    except Exception as e:
        raise Exception(f"❌ Failed to fetch peers from OpenAI: {e}\nResponse: {response_json}")

# === Step 1: Fetch Target Financials ===
target_financials = fetch_fmp_financials(symbol)

sector = target_financials['overview'].get("sector", "Unknown")
industry = target_financials['overview'].get("industry", "Unknown")
target_market_cap = target_financials['overview'].get("mktCap", 0)

target_metrics = calculate_financial_metrics(target_financials)

print(f"✅ {symbol} Sector: {sector}, Industry: {industry}, Market Cap: {target_market_cap:,.0f}")

# === Step 2: Fetch Peers from OpenAI (Market Cap Aware) ===
peers = fetch_peers_from_openai(symbol, target_market_cap)
print(f"✅ Peers fetched from OpenAI for {symbol}: {peers}")

# === Step 3: Fetch & Calculate Financial Metrics for Each Peer ===
peer_data = {}

for peer in peers:
    peer_financials = fetch_fmp_financials(peer)
    peer_metrics = calculate_financial_metrics(peer_financials)

    peer_data[peer] = {
        "financial_metrics": peer_metrics,
        "overview": peer_financials['overview'],
        "financials": peer_financials
    }

# === Step 4: Save Final Comparable Analysis ===
comparable_analysis = {
    "target": {
        "ticker": symbol,
        "industry": industry,
        "sector": sector,
        "market_cap": target_market_cap,
        "financial_metrics": target_metrics,
        "overview": target_financials['overview'],
        "financials": target_financials
    },
    "peers": peer_data
}

with open(output_json_path, "w") as f:
    json.dump(comparable_analysis, f, indent=4)

print(f"\n✅ Comparable Analysis saved to: {output_json_path}")
