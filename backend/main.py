from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
from datetime import datetime
from typing import Optional, Dict, Any, List
from ai_prediction_engine import AIPredictionEngine

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Sports Betting API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://127.0.0.1:3000", "http://127.0.0.1:3001", "http://127.0.0.1:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class GameInfo(BaseModel):
    home_team: str
    away_team: str
    date: str

class PredictionFactors(BaseModel):
    team_strength: float
    recent_form: float
    head_to_head: float
    home_advantage: float

class Prediction(BaseModel):
    id: int
    game: GameInfo
    prediction_type: str
    confidence: float
    reasoning: str
    factors: Optional[PredictionFactors] = None

class PredictionsResponse(BaseModel):
    predictions: List[Prediction]
    count: int

# API configuration
ODDS_API_KEY = "e45c16d3a604ed4263b6432b9a13a850"
ODDS_API_URL = "https://api.the-odds-api.com/v4"
SOCCER_API_DATA_KEY = "76d413355f4feb43389a6ed6c489fd4be4d83b0b"

class SoccerAPIDataService:
    """Service for SoccerDataAPI.com"""

    def __init__(self):
        self.base_url = "https://api.soccerdataapi.com"
        self.api_key = SOCCER_API_DATA_KEY
        self.headers = {
            "Accept-Encoding": "gzip",
            "Accept": "application/json"
        }

    async def test_connection(self) -> Dict[str, Any]:
        """Test connection with SoccerDataAPI"""
        url = f"{self.base_url}/country/?auth_token={self.api_key}"

        try:
            print(f"🔍 Testing SoccerDataAPI: {url}")
            print(f"🔑 API Key: {self.api_key[:10]}...")

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, headers=self.headers)

                print(f"📊 Status: {response.status_code}")
                print(f"📊 Response headers: {dict(response.headers)}")

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "status_code": response.status_code,
                        "data_type": type(data).__name__,
                        "countries_count": len(data) if isinstance(data, list) else "N/A",
                        "response_preview": str(data)[:300] if data else "Empty response"
                    }
                elif response.status_code == 401:
                    return {
                        "success": False,
                        "error": "Authentication failed - check API key",
                        "status_code": 401
                    }
                elif response.status_code == 403:
                    return {
                        "success": False,
                        "error": "Access forbidden - check API permissions",
                        "status_code": 403
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "response_text": response.text[:300]
                    }

        except httpx.ConnectError as e:
            return {
                "success": False,
                "error": f"Connection failed: {str(e)}",
                "check": "Verify api.soccerdataapi.com is accessible"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }

    async def get_premier_league_standings(self) -> Dict[str, Any]:
        """Get Premier League standings"""
        url = f"{self.base_url}/standing/?league_id=228&auth_token={self.api_key}"

        try:
            print(f"🏆 Fetching Premier League standings: {url}")

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, headers=self.headers)

                print(f"📊 Standings status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "league_id": 228,
                        "data": data
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "response": response.text[:300]
                    }

        except Exception as e:
            return {
                "success": False,
                "error": f"Standings request failed: {str(e)}"
            }

    async def get_head_to_head_by_names(self, home_team: str, away_team: str) -> Dict[str, Any]:
        """Get head-to-head using team names (converts to IDs automatically)"""
        team_mapping = {
            "arsenal": 3068,
            "liverpool": 4138,
            "tottenham": 2909,
            "tottenham hotspur": 2909,
            "spurs": 2909,
            "chelsea": 2916,
            "manchester city": 4136,
            "man city": 4136,
            "city": 4136,
            "manchester united": 4137,
            "man united": 4137,
            "man utd": 4137,
            "united": 4137,
            "nottingham forest": 4149,
            "forest": 4149,
            "everton": 4139,
            "bournemouth": 3072,
            "afc bournemouth": 3072,
            "burnley": 3104,
            "brentford": 4148,
            "leeds united": 4147,
            "leeds": 4147,
            "fulham": 4145,
            "crystal palace": 4140,
            "palace": 4140,
            "newcastle united": 3071,
            "newcastle": 3071,
            "aston villa": 2912,
            "villa": 2912,
            "brighton": 3200,
            "brighton & hove albion": 3200,
            "wolves": 3074,
            "wolverhampton wanderers": 3074,
            "west ham": 3059,
            "west ham united": 3059,
            "sunderland": 3073
        }

        home_team_clean = home_team.replace("_", " ").lower().strip()
        away_team_clean = away_team.replace("_", " ").lower().strip()

        home_id = team_mapping.get(home_team_clean)
        away_id = team_mapping.get(away_team_clean)

        if not home_id or not away_id:
            return {
                "error": f"Team not found. Home: '{home_team}' -> '{home_team_clean}' ({home_id}), Away: '{away_team}' -> '{away_team_clean}' ({away_id})",
                "available_teams": sorted(list(team_mapping.keys())),
                "tip": "Use spaces instead of underscores in team names"
            }

        url = f"{self.base_url}/head-to-head/?team_1_id={home_id}&team_2_id={away_id}&auth_token={self.api_key}"

        try:
            print(f"🔥 Getting H2H: {home_team_clean} (ID: {home_id}) vs {away_team_clean} (ID: {away_id})")

            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(url, headers=self.headers)

                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "home_team": {"name": home_team, "id": home_id},
                        "away_team": {"name": away_team, "id": away_id},
                        "head_to_head_data": data
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}",
                        "response": response.text[:300]
                    }

        except Exception as e:
            return {
                "success": False,
                "error": f"H2H request failed: {str(e)}"
            }

    async def get_head_to_head(self, home_team: str, away_team: str) -> Dict[str, Any]:
        """Get head-to-head record between two teams"""
        return await self.get_head_to_head_by_names(home_team, away_team)

    async def get_team_statistics(self, team_name: str) -> Dict[str, Any]:
        """Placeholder - need team_id mapping"""
        return {"message": f"Need team_id for {team_name} - will implement after connection works"}

    async def get_team_form(self, team_name: str) -> Dict[str, Any]:
        """Placeholder - need team_id mapping"""
        return {"message": f"Need team_id for {team_name} - will implement after connection works"}


