import json
import numpy as np
from datetime import datetime, timedelta
import random
from real_data_service import RealFlightDataService

# Initialize real data service
try:
    real_data_service = RealFlightDataService()
    USE_REAL_DATA = True
except Exception as e:
    print(f"Real data service unavailable: {e}")
    USE_REAL_DATA = False
    real_data_service = None

def load_mock_data():
    """Load mock flight data from JSON file"""
    with open('mock_data.json', 'r') as f:
        return json.load(f)

def fetch_flights(origin, destination, departure_date, return_date=None):
    """Fetch flights for given route and dates"""
    if USE_REAL_DATA and real_data_service:
        try:
            # Include return_date if needed
            result = real_data_service.fetch_live_flights(origin, destination, departure_date)
            
            # If you want round-trip, you can also fetch return flights
            if return_date:
                return_result = real_data_service.fetch_live_flights(destination, origin, return_date)
                # Combine or store separately
                result["return_flights"] = return_result.get("flights", [])
            
            if result and result.get('flights'):
                prices = [f['price'] for f in result['flights']]
                real_data_service.store_price_history(f"{origin}-{destination}", prices)
                return result
        except Exception as e:
            print(f"Real data fetch failed: {e}")
    
    # Fallback to mock data
    data = load_mock_data()
    route_key = f"{origin}-{destination}"
    return_key = f"{destination}-{origin}" if return_date else None
    
    flights = []
    if route_key in data:
        flights = data[route_key]["flights"].copy()
        date_factor = random.uniform(0.85, 1.15)
        for flight in flights:
            flight["price"] = int(flight["price"] * date_factor)
    
    result = {"flights": sorted(flights, key=lambda x: x["price"])[:8]}
    
    # Add mock return flights if return_date exists
    if return_date and return_key in data:
        return_flights = data[return_key]["flights"].copy()
        date_factor = random.uniform(0.85, 1.15)
        for flight in return_flights:
            flight["price"] = int(flight["price"] * date_factor)
        result["return_flights"] = sorted(return_flights, key=lambda x: x["price"])[:8]
    
    return result

def predict_price_range(price_history, current_price=None):
    """Predict price range using historical data"""
    if not price_history:
        return {"q10": 200, "q50": 250, "q90": 300}
    
    prices = np.array(price_history)
    q10 = np.percentile(prices, 10)
    q50 = np.percentile(prices, 50)
    q90 = np.percentile(prices, 90)
    
    return {
        "q10": int(q10),
        "q50": int(q50), 
        "q90": int(q90),
        "mean": int(np.mean(prices)),
        "std": int(np.std(prices))
    }

def decide_recommendation(current_price, price_stats, user_budget):
    """Make buy/wait/alternate recommendation"""
    q10, q50, q90 = price_stats["q10"], price_stats["q50"], price_stats["q90"]
    
    # Price position analysis
    if current_price <= q10:
        decision = "BUY NOW"
        confidence = 0.9
        reason = f"Excellent deal! Current price ${current_price} is in bottom 10% of historical prices."
    elif current_price <= q50:
        decision = "BUY" if current_price <= user_budget else "WAIT"
        confidence = 0.7
        reason = f"Good price at ${current_price}, below median of ${q50}."
    elif current_price <= q90:
        decision = "WAIT"
        confidence = 0.6
        reason = f"Price ${current_price} is above median. Consider waiting or flexible dates."
    else:
        decision = "ALTERNATE"
        confidence = 0.8
        reason = f"Price ${current_price} is in top 10%. Try different dates or nearby airports."
    
    # Budget consideration
    if current_price > user_budget * 1.2:
        decision = "ALTERNATE"
        reason += f" Significantly over budget of ${user_budget}."
    
    return {
        "decision": decision,
        "confidence": confidence,
        "reason": reason,
        "price_position": "bottom 10%" if current_price <= q10 else 
                         "below median" if current_price <= q50 else
                         "above median" if current_price <= q90 else "top 10%"
    }

def get_price_history(origin, destination):
    """Get historical price data for route"""
    route_key = f"{origin}-{destination}"
    
    if USE_REAL_DATA and real_data_service:
        try:
            return real_data_service.get_historical_prices(route_key)
        except Exception as e:
            print(f"Real price history failed: {e}")
    
    # Fallback to mock data
    data = load_mock_data()
    if route_key in data:
        return data[route_key]["price_history"]
    return []

def get_future_predictions(origin, destination):
    """Get ML-based future price predictions"""
    if USE_REAL_DATA and real_data_service:
        try:
            route_key = f"{origin}-{destination}"
            historical_prices = real_data_service.get_historical_prices(route_key)
            return real_data_service.predict_future_prices(historical_prices)
        except Exception as e:
            print(f"Price prediction failed: {e}")
    
    return {"trend": "stable", "confidence": 0.5}

def get_market_alerts(routes, budget):
    """Get real-time market alerts for price drops"""
    if USE_REAL_DATA and real_data_service:
        try:
            return real_data_service.get_market_alerts(routes, budget)
        except Exception as e:
            print(f"Market alerts failed: {e}")
    
    return []

def get_booking_insights(origin, destination):
    """Get optimal booking timing insights"""
    if USE_REAL_DATA and real_data_service:
        try:
            route_key = f"{origin}-{destination}"
            return real_data_service.analyze_booking_patterns(route_key)
        except Exception as e:
            print(f"Booking insights failed: {e}")
    
    return {"best_day": "Tuesday", "best_time": "3PM", "confidence": 0.5}