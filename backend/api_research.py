"""
Sports API Research - Free and Paid Options

FREE APIs (Good for development):
1. ESPN API - Unofficial but widely used
2. Football-Data.org - 10 requests/minute free tier
3. SportsData.io - Free tier available
4. API-Football (RapidAPI) - Limited free requests

PREMIUM APIs (For production):
1. SportRadar - Professional grade, expensive
2. The Odds API - Betting odds focus
3. Sportsbook APIs - Direct integration

For MVP: We'll start with free APIs for development
"""

import requests
import json
from datetime import datetime

def test_espn_api():
    """Test ESPN's unofficial API"""
    try:
        # Premier League fixtures
        url = "https://site-web-api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"ESPN API: Found {len(events)} Premier League games")

            # Show first game details
            if events:
                game = events[0]
                home_team = game['competitions'][0]['competitors'][0]['team']['displayName']
                away_team = game['competitions'][0]['competitors'][1]['team']['displayName']
                date = game['date']
                print(f"Sample game: {home_team} vs {away_team} on {date}")

            return True
        else:
            print(f"ESPN API failed: {response.status_code}")
            return False

    except Exception as e:
        print(f"ESPN API error: {e}")
        return False

def test_football_data_api():
    """Test Football-Data.org API"""
    try:
        # Note: Requires free API key registration
        url = "https://api.football-data.org/v4/competitions/PL/matches"
        headers = {
            'X-Auth-Token': 'YOUR_API_KEY_HERE'  # Need to register
        }

        print("Football-Data.org requires free API key registration")
        print("Visit: https://www.football-data.org/client/register")
        return False

    except Exception as e:
        print(f"Football-Data API error: {e}")
        return False

if __name__ == "__main__":
    print("Testing sports data APIs...")
    print("-" * 40)

    # Test APIs
    espn_works = test_espn_api()
    football_data_works = test_football_data_api()

    print("-" * 40)
    print("API Test Results:")
    print(f"ESPN API: {'✅ Working' if espn_works else '❌ Failed'}")
    print(f"Football-Data.org: {'✅ Working' if football_data_works else '❌ Needs API Key'}")

    print("\nRecommendation: Start with ESPN API for development")