# Initialize SoccerAPIData service
soccer_api_service = SoccerAPIDataService()
prediction_engine = AIPredictionEngine(soccer_api_service)

@app.get("/")
async def root():
    return {"message": "AI Sports Betting API with SoccerAPIData + Odds API"}

@app.get("/api/predictions", response_model=PredictionsResponse)
async def get_predictions():
    """Get today's predictions"""
    mock_predictions = [
        Prediction(
            id=1,
            game=GameInfo(
                home_team="Arsenal",
                away_team="Liverpool",
                date=(datetime.now() + timedelta(hours=2)).isoformat()
            ),
            prediction_type="home_win",
            confidence=78.5,
            reasoning="Strong home record and recent form",
            factors=PredictionFactors(
                team_strength=0.12,
                recent_form=0.08,
                head_to_head=0.03,
                home_advantage=0.15
            )
        )
    ]

    return PredictionsResponse(
        predictions=mock_predictions,
        count=len(mock_predictions)
    )

@app.get("/api/real-fixtures")
async def get_real_fixtures():
    """Proxy endpoint to fetch real fixtures from The Odds API"""
    url = f"{ODDS_API_URL}/sports/soccer_epl/odds?api_key={ODDS_API_KEY}&regions=uk&markets=h2h&oddsFormat=decimal"

    try:
        print(f"🏈 Backend: Fetching real fixtures from The Odds API...")

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            fixtures_data = response.json()
            print(f"✅ Backend: Got {len(fixtures_data)} fixtures from API")

            transformed_predictions = []

            for i, fixture in enumerate(fixtures_data):
                utc_time = datetime.fromisoformat(fixture['commence_time'].replace('Z', '+00:00'))
                copenhagen_time = utc_time + timedelta(hours=2)

                confidence = round(random.uniform(65, 95), 1)

                bookmaker = fixture.get('bookmakers', [])
                if bookmaker and len(bookmaker) > 0:
                    h2h_market = next((m for m in bookmaker[0].get('markets', []) if m['key'] == 'h2h'), None)
                    if h2h_market and len(h2h_market['outcomes']) >= 2:
                        home_odds = h2h_market['outcomes'][0]['price']
                        away_odds = h2h_market['outcomes'][1]['price']

                        if home_odds < away_odds:
                            prediction_type = "home_win"
                            reasoning = f"Home team favored by bookmakers (odds: {home_odds})"
                        elif away_odds < home_odds:
                            prediction_type = "away_win"
                            reasoning = f"Away team favored by bookmakers (odds: {away_odds})"
                        else:
                            prediction_type = "draw"
                            reasoning = "Evenly matched teams based on odds"
                    else:
                        prediction_type = "home_win"
                        reasoning = "Home advantage factor"
                else:
                    prediction_type = "home_win"
                    reasoning = "Home advantage factor"

                transformed_prediction = {
                    "id": i + 1,
                    "game": {
                        "home_team": fixture['home_team'],
                        "away_team": fixture['away_team'],
                        "date": fixture['commence_time']
                    },
                    "prediction_type": prediction_type,
                    "confidence": confidence,
                    "reasoning": reasoning,
                    "kickoff_datetime": fixture['commence_time'],
                    "kickoffTimeDisplay": copenhagen_time.strftime('%H:%M'),
                    "kickoffDateDisplay": copenhagen_time.strftime('%a, %d %b'),
                    "real_data": True,
                    "factors": {
                        "team_strength": round(random.uniform(-0.2, 0.2), 3),
                        "recent_form": round(random.uniform(-0.15, 0.15), 3),
                        "head_to_head": round(random.uniform(-0.1, 0.1), 3),
                        "home_advantage": round(random.uniform(0.05, 0.25), 3)
                    },
                    "odds": {
                        "home_win": bookmaker[0]['markets'][0]['outcomes'][0]['price'] if bookmaker and bookmaker[0].get('markets') else 2.0,
                        "away_win": bookmaker[0]['markets'][0]['outcomes'][1]['price'] if bookmaker and bookmaker[0].get('markets') and len(bookmaker[0]['markets'][0]['outcomes']) > 1 else 2.0,
                        "draw": bookmaker[0]['markets'][0]['outcomes'][2]['price'] if bookmaker and bookmaker[0].get('markets') and len(bookmaker[0]['markets'][0]['outcomes']) > 2 else 3.0
                    }
                }

                transformed_predictions.append(transformed_prediction)

            return {
                "predictions": transformed_predictions,
                "count": len(transformed_predictions),
                "source": "real_api_data"
            }

    except httpx.HTTPStatusError as e:
        print(f"❌ Backend: HTTP error {e.response.status_code}")
        raise HTTPException(status_code=500, detail=f"Odds API returned {e.response.status_code}")
    except Exception as e:
        print(f"❌ Backend: Error fetching fixtures: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch fixtures: {str(e)}")


