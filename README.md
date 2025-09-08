# OwlWays AI Travel Assistant 🦉

An intelligent Streamlit web app that helps travelers make smart flight booking decisions using AI-powered price analysis and recommendations.

Link to repo: https://github.com/zyng233/OwlWays

## Features

- **Real-time Flight Data**: Powered by Amadeus API with 50+ international airports
- **Smart Price Predictions**: Analyzes historical data to predict if you should BUY, WAIT, or try ALTERNATE options
- - **Date Flexibility**: Search multiple days to find cheapest options
- **AI-Powered Explanations**: Uses Amazon Bedrock (Claude 3.5 Sonnet) for natural language insights
- **Price Range Analysis**: Historical trends, percentiles, and future predictions
- **Interactive Charts**: Visualize price trends and comparisons
- **One-Click Booking**: Direct links to flight booking sites

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS (For Bedrock AI features)**
   aws configure
   - Add to `.env` file:
   ```bash
   AWS_ACCESS_KEY_ID=your_access_key_id_here
   AWS_SECRET_ACCESS_KEY=your_secret_access_key_here
   AWS_DEFAULT_REGION-youe_default_region_here
   ```

3. **Configure Amadeus API (Recommended)**
   - Sign up at https://developers.amadeus.com/
   - Create an app to get API credentials
   - Add to `.env` file:
   ```
   AMADEUS_CLIENT_ID=your_client_id_here
   AMADEUS_CLIENT_SECRET=your_client_secret_here
   ```
   
4. **Run the App**
   ```bash
   streamlit run app.py
   ```

5. **Open Browser**
   Navigate to `http://localhost:8501`

## Usage

1. **Select Flight Details**:
   - **From/To**: Choose from 50+ international airports
   - **Departure Date**: Select your travel date
   - **Return Date**: Optional for round-trip (leave empty for one-way)
   - **Budget**: Set price limit in SGD (S$100-S$5000)
   - **Date Flexibility**: Search +0 to +7 days for better deals

2. **Get AI-Powered Results**:
   - Smart recommendation (BUY NOW/BUY/WAIT/ALTERNATE)
   - Top cheapest flights with airline names
   - Price analysis vs historical data
   - Future price predictions
   - Direct booking links

## Supported Routes

**Real-time data available for 1000+ routes including**:
- **SIN ↔ BKK** (Singapore ↔ Bangkok)
- **SIN ↔ JFK** (Singapore ↔ New York)
- **JFK ↔ LAX** (New York ↔ Los Angeles)
- **LHR ↔ SIN** (London ↔ Singapore)
- And many more international connections

## Architecture

```
app.py                 # Main Streamlit UI and logic
real_data_service.py   # Amadeus API integration & data processing
tools.py              # Flight search and analysis functions
agents.py             # Amazon Bedrock AI integration
mock_data.json        # Fallback flight dataset
test_amadeus.py       # API connection testing
.env                  # API credentials (create this)
```

## AI Decision Process

1. **Data Collection**: Fetch real-time flights via Amadeus API
2. **Flexibility Search**: Query multiple dates for best deals
3. **Price Analysis**: Compare against 30-day historical data
4. **ML Predictions**: Forecast future price trends
5. **Smart Recommendations**: Generate BUY/WAIT/ALTERNATE with confidence
6. **Natural Language**: AI explanations via Amazon Bedrock


## Smart Recommendation Logic

- **BUY NOW** 🟢: Price ≤ 10th percentile (excellent deal, act fast)
- **BUY** 🟡: Price ≤ median and within budget (good deal)
- **WAIT** 🟠: Price > median (likely to drop, be patient)
- **ALTERNATE** 🔴: Price ≥ 90th percentile (try flexible dates/airports)

## Data Sources

**Real-time Mode** (when API configured):
- **Amadeus API**: Live flight prices and schedules
- **AWS DynamoDB**: Historical price storage
- **Amazon Bedrock**: AI-powered explanations

**Fallback Mode** (when APIs unavailable):
- Enhanced mock data with realistic pricing
- 50+ airline code mappings
- Market-based price variations

## Requirements

- Python 3.8+
- Streamlit 1.29+
- Amadeus API account (recommended for real-time data)
- AWS Account (optional, for AI features and price history)
- Internet connection

## Key Features Explained

### 🔄 **Date Flexibility**
Search departure date + up to 7 additional days to find cheaper flights. Perfect for flexible travelers.

### 📊 **Price Intelligence**
- Historical price analysis (30-day trends)
- Future price predictions using ML
- Percentile-based deal identification
- Budget-aware recommendations

### ✈️ **Flight Options**
- One-way and round-trip support
- Real-time pricing from Amadeus
- Direct booking links to Google Flights
- Alternative date suggestions

## Troubleshooting

**"Invalid Amadeus credentials"**: Update `.env` with real API keys from developers.amadeus.com

**"No flights found"**: App supports 1000+ routes. Try popular international connections.

**"Using mock data"**: Real-time features require Amadeus API setup. App works with realistic fallback data.

**Installation Issues**: Ensure Python 3.8+ and run `pip install --upgrade pip` first.

---

🚀 **Ready for Production**: Real-time flight data, AI recommendations, and scalable architecture!
