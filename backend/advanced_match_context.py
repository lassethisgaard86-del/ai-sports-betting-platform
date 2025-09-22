# advanced_match_context.py - New file for match context intelligence

from datetime import datetime
import re

class AdvancedMatchContext:
    """Analyzes contextual factors that significantly impact match outcomes"""

    def __init__(self):
        # Derby and rivalry definitions
        self.rivalries = {
            # MAJOR DERBIES (High emotional intensity)
            "north_london_derby": {
                "teams": ["arsenal", "tottenham"],
                "intensity": 0.20,  # +20% emotional boost
                "unpredictability": 0.25,  # Form matters 25% less
                "description": "North London Derby - form goes out the window"
            },
            "manchester_derby": {
                "teams": ["manchester_city", "manchester_united"],
                "intensity": 0.18,
                "unpredictability": 0.22,
                "description": "Manchester Derby - tactical chess match"
            },
            "merseyside_derby": {
                "teams": ["liverpool", "everton"],
                "intensity": 0.22,  # Highest intensity
                "unpredictability": 0.28,
                "description": "Merseyside Derby - anything can happen"
            },
            "northwest_derby": {
                "teams": ["liverpool", "manchester_united"],
                "intensity": 0.19,
                "unpredictability": 0.24,
                "description": "Historic rivalry - hatred overrides form"
            },

            # LONDON DERBIES (Medium-high intensity)
            "west_london_derby": {
                "teams": ["chelsea", "fulham"],
                "intensity": 0.12,
                "unpredictability": 0.15,
                "description": "West London Derby"
            },
            "south_london_derby": {
                "teams": ["crystal_palace", "millwall"],
                "intensity": 0.15,
                "unpredictability": 0.18,
                "description": "South London Derby"
            },
            "chelsea_arsenal": {
                "teams": ["chelsea", "arsenal"],
                "intensity": 0.14,
                "unpredictability": 0.17,
                "description": "London rivalry with recent edge"
            },

            # REGIONAL RIVALRIES (Medium intensity)
            "yorkshire_derby": {
                "teams": ["leeds_united", "sheffield_united"],
                "intensity": 0.16,
                "unpredictability": 0.20,
                "description": "Yorkshire Derby - fierce local pride"
            },
            "midlands_derby": {
                "teams": ["aston_villa", "birmingham_city"],
                "intensity": 0.17,
                "unpredictability": 0.21,
                "description": "Birmingham Derby - Second City rivalry"
            },

            # BIG 6 VS BIG 6 (Tactical intensity)
            "big_6_clash": {
                "teams": ["manchester_city", "arsenal", "liverpool", "chelsea", "tottenham", "manchester_united"],
                "intensity": 0.10,
                "unpredictability": 0.15,
                "description": "Big 6 clash - tactical battle"
            }
        }

        # Revenge factor tracking
        self.revenge_scenarios = {
            "embarrassing_defeat": 0.12,  # Lost by 4+ goals recently
            "cup_elimination": 0.08,     # Knocked out of cup competition
            "title_deciding": 0.15,      # Lost crucial title deciding game
            "relegation_battle": 0.10    # Lost crucial relegation game
        }

        # Seasonal context factors
        self.seasonal_factors = {
            "august_chaos": {
                "months": [8],
                "unpredictability": 0.25,  # 25% more unpredictable
                "description": "August chaos - new signings, fitness issues"
            },
            "christmas_period": {
                "months": [12],
                "squad_depth_importance": 0.20,  # Squad depth 20% more important
                "description": "Christmas fixtures - squad depth crucial"
            },
            "january_window": {
                "months": [1],
                "unsettled_players": 0.08,  # Players distracted by transfers
                "description": "January transfer window uncertainty"
            },
            "run_in_pressure": {
                "months": [4, 5],
                "pressure_multiplier": 1.3,  # 30% more pressure
                "description": "Season run-in - every point matters"
            },
            "dead_rubber_period": {
                "months": [5],
                "motivation_penalty": 0.12,  # Teams with nothing to play for
                "description": "Dead rubber games - motivation issues"
            }
        }

        # Competition load analysis
        self.competition_fatigue = {
            "champions_league": {
                "european_hangover": 0.08,  # 3-day rule after CL games
                "prestige_motivation": 0.05,  # Motivation boost for CL teams
                "description": "Champions League teams affected by European commitments"
            },
            "europa_league": {
                "european_hangover": 0.05,  # Less fatigue than CL
                "thursday_effect": 0.06,    # Thursday games affect Sunday more than Saturday
                "description": "Europa League Thursday night fatigue"
            },
            "cup_competitions": {
                "fa_cup_distraction": 0.03,  # Slight distraction
                "league_cup_rest": -0.02,    # Often rest players, so fresher for league
                "description": "Domestic cup competition effects"
            }
        }

    def analyze_match_context(self, home_team: str, away_team: str, match_date: datetime = None) -> dict:
        """Comprehensive match context analysis"""

        if match_date is None:
            match_date = datetime.now()

        context_analysis = {
            "rivalry_factor": self._analyze_rivalry(home_team, away_team),
            "seasonal_context": self._analyze_seasonal_context(match_date),
            "revenge_factor": self._analyze_revenge_scenarios(home_team, away_team),
            "pressure_context": self._analyze_pressure_context(home_team, away_team, match_date),
            "competition_load": self._analyze_competition_fatigue(home_team, away_team),
            "external_factors": self._analyze_external_factors(match_date),
            "total_context_impact": 0
        }

        # Calculate total context impact
        context_analysis["total_context_impact"] = (
            context_analysis["rivalry_factor"]["impact"] +
            context_analysis["seasonal_context"]["impact"] +
            context_analysis["revenge_factor"]["impact"] +
            context_analysis["pressure_context"]["impact"] +
            context_analysis["competition_load"]["impact"]
        )

        return context_analysis

    def _analyze_rivalry(self, home_team: str, away_team: str) -> dict:
        """Detect and analyze rivalry intensity"""

        home_clean = home_team.lower().replace("_", " ").strip()
        away_clean = away_team.lower().replace("_", " ").strip()

        # Check for specific rivalries
        for rivalry_name, rivalry_data in self.rivalries.items():
            teams = rivalry_data["teams"]

            # Convert team names for matching
            teams_clean = [team.replace("_", " ") for team in teams]

            if home_clean in teams_clean and away_clean in teams_clean:
                return {
                    "is_rivalry": True,
                    "rivalry_type": rivalry_name,
                    "intensity": rivalry_data["intensity"],
                    "unpredictability": rivalry_data["unpredictability"],
                    "description": rivalry_data["description"],
                    "impact": rivalry_data["intensity"]  # Positive impact for emotional boost
                }

        # Check for Big 6 clash
        big_6_teams = self.rivalries["big_6_clash"]["teams"]
        big_6_clean = [team.replace("_", " ") for team in big_6_teams]

        if home_clean in big_6_clean and away_clean in big_6_clean:
            return {
                "is_rivalry": True,
                "rivalry_type": "big_6_clash",
                "intensity": 0.10,
                "unpredictability": 0.15,
                "description": "Big 6 tactical battle",
                "impact": 0.05  # Moderate impact
            }

        return {
            "is_rivalry": False,
            "rivalry_type": "none",
            "intensity": 0,
            "unpredictability": 0,
            "description": "No significant rivalry",
            "impact": 0
        }

    def _analyze_seasonal_context(self, match_date: datetime) -> dict:
        """Analyze seasonal timing effects"""

        current_month = match_date.month

        for context_name, context_data in self.seasonal_factors.items():
            if current_month in context_data.get("months", []):
                impact = 0

                # Calculate impact based on context type
                if "unpredictability" in context_data:
                    impact += context_data["unpredictability"] * 0.3
                if "squad_depth_importance" in context_data:
                    impact += context_data["squad_depth_importance"] * 0.2
                if "pressure_multiplier" in context_data:
                    impact += (context_data["pressure_multiplier"] - 1) * 0.1
                if "motivation_penalty" in context_data:
                    impact -= context_data["motivation_penalty"] * 0.8

                return {
                    "active_context": context_name,
                    "description": context_data["description"],
                    "month": current_month,
                    "impact": impact,
                    "details": context_data
                }

        return {
            "active_context": "normal_period",
            "description": "Normal season period",
            "month": current_month,
            "impact": 0,
            "details": {}
        }

    def _analyze_revenge_scenarios(self, home_team: str, away_team: str) -> dict:
        """Analyze potential revenge motivations"""

        # This would typically check recent head-to-head results
        # For now, we'll use probabilistic analysis based on team names

        revenge_probability = 0
        revenge_type = "none"

        # Big clubs more likely to have revenge scenarios
        big_clubs = ["manchester_united", "chelsea", "arsenal", "liverpool", "manchester_city", "tottenham"]

        home_clean = home_team.lower().replace(" ", "_")
        away_clean = away_team.lower().replace(" ", "_")

        if home_clean in big_clubs or away_clean in big_clubs:
            revenge_probability = 0.15  # 15% chance of revenge scenario
            revenge_type = "potential_revenge"

        impact = revenge_probability * 0.08  # Convert to impact factor

        return {
            "has_revenge_factor": revenge_probability > 0.1,
            "revenge_type": revenge_type,
            "probability": revenge_probability,
            "impact": impact,
            "description": f"Potential revenge scenario ({revenge_probability*100:.0f}% chance)"
        }

    def _analyze_pressure_context(self, home_team: str, away_team: str, match_date: datetime) -> dict:
        """Analyze pressure situations based on timing and stakes"""

        pressure_situations = []
        total_impact = 0

        # End of season pressure (April/May)
        if match_date.month in [4, 5]:
            pressure_situations.append("end_of_season_pressure")
            total_impact += 0.06

        # Christmas period pressure (December/January)
        if match_date.month in [12, 1]:
            pressure_situations.append("festive_period_pressure")
            total_impact += 0.04

        # Big club expectations
        big_clubs = ["manchester_united", "chelsea", "arsenal", "liverpool", "manchester_city", "tottenham"]
        home_clean = home_team.lower().replace(" ", "_")
        away_clean = away_team.lower().replace(" ", "_")

        if home_clean in big_clubs:
            pressure_situations.append("big_club_expectations")
            total_impact += 0.03

        return {
            "pressure_situations": pressure_situations,
            "impact": total_impact,
            "description": f"Pressure factors: {', '.join(pressure_situations) if pressure_situations else 'Low pressure'}"
        }

    def _analyze_competition_fatigue(self, home_team: str, away_team: str) -> dict:
        """Analyze European competition fatigue effects"""

        # European competition teams (would be dynamic in real system)
        european_teams = {
            "champions_league": ["manchester_city", "arsenal", "manchester_united", "newcastle_united"],
            "europa_league": ["liverpool", "brighton", "west_ham_united", "aston_villa"]
        }

        home_clean = home_team.lower().replace(" ", "_")
        away_clean = away_team.lower().replace(" ", "_")

        home_fatigue = 0
        away_fatigue = 0

        # Champions League fatigue
        if home_clean in european_teams["champions_league"]:
            home_fatigue += 0.08
        if away_clean in european_teams["champions_league"]:
            away_fatigue += 0.08

        # Europa League fatigue
        if home_clean in european_teams["europa_league"]:
            home_fatigue += 0.05
        if away_clean in european_teams["europa_league"]:
            away_fatigue += 0.05

        net_impact = away_fatigue - home_fatigue  # Positive favors home team

        return {
            "home_european_fatigue": home_fatigue,
            "away_european_fatigue": away_fatigue,
            "impact": net_impact,
            "description": f"European fatigue - Home: {home_fatigue:.2f}, Away: {away_fatigue:.2f}"
        }

    def _analyze_external_factors(self, match_date: datetime) -> dict:
        """Analyze external factors like weather, international breaks, etc."""

        external_factors = []

        # Post-international break (would check actual dates in real system)
        # Assuming international breaks happen certain weekends
        if match_date.day in [15, 16]:  # Simplified check
            external_factors.append("post_international_break")

        # Midweek fixture fatigue
        if match_date.weekday() in [1, 2, 3]:  # Tuesday, Wednesday, Thursday
            external_factors.append("midweek_fixture")

        return {
            "external_factors": external_factors,
            "impact": len(external_factors) * 0.02,  # Small impact per factor
            "description": f"External factors: {', '.join(external_factors) if external_factors else 'None'}"
        }

    def get_context_summary(self, context_analysis: dict) -> str:
        """Generate human-readable context summary"""

        summary_parts = []

                # Rivalry
        if context_analysis["rivalry_factor"]["is_rivalry"]:
            rivalry_desc = context_analysis["rivalry_factor"]["description"]
            intensity = context_analysis["rivalry_factor"]["intensity"]
            summary_parts.append(f"🔥 {rivalry_desc} (+{intensity*100:.0f}% intensity)")

        # Seasonal context
        if context_analysis["seasonal_context"]["impact"] != 0:
            seasonal_desc = context_analysis["seasonal_context"]["description"]
            impact = context_analysis["seasonal_context"]["impact"]
            summary_parts.append(f"📅 {seasonal_desc} ({impact*100:+.0f}% impact)")

        # Revenge factor
        if context_analysis["revenge_factor"]["has_revenge_factor"]:
            revenge_desc = context_analysis["revenge_factor"]["description"]
            summary_parts.append(f"⚔️ {revenge_desc}")

        # Pressure context
        if context_analysis["pressure_context"]["impact"] > 0:
            pressure_desc = context_analysis["pressure_context"]["description"]
            summary_parts.append(f"💪 {pressure_desc}")

        # Competition fatigue
        if abs(context_analysis["competition_load"]["impact"]) > 0.03:
            fatigue_desc = context_analysis["competition_load"]["description"]
            summary_parts.append(f"🏆 {fatigue_desc}")

        if summary_parts:
            return " | ".join(summary_parts)
        else:
            return "📋 Standard league fixture - no major contextual factors"
