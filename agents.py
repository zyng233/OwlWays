import boto3
import json
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class BedrockAgent:
    def __init__(self):
        try:
            # Setup AWS credentials from .env
            os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
            os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
            os.environ['AWS_SESSION_TOKEN'] = os.getenv('AWS_SESSION_TOKEN')
            
            self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
            self.model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
            self.available = True
            print("Bedrock agent initialized successfully")
        except Exception as e:
            print(f"Bedrock not available: {e}")
            self.available = False
    
    def generate_explanation(self, flight_data, price_stats, recommendation, user_context):
        """Generate natural language explanation using Bedrock"""
        if not self.available:
            return self._fallback_explanation(flight_data, price_stats, recommendation)
        
        prompt = f"""
        You are a travel pricing expert. Analyze this flight data and provide a clear, actionable explanation.

        Flight Search Context:
        - Route: {user_context.get('origin', 'N/A')} → {user_context.get('destination', 'N/A')}
        - Budget: ${user_context.get('budget', 'N/A')}
        - Departure: {user_context.get('date', 'N/A')}

        Current Analysis:
        - Cheapest flight: ${flight_data['flights'][0]['price'] if flight_data['flights'] else 'N/A'}
        - Price range (10th-90th percentile): ${price_stats['q10']}-${price_stats['q90']}
        - Recommendation: {recommendation['decision']}
        - Confidence: {recommendation['confidence']:.0%}

        Provide a 2-3 sentence explanation that:
        1. Explains the current price position
        2. Gives clear actionable advice
        3. Mentions any budget considerations

        Keep it conversational and helpful.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 200,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            return result['content'][0]['text'].strip()
            
        except ClientError as e:
            return self._fallback_explanation(flight_data, price_stats, recommendation)
    
    def _fallback_explanation(self, flight_data, price_stats, recommendation):
        """Fallback explanation when Bedrock is unavailable"""
        if not flight_data['flights']:
            return "No flights found for this route. Try different dates or nearby airports."
        
        cheapest = flight_data['flights'][0]['price']
        decision = recommendation['decision']
        
        explanations = {
            "BUY NOW": f"Great deal! At ${cheapest}, this is significantly below the typical range of ${price_stats['q10']}-${price_stats['q90']}. Book soon as prices this low don't last long.",
            "BUY": f"Good price at ${cheapest}. This is below the median price and within a reasonable range. Consider booking if it fits your budget.",
            "WAIT": f"Current price of ${cheapest} is above average. Historical data suggests waiting a few days or being flexible with dates could save you money.",
            "ALTERNATE": f"Price of ${cheapest} is quite high compared to typical range of ${price_stats['q10']}-${price_stats['q90']}. Consider different dates, nearby airports, or alternative routes."
        }
        
        return explanations.get(decision, "Unable to generate recommendation at this time.")

    def analyze_market_trends(self, price_history):
        """Analyze price trends and patterns"""
        if not self.available or not price_history:
            return "Price trend analysis unavailable."
        
        recent_trend = "stable"
        if len(price_history) >= 5:
            recent_avg = sum(price_history[-5:]) / 5
            older_avg = sum(price_history[-10:-5]) / 5 if len(price_history) >= 10 else recent_avg
            
            if recent_avg > older_avg * 1.1:
                recent_trend = "increasing"
            elif recent_avg < older_avg * 0.9:
                recent_trend = "decreasing"
        
        return f"Recent price trend: {recent_trend}"