from typing import Dict, Any
import random
from datetime import datetime

class AIPredictionEngine:
    """Advanced AI engine that analyzes comprehensive sports data for realistic predictions"""

    def __init__(self, soccer_api_service):
        self.soccer_api = soccer_api_service

        # Club classification for context analysis
        self.big_six = ["manchester united", "chelsea", "arsenal", "liverpool", "manchester city", "tottenham"]
        self.historic_clubs = ["manchester united", "liverpool", "arsenal", "chelsea", "manchester city", "tottenham", "everton", "aston villa", "newcastle united", "west ham united"]

        # Expected positions for psychological analysis
        self.expected_positions = {
            "manchester city": 2, "arsenal": 3, "liverpool": 4, "chelsea": 5,
            "tottenham": 6, "manchester united": 7, "newcastle united": 10,
            "aston villa": 12, "west ham united": 11, "brighton": 13,
            "crystal palace": 14, "brentford": 15, "nottingham forest": 16,
            "fulham": 17, "everton": 12, "wolverhampton wanderers": 16,
            "burnley": 18, "leeds united": 19, "sunderland": 20
        }

    async def analyze_match(self, home_team: str, away_team: str) -> Dict[str, Any]:
        """Comprehensive match analysis using real data and advanced context"""

        print(f"🤖 AI: Advanced Analysis of {home_team} vs {away_team}")

        # Get real data
        standings = await self.soccer_api.get_premier_league_standings()
        h2h_data = await self.soccer_api.get_head_to_head(home_team, away_team)

        # Extract team positions from standings
        home_position, away_position = self._get_team_positions(standings, home_team, away_team)

        # Analyze head-to-head
        h2h_analysis = self._analyze_head_to_head(h2h_data, home_team, away_team)

        # Calculate all factors WITH TEAM PROFILES
        factors = self._calculate_prediction_factors(home_position, away_position, h2h_analysis, home_team, away_team)
        context_factors = self._calculate_context_factors(home_position, away_position, home_team, away_team)
        psych_factors = self._calculate_psychological_factors(home_position, away_position, home_team, away_team)
        advanced_context_factors = self._calculate_advanced_context_factors(home_team, away_team)

        # Combine all factors
        all_factors = {**factors, **context_factors, **psych_factors, **advanced_context_factors}

        # Make final prediction
        prediction = self._make_advanced_prediction(all_factors, home_team, away_team, h2h_analysis)

        return {
            "home_team": home_team,
            "away_team": away_team,
            "prediction": prediction,
            "factors": factors,
            "context_factors": context_factors,
            "psychological_factors": psych_factors,
            "advanced_context_factors": advanced_context_factors,
            "confidence": prediction["confidence"],
            "reasoning": prediction["reasoning"],
            "data_sources": {
                "standings": standings["success"] if isinstance(standings, dict) and standings else False,
                "head_to_head": h2h_data["success"] if isinstance(h2h_data, dict) and h2h_data else False
            }
        }

    def _get_team_positions(self, standings_data, home_team, away_team):
        """Extract team league positions from standings"""

        if isinstance(standings_data, str):
            print(f"⚠️ Standings data is a string: {standings_data}")
            return None, None

        if not standings_data or not isinstance(standings_data, dict) or not standings_data.get("success"):
            print(f"⚠️ Invalid standings data: {standings_data}")
            return None, None

        data = standings_data.get("data", {})
        stages = data.get("stage", [])

        if not stages:
            print("⚠️ No stages data available")
            return None, None

        standings = stages[0].get("standings", []) if stages else []

        if not standings:
            print("⚠️ No standings data available")
            return None, None

        home_pos = away_pos = None

        for team in standings:
            if not isinstance(team, dict):
                continue

            team_name = team.get("team_name", "").lower()

            if self._team_name_matches(team_name, home_team):
                home_pos = {
                    "position": team.get("position"),
                    "points": team.get("points"),
                    "wins": team.get("wins"),
                    "losses": team.get("losses"),
                    "draws": team.get("draws"),
                    "goals_for": team.get("goals_for"),
                    "goals_against": team.get("goals_against"),
                    "games_played": team.get("games_played"),
                    "team_name": team.get("team_name")
                }
            elif self._team_name_matches(team_name, away_team):
                away_pos = {
                    "position": team.get("position"),
                    "points": team.get("points"),
                    "wins": team.get("wins"),
                    "losses": team.get("losses"),
                    "draws": team.get("draws"),
                    "goals_for": team.get("goals_for"),
                    "goals_against": team.get("goals_against"),
                    "games_played": team.get("games_played"),
                    "team_name": team.get("team_name")
                }

        print(f"🔍 Found positions - Home: {home_pos}, Away: {away_pos}")
        return home_pos, away_pos

    def _team_name_matches(self, team_name_from_api, search_team):
        """Flexible team name matching"""
        team_name_clean = team_name_from_api.lower().strip()
        search_clean = search_team.replace("_", " ").lower().strip()

        if team_name_clean == search_clean:
            return True

        variations = {
            "manchester city": ["man city", "city"],
            "manchester united": ["man united", "man utd", "united"],
            "tottenham hotspur": ["tottenham", "spurs"],
            "brighton & hove albion": ["brighton"],
            "wolverhampton wanderers": ["wolves"],
            "west ham united": ["west ham"],
            "newcastle united": ["newcastle"],
            "nottingham forest": ["forest"],
            "afc bournemouth": ["bournemouth"],
            "crystal palace": ["palace"],
            "leeds united": ["leeds"]
        }

        for full_name, short_names in variations.items():
            if team_name_clean == full_name and search_clean in short_names:
                return True
            if search_clean == full_name and team_name_clean in short_names:
                return True

        return False

    def _analyze_head_to_head(self, h2h_data, home_team, away_team):
        """Analyze head-to-head historical data"""

        if isinstance(h2h_data, str):
            return {"advantage": "neutral", "confidence": 0.02}

        if not h2h_data or not isinstance(h2h_data, dict) or not h2h_data.get("success"):
            return {"advantage": "neutral", "confidence": 0.02}

        stats = h2h_data.get("head_to_head_data", {}).get("stats", {})
        overall = stats.get("overall", {})

        if not overall:
            return {"advantage": "neutral", "confidence": 0.02}

        team1_wins = overall.get("overall_team1_wins", 0)
        team2_wins = overall.get("overall_team2_wins", 0)
        total_games = overall.get("overall_games_played", 1)

        team1_win_rate = team1_wins / total_games if total_games > 0 else 0
        team2_win_rate = team2_wins / total_games if total_games > 0 else 0

        if team1_win_rate > team2_win_rate + 0.2:
            advantage = "home"
            confidence = min((team1_win_rate - team2_win_rate) * 0.3, 0.1)
        elif team2_win_rate > team1_win_rate + 0.2:
            advantage = "away"
            confidence = min((team2_win_rate - team1_win_rate) * 0.3, 0.1)
        else:
            advantage = "neutral"
            confidence = 0.02

        return {
            "advantage": advantage,
            "confidence": confidence,
            "team1_wins": team1_wins,
            "team2_wins": team2_wins,
            "total_games": total_games
        }
    def _calculate_prediction_factors(self, home_pos, away_pos, h2h_analysis, home_team, away_team):
        """Calculate prediction factors with team-specific intelligence"""

        # Initialize team profiles database
        if not hasattr(self, 'team_profiles_db'):
            from team_profiles import TeamProfilesDatabase
            self.team_profiles_db = TeamProfilesDatabase()

        # Get team profiles
        home_profile = self.team_profiles_db.get_team_profile(home_team)
        away_profile = self.team_profiles_db.get_team_profile(away_team)

        # Calculate style matchup
        style_matchup = self.team_profiles_db.calculate_style_matchup(home_team, away_team)

        factors = {
            "league_position": 0,
            "current_form": 0,
            "goal_form": 0,
            "head_to_head": h2h_analysis.get("confidence", 0) * 0.3,
            "home_advantage": 0,  # Will be calculated based on team profile
            "style_matchup": style_matchup["total_style_factor"],
            "squad_depth_advantage": 0,
            "manager_advantage": 0,
            "pressure_handling": 0,
            "total_confidence": 0
        }

        if home_pos and away_pos:
            # ENHANCED League position analysis
            pos_diff = away_pos["position"] - home_pos["position"]
            base_position_factor = min(pos_diff * 0.015, 0.2)

            # Adjust for big game mentality
            if home_profile["psychological_traits"]["big_game_mentality"] == "strong":
                base_position_factor += 0.03  # Big teams raise their game
            if away_profile["psychological_traits"]["big_game_mentality"] == "weak":
                base_position_factor += 0.02  # Weak mentality hurts away team more

            factors["league_position"] = base_position_factor

            # ENHANCED Current form analysis with consistency factor
            home_ppg = home_pos["points"] / max(home_pos["games_played"], 1)
            away_ppg = away_pos["points"] / max(away_pos["games_played"], 1)
            form_diff = home_ppg - away_ppg
            base_form = min(form_diff * 0.15, 0.25)

            # Adjust for consistency
            home_consistency = home_profile["psychological_traits"]["consistency"]
            away_consistency = away_profile["psychological_traits"]["consistency"]

            consistency_map = {
                "very_high": 1.1, "high": 1.05, "good": 1.02, "medium": 1.0,
                "inconsistent": 0.95, "poor": 0.90, "very_poor": 0.85
            }

            consistency_factor = (
                consistency_map.get(home_consistency, 1.0) /
                consistency_map.get(away_consistency, 1.0)
            )

            factors["current_form"] = base_form * consistency_factor

            # ENHANCED Goal form with playing style context
            home_goal_diff = home_pos["goals_for"] - home_pos["goals_against"]
            away_goal_diff = away_pos["goals_for"] - away_pos["goals_against"]
            goal_form_diff = home_goal_diff - away_goal_diff
            base_goal_form = min(goal_form_diff * 0.02, 0.15)

            # Adjust based on attacking/defensive style
            home_style = home_profile["playing_style"]["primary"]
            away_style = away_profile["playing_style"]["primary"]

            # Attacking teams get boost for good goal difference
            if home_style in ["possession_attack", "high_intensity_press"] and home_goal_diff > 3:
                base_goal_form += 0.03
            if away_style in ["possession_attack", "high_intensity_press"] and away_goal_diff > 3:
                base_goal_form -= 0.03

            # Defensive teams get boost for low goals conceded
            if home_style in ["defensive_low_block"] and home_pos["goals_against"] < 3:
                base_goal_form += 0.04
            if away_style in ["defensive_low_block"] and away_pos["goals_against"] < 3:
                base_goal_form -= 0.04

            factors["goal_form"] = base_goal_form

            # TEAM-SPECIFIC Home advantage (instead of generic 8%)
            home_advantage_base = home_profile["home_away_split"]["home_advantage"]
            away_resilience = away_profile["home_away_split"]["away_resilience"]

            # True home advantage = Home boost - Away resilience penalty
            factors["home_advantage"] = home_advantage_base + (1 - away_resilience)

            # NEW: Squad depth advantage
            home_depth = home_profile["squad_depth"]["depth_quality"]
            away_depth = away_profile["squad_depth"]["depth_quality"]

            depth_values = {
                "exceptional": 0.15, "good": 0.08, "limited": 0.02, "poor": -0.05
            }

            factors["squad_depth_advantage"] = (
                depth_values.get(home_depth, 0) - depth_values.get(away_depth, 0)
            )

            # NEW: Manager advantage
            home_tactical_flex = home_profile["manager_profile"]["tactical_flexibility"]
            away_tactical_flex = away_profile["manager_profile"]["tactical_flexibility"]

            home_big_game = home_profile["manager_profile"]["big_game_specialist"]
            away_big_game = away_profile["manager_profile"]["big_game_specialist"]

            tactical_values = {
                "very_high": 0.06, "high": 0.04, "medium": 0.02,
                "low": -0.02, "very_low": -0.04
            }

            manager_factor = tactical_values.get(home_tactical_flex, 0) - tactical_values.get(away_tactical_flex, 0)

            # Big game specialist bonus
            if home_big_game and not away_big_game:
                manager_factor += 0.03
            elif away_big_game and not home_big_game:
                manager_factor -= 0.03

            factors["manager_advantage"] = manager_factor

            # NEW: Pressure handling
            home_pressure = home_profile["psychological_traits"]["pressure_handling"]
            away_pressure = away_profile["psychological_traits"]["pressure_handling"]

            pressure_values = {
                "excellent": 0.08, "good": 0.04, "improving": 0.02, "medium": 0,
                "poor": -0.06, "very_poor": -0.12
            }

            factors["pressure_handling"] = (
                pressure_values.get(home_pressure, 0) - pressure_values.get(away_pressure, 0)
            )

        # Calculate total confidence with new factors
        factors["total_confidence"] = min(
            abs(factors["current_form"]) * 0.25 +
            abs(factors["league_position"]) * 0.20 +
            abs(factors["home_advantage"]) * 0.15 +
            abs(factors["style_matchup"]) * 0.15 +
            abs(factors["manager_advantage"]) * 0.10 +
            abs(factors["pressure_handling"]) * 0.10 +
            abs(factors["squad_depth_advantage"]) * 0.05,
            0.35  # Increased max confidence with more factors
        )

        print(f"🎯 TEAM PROFILE ANALYSIS:")
        print(f"📊 {home_team}: {home_profile['playing_style']['primary']} vs {away_team}: {away_profile['playing_style']['primary']}")
        print(f"🏠 Home Advantage: {factors['home_advantage']:.3f} (vs generic 0.08)")
        print(f"⚔️ Style Matchup: {factors['style_matchup']:.3f}")
        print(f"👥 Squad Depth: {factors['squad_depth_advantage']:.3f}")
        print(f"🎯 Manager: {factors['manager_advantage']:.3f}")
        print(f"💪 Pressure Handling: {factors['pressure_handling']:.3f}")

        return factors

    def _calculate_context_factors(self, home_pos, away_pos, home_team, away_team):
        """Calculate contextual factors that affect performance"""

        context_factors = {
            "goal_scoring_crisis": 0,
            "defensive_crisis": 0,
            "win_drought": 0,
            "squad_value_vs_performance": 0
        }

        if not home_pos or not away_pos:
            return context_factors

        # Goal scoring crisis detection (teams not scoring)
        home_goals_per_game = home_pos["goals_for"] / max(home_pos["games_played"], 1)
        away_goals_per_game = away_pos["goals_for"] / max(away_pos["games_played"], 1)

        # Crisis if scoring less than 0.8 goals per game
        if home_goals_per_game < 0.8:
            context_factors["goal_scoring_crisis"] -= 0.08  # -8% penalty
            print(f"🚨 {home_team} in goal scoring crisis: {home_goals_per_game:.1f} goals/game")

        if away_goals_per_game < 0.8:
            context_factors["goal_scoring_crisis"] += 0.08  # +8% for home team
            print(f"🚨 {away_team} in goal scoring crisis: {away_goals_per_game:.1f} goals/game")

        # Win drought detection
        if home_pos["wins"] == 0 and home_pos["games_played"] >= 2:
            context_factors["win_drought"] -= 0.12  # -12% penalty for no wins
            print(f"🚨 {home_team} WINLESS in {home_pos['games_played']} games")

        if away_pos["wins"] == 0 and away_pos["games_played"] >= 2:
            context_factors["win_drought"] += 0.12  # +12% boost for home team
            print(f"🚨 {away_team} WINLESS in {away_pos['games_played']} games")

        # Big club underperformance (using expected positions)
        home_expected = self.expected_positions.get(home_team.lower().replace("_", " "), home_pos["position"])
        away_expected = self.expected_positions.get(away_team.lower().replace("_", " "), away_pos["position"])

        home_underperform = home_pos["position"] - home_expected
        away_underperform = away_pos["position"] - away_expected

        # Penalty for underperforming expectations by 5+ positions
        if home_underperform >= 5:
            context_factors["squad_value_vs_performance"] -= 0.15  # -15% penalty
            print(f"📉 {home_team} underperforming: Expected {home_expected}, Currently {home_pos['position']}")

        if away_underperform >= 5:
            context_factors["squad_value_vs_performance"] += 0.15  # +15% boost
            print(f"📉 {away_team} underperforming: Expected {away_expected}, Currently {away_pos['position']}")

        return context_factors

    def _calculate_psychological_factors(self, home_pos, away_pos, home_team, away_team):
        """Calculate psychological and momentum factors"""

        psych_factors = {
            "pressure_factor": 0,
            "momentum_factor": 0,
            "expectation_vs_reality": 0
        }

        if not home_pos or not away_pos:
            return psych_factors

        # Pressure factor for teams in crisis positions
        if home_pos["position"] >= 17:  # Relegation zone
            psych_factors["pressure_factor"] -= 0.05  # Pressure hurts performance
        elif home_pos["position"] <= 4:  # Top 4 pressure
            psych_factors["pressure_factor"] += 0.03  # Champions League motivation

        if away_pos["position"] >= 17:
            psych_factors["pressure_factor"] += 0.05  # Home team benefits
        elif away_pos["position"] <= 4:
            psych_factors["pressure_factor"] -= 0.03

        # Momentum factor (recent form trend)
        home_recent_points = home_pos["points"] / max(home_pos["games_played"], 1)
        away_recent_points = away_pos["points"] / max(away_pos["games_played"], 1)

        if home_recent_points > 2.0:  # Excellent form (2+ points per game)
            psych_factors["momentum_factor"] += 0.06
        elif home_recent_points < 0.7:  # Poor form
            psych_factors["momentum_factor"] -= 0.06

        if away_recent_points > 2.0:
            psych_factors["momentum_factor"] -= 0.06
        elif away_recent_points < 0.7:
            psych_factors["momentum_factor"] += 0.06

        # Expectation vs reality factor
        home_expected = self.expected_positions.get(home_team.lower().replace("_", " "), home_pos["position"])
        away_expected = self.expected_positions.get(away_team.lower().replace("_", " "), away_pos["position"])

        expectation_gap = (home_pos["position"] - home_expected) - (away_pos["position"] - away_expected)
        psych_factors["expectation_vs_reality"] = min(expectation_gap * -0.01, 0.08)

        return psych_factors

    def _calculate_advanced_context_factors(self, home_team, away_team):
        """Calculate advanced match context factors"""

        # Initialize context analyzer
        if not hasattr(self, 'context_analyzer'):
            from advanced_match_context import AdvancedMatchContext
            self.context_analyzer = AdvancedMatchContext()

        # Analyze match context
        context_analysis = self.context_analyzer.analyze_match_context(home_team, away_team)

        context_factors = {
            "rivalry_intensity": context_analysis["rivalry_factor"]["impact"],
            "seasonal_impact": context_analysis["seasonal_context"]["impact"],
            "revenge_motivation": context_analysis["revenge_factor"]["impact"],
            "pressure_situation": context_analysis["pressure_context"]["impact"],
            "european_fatigue": context_analysis["competition_load"]["impact"],
            "context_summary": self.context_analyzer.get_context_summary(context_analysis)
        }

        print(f"🎯 ADVANCED MATCH CONTEXT:")
        print(f"📋 {context_factors['context_summary']}")
        if context_analysis["rivalry_factor"]["is_rivalry"]:
            print(f"🔥 RIVALRY DETECTED: {context_analysis['rivalry_factor']['rivalry_type']} - {context_analysis['rivalry_factor']['intensity']*100:.0f}% intensity boost")
        if abs(context_analysis["seasonal_context"]["impact"]) > 0.02:
                    print(f"📅 SEASONAL FACTOR: {context_analysis['seasonal_context']['active_context']} - {context_analysis['seasonal_context']['impact']*100:+.0f}%")
        if abs(context_analysis["competition_load"]["impact"]) > 0.03:
            print(f"🏆 EUROPEAN FATIGUE: {context_analysis['competition_load']['description']}")

        return context_factors

    def _make_advanced_prediction(self, all_factors, home_team, away_team, h2h_analysis):
        """Make final prediction combining all factor analysis"""

        # Calculate total home advantage
        home_advantage = 0
        for factor_name, value in all_factors.items():
            if factor_name not in ["total_confidence", "context_summary"]:  # Exclude non-numeric factors
                if isinstance(value, (int, float)):  # Only add numeric values
                    home_advantage += value

        # Add H2H advantage
        if h2h_analysis.get("advantage") == "home":
            home_advantage += all_factors.get("head_to_head", 0)
        elif h2h_analysis.get("advantage") == "away":
            home_advantage -= all_factors.get("head_to_head", 0)

        # ENHANCED CONFIDENCE SYSTEM WITH RIVALRY FACTORS
        base_confidence_modifier = 1.0

        # Rivalry reduces predictability but increases intensity
        if all_factors.get("rivalry_intensity", 0) > 0.15:  # Major rivalry
            base_confidence_modifier = 0.85  # 15% less predictable
            print(f"🔥 MAJOR RIVALRY: Reducing predictability by 15%")
        elif all_factors.get("rivalry_intensity", 0) > 0.05:  # Minor rivalry
            base_confidence_modifier = 0.92  # 8% less predictable

        # REALISTIC CONFIDENCE SYSTEM WITH ALL FACTORS
        if home_advantage > 0.25:  # Very strong home advantage
            prediction_type = "home_win"
            confidence = min(65 + (home_advantage * 50), 78) * base_confidence_modifier  # Max 78%
        elif home_advantage > 0.15:  # Strong home advantage
            prediction_type = "home_win"
            confidence = min(60 + (home_advantage * 60), 72) * base_confidence_modifier  # Max 72%
        elif home_advantage > 0.05:  # Moderate home advantage
            prediction_type = "home_win"
            confidence = min(55 + (home_advantage * 80), 65) * base_confidence_modifier  # Max 65%
        elif home_advantage < -0.25:  # Very strong away advantage
            prediction_type = "away_win"
            confidence = min(65 + (abs(home_advantage) * 50), 78) * base_confidence_modifier  # Max 78%
        elif home_advantage < -0.15:  # Strong away advantage
            prediction_type = "away_win"
            confidence = min(60 + (abs(home_advantage) * 60), 72) * base_confidence_modifier  # Max 72%
        elif home_advantage < -0.05:  # Moderate away advantage
            prediction_type = "away_win"
            confidence = min(55 + (abs(home_advantage) * 80), 65) * base_confidence_modifier  # Max 65%
        else:  # Very close match
            prediction_type = "close_match"
            confidence = round(random.uniform(51, 58) * base_confidence_modifier, 1)  # Very conservative

        # Build comprehensive reasoning
        reason_parts = []

        # NEW: Rivalry factor
        if abs(all_factors.get("rivalry_intensity", 0)) > 0.08:
            reason_parts.append("rivalry intensity")

        # NEW: Seasonal context
        if abs(all_factors.get("seasonal_impact", 0)) > 0.05:
            reason_parts.append("seasonal factors")

        # NEW: European fatigue
        if abs(all_factors.get("european_fatigue", 0)) > 0.04:
            if all_factors.get("european_fatigue", 0) > 0:
                reason_parts.append("opponent European fatigue")
            else:
                reason_parts.append("European fatigue disadvantage")

        # Current form reasoning
        if abs(all_factors.get("current_form", 0)) > 0.05:
            if all_factors.get("current_form", 0) > 0:
                reason_parts.append("superior current form")
            else:
                reason_parts.append("poor current form")

        # Goal scoring crisis
        if abs(all_factors.get("goal_scoring_crisis", 0)) > 0.08:
            if all_factors.get("goal_scoring_crisis", 0) < 0:
                reason_parts.append("goal scoring crisis")
            else:
                reason_parts.append("opponent's scoring struggles")

        # Win drought
        if abs(all_factors.get("win_drought", 0)) > 0.08:
            if all_factors.get("win_drought", 0) < 0:
                reason_parts.append("winless streak")
            else:
                reason_parts.append("opponent winless")

        # Big club underperforming
        if abs(all_factors.get("squad_value_vs_performance", 0)) > 0.08:
            if all_factors.get("squad_value_vs_performance", 0) < 0:
                reason_parts.append("underperforming expectations")
            else:
                reason_parts.append("opponent underperforming")

        # Pressure factor
        if abs(all_factors.get("pressure_factor", 0)) > 0.05:
            if all_factors.get("pressure_factor", 0) < 0:
                reason_parts.append("increased pressure")

        # League position
        if abs(all_factors.get("league_position", 0)) > 0.03:
            reason_parts.append("league position advantage")

        # Home advantage
        if all_factors.get("home_advantage", 0) > 0.05:
            reason_parts.append("home advantage")

        # Style matchup
        if abs(all_factors.get("style_matchup", 0)) > 0.04:
            if all_factors.get("style_matchup", 0) > 0:
                reason_parts.append("favorable tactical matchup")
            else:
                reason_parts.append("difficult tactical matchup")

        # Manager advantage
        if abs(all_factors.get("manager_advantage", 0)) > 0.03:
            if all_factors.get("manager_advantage", 0) > 0:
                reason_parts.append("managerial advantage")
            else:
                reason_parts.append("managerial disadvantage")

        # Pressure handling
        if abs(all_factors.get("pressure_handling", 0)) > 0.04:
            if all_factors.get("pressure_handling", 0) > 0:
                reason_parts.append("better pressure handling")
            else:
                reason_parts.append("pressure vulnerability")

        # H2H
        if abs(all_factors.get("head_to_head", 0)) > 0.03:
            reason_parts.append("historical record")

        # Determine winner for reasoning
        if prediction_type == "home_win":
            winner = home_team.replace("_", " ").title()
        elif prediction_type == "away_win":
            winner = away_team.replace("_", " ").title()
        else:
            winner = "Either team could win"

        # Build final reasoning with context
        context_note = ""
        if all_factors.get("rivalry_intensity", 0) > 0.1:
            context_note = " (rivalry factor increases unpredictability)"

        if reason_parts:
            reasoning = f"{winner} favored due to {', '.join(reason_parts[:4])}{context_note}"  # Limit to top 4 reasons
        else:
            reasoning = f"{winner} - balanced statistical analysis{context_note}"

        print(f"🎯 Enhanced prediction: {prediction_type}, confidence: {confidence:.1f}%")
        print(f"🔍 Total home advantage: {round(home_advantage, 3)}")
        print(f"💭 Reasoning: {reasoning}")

        return {
            "prediction_type": prediction_type,
            "confidence": round(confidence, 1),
            "reasoning": reasoning,
            "home_advantage_total": round(home_advantage, 3),
            "key_factors": reason_parts[:3]  # Top 3 factors
        }