@app.get("/api/real-fixtures/usage")
async def get_api_usage():
    """Get The Odds API usage information"""
    url = f"{ODDS_API_URL}/sports?api_key={ODDS_API_KEY}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            remaining = int(response.headers.get('x-requests-remaining', '0'))
            used = int(response.headers.get('x-requests-used', '0'))

            return {
                "remaining": remaining,
                "used": used,
                "total": 500
            }
    except Exception as e:
        return {
            "remaining": 0,
            "used": 500,
            "total": 500,
            "error": str(e)
        }

# SoccerAPIData endpoints
@app.get("/api/football/test")
async def test_soccer_api_connection():
    """Test SoccerAPIData API connection"""
    try:
        result = await soccer_api_service.test_connection()
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/football/standings")
async def get_premier_league_standings():
    """Get current Premier League standings from SoccerAPIData"""
    try:
        print("🏆 SoccerAPIData: Fetching Premier League standings")
        standings = await soccer_api_service.get_premier_league_standings()
        return standings
    except Exception as e:
        print(f"❌ SoccerAPIData standings error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch standings: {str(e)}")

@app.get("/api/football/team-stats/{team_name}")
async def get_team_statistics(team_name: str):
    """Get comprehensive team statistics"""
    try:
        print(f"🏆 SoccerAPIData: Fetching stats for {team_name}")

        team_stats = await soccer_api_service.get_team_statistics(team_name)
        team_form = await soccer_api_service.get_team_form(team_name)

        return {
            "team": team_name,
            "statistics": team_stats,
            "recent_form": team_form,
            "source": "SoccerAPIData"
        }

    except Exception as e:
        print(f"❌ SoccerAPIData error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch team data: {str(e)}")

@app.get("/api/football/head-to-head/{home_team}/{away_team}")
async def get_head_to_head(home_team: str, away_team: str):
    """Get head-to-head record between two teams"""
    try:
        print(f"🏆 SoccerAPIData: Fetching H2H for {home_team} vs {away_team}")

        h2h_data = await soccer_api_service.get_head_to_head(home_team, away_team)

        return {
            "home_team": home_team,
            "away_team": away_team,
            "head_to_head": h2h_data,
            "source": "SoccerAPIData"
        }

    except Exception as e:
        print(f"❌ SoccerAPIData H2H error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch H2H data: {str(e)}")

@app.get("/api/predictions/{prediction_id}")
async def get_prediction_by_id(prediction_id: int):
    """Get a specific prediction by ID"""
    if prediction_id == 1:
        return Prediction(
            id=1,
            game=GameInfo(
                home_team="Arsenal",
                away_team="Liverpool",
                date=(datetime.now() + timedelta(hours=2)).isoformat()
            ),
            prediction_type="home_win",
            confidence=78.5,
            reasoning="Strong home record and recent form",
            factors=PredictionFactors(
                team_strength=0.12,
                recent_form=0.08,
                head_to_head=0.03,
                home_advantage=0.15
            )
        )
    else:
        raise HTTPException(status_code=404, detail="Prediction not found")

@app.get("/api/football/predict/{home_team}/{away_team}")
async def get_ai_prediction(home_team: str, away_team: str):
    """Get AI prediction for a specific match"""
    try:
        print(f"🤖 AI Prediction request: {home_team} vs {away_team}")

        prediction = await prediction_engine.analyze_match(home_team, away_team)

        return {
            "success": True,
            "match": f"{home_team} vs {away_team}",
            "prediction": prediction,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"❌ AI Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
