# AI Travel Assistant 🛫

An intelligent Streamlit web app that helps travelers make smart flight booking decisions using AI-powered price analysis and recommendations.

## Features

- **Smart Price Predictions**: Analyzes historical data to predict if you should BUY, WAIT, or try ALTERNATE options
- **AI-Powered Explanations**: Uses Amazon Bedrock (Claude 3.5 Sonnet) for natural language insights
- **Price Range Analysis**: Shows 10th-90th percentile price windows to identify deals
- **Interactive Charts**: Visualize price trends and comparisons
- **Mock Flight Data**: Ready-to-use dataset (easily replaceable with real APIs)
- **One-Click Booking**: Direct links to flight booking sites

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS (Optional)**
   ```bash
   # For Bedrock AI features
   aws configure
   # OR set environment variables:
   # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION
   ```

3. **Run the App**
   ```bash
   streamlit run app.py
   ```

4. **Open Browser**
   Navigate to `http://localhost:8501`

## Usage

1. Enter flight details in the sidebar:
   - **Origin/Destination**: Use IATA codes (e.g., JFK, LAX)
   - **Departure Date**: Pick your travel date
   - **Budget**: Set your price limit
   - **Flexibility**: Date flexibility for better deals

2. Click "Search Flights" to get:
   - AI recommendation (BUY/WAIT/ALTERNATE)
   - Top 5 cheapest flights
   - Price analysis and trends
   - Natural language explanation

## Sample Routes

Try these routes with mock data:
- **JFK → LAX** (New York to Los Angeles)
- **LAX → JFK** (Los Angeles to New York)

## Architecture

```
app.py          # Main Streamlit UI and logic
agents.py       # Amazon Bedrock integration
tools.py        # Flight data and analysis functions
mock_data.json  # Sample flight dataset
```

## AI Reasoning Flow

1. **Plan**: Analyze user requirements and market data
2. **Tool Calls**: Fetch flights, predict prices, analyze trends
3. **Reflect**: Compare current prices to historical ranges
4. **Explain**: Generate natural language insights via Bedrock
5. **Recommend**: Provide actionable BUY/WAIT/ALTERNATE advice

## Price Analysis Logic

- **BUY NOW**: Current price ≤ 10th percentile (excellent deal)
- **BUY**: Price ≤ median and within budget (good deal)
- **WAIT**: Price > median (likely to drop)
- **ALTERNATE**: Price ≥ 90th percentile (try different dates/airports)

## Extending to Real APIs

Replace mock data in `tools.py` with:
- **Amadeus API**: Real-time flight prices
- **Skyscanner API**: Price predictions
- **Google Flights**: Historical data

## Requirements

- Python 3.8+
- Streamlit 1.29+
- AWS Account (optional, for Bedrock AI features)
- Internet connection

## Troubleshooting

**Bedrock Not Available**: App works with fallback explanations if AWS/Bedrock isn't configured.

**No Flights Found**: Currently supports JFK-LAX routes. Add more routes in `mock_data.json`.

**Installation Issues**: Ensure Python 3.8+ and try `pip install --upgrade pip` first.

---

Built for hackathons and rapid prototyping. Ready to scale with real flight APIs! ✈️