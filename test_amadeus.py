#!/usr/bin/env python3
"""
Test script for Amadeus API integration
Run this to verify your API credentials work
"""

import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError
from datetime import datetime, timedelta

load_dotenv()

def test_amadeus_connection():
    """Test Amadeus API connection and basic flight search"""
    
    # Check if credentials are set
    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Amadeus credentials not found in .env file")
        print("Please add your AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET to .env")
        return False
    
    if client_id == "your_amadeus_client_id_here":
        print("❌ Please replace placeholder credentials in .env with real Amadeus API keys")
        return False
    
    try:
        # Initialize client
        amadeus = Client(client_id=client_id, client_secret=client_secret)
        print("✅ Amadeus client initialized")
        
        # Test flight search
        tomorrow = datetime.now() + timedelta(days=1)
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode='SIN',
            destinationLocationCode='JFK',
            departureDate=tomorrow.strftime('%Y-%m-%d'),
            adults=1,
            max=5
        )
        
        print(f"✅ API call successful! Found {len(response.data)} flight offers")
        
        # Display first flight
        if response.data:
            offer = response.data[0]
            price = offer['price']['total']
            currency = offer['price']['currency']
            print(f"Sample flight: {currency} {price}")
            
        return True
        
    except ResponseError as error:
        print(f"❌ Amadeus API error: {error}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Amadeus API integration...")
    success = test_amadeus_connection()
    
    if success:
        print("\n🎉 Amadeus API is working! Your app will now fetch real-time flight data.")
    else:
        print("\n⚠️  Amadeus API test failed. App will use mock data.")
        print("\nTo fix this:")
        print("1. Sign up at https://developers.amadeus.com/")
        print("2. Create a new app to get API keys")
        print("3. Add your keys to the .env file")