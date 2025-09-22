# team_profiles.py - New file for comprehensive team intelligence

class TeamProfilesDatabase:
    """Comprehensive database of team-specific characteristics and patterns"""

    def __init__(self):
        self.team_profiles = {
            # BIG SIX PROFILES
            "manchester_city": {
                "playing_style": {
                    "primary": "possession_based",
                    "possession_percentage": 68,
                    "build_up_style": "patient_technical",
                    "pressing_intensity": "high",
                    "width_focus": "balanced",
                    "tempo": "variable"
                },
                "home_away_split": {
                    "home_advantage": 0.12,  # +12% at home
                    "away_resilience": 0.95,  # Only -5% away
                    "neutral_venue": 1.02    # +2% at neutral venues
                },
                "squad_depth": {
                    "depth_quality": "exceptional",  # Can rotate without drop-off
                    "injury_resilience": 0.92,      # Only -8% when injuries
                    "key_player_dependency": 0.15   # Low dependency on single player
                },
                "manager_profile": {
                    "tactical_flexibility": "very_high",
                    "big_game_specialist": True,
                    "pressure_response": "excellent",
                    "in_game_adjustments": "masterful"
                },
                "psychological_traits": {
                    "pressure_handling": "excellent",
                    "big_game_mentality": "strong",
                    "comeback_ability": "high",
                    "consistency": "very_high"
                }
            },

            "manchester_united": {
                "playing_style": {
                    "primary": "transitional_counter",
                    "possession_percentage": 52,
                    "build_up_style": "direct_mixed",
                    "pressing_intensity": "medium",
                    "width_focus": "wing_heavy",
                    "tempo": "variable"
                },
                "home_away_split": {
                    "home_advantage": 0.15,  # +15% at Old Trafford (historic ground)
                    "away_resilience": 0.78,  # -22% away (major weakness)
                    "neutral_venue": 0.88    # -12% neutral
                },
                "squad_depth": {
                    "depth_quality": "poor",           # Major drop-off in quality
                    "injury_resilience": 0.72,        # -28% when injuries hit
                    "key_player_dependency": 0.35     # Very dependent on few players
                },
                "manager_profile": {
                    "tactical_flexibility": "medium",
                    "big_game_specialist": False,
                    "pressure_response": "poor",       # Current crisis
                    "in_game_adjustments": "limited"
                },
                "psychological_traits": {
                    "pressure_handling": "poor",       # Current state
                    "big_game_mentality": "inconsistent",
                    "comeback_ability": "medium",
                    "consistency": "very_poor"        # Current form
                }
            },

            "arsenal": {
                "playing_style": {
                    "primary": "possession_attack",
                    "possession_percentage": 62,
                    "build_up_style": "patient_technical",
                    "pressing_intensity": "very_high",
                    "width_focus": "wide_overloads",
                    "tempo": "high"
                },
                "home_away_split": {
                    "home_advantage": 0.18,  # +18% at Emirates (loud crowd)
                    "away_resilience": 0.85,  # -15% away
                    "neutral_venue": 0.92    # -8% neutral
                },
                "squad_depth": {
                    "depth_quality": "good",
                    "injury_resilience": 0.82,        # -18% when injuries
                    "key_player_dependency": 0.25     # Some key player reliance
                },
                "manager_profile": {
                    "tactical_flexibility": "high",
                    "big_game_specialist": True,
                    "pressure_response": "good",
                    "in_game_adjustments": "good"
                },
                "psychological_traits": {
                    "pressure_handling": "improving",
                    "big_game_mentality": "strong",
                    "comeback_ability": "high",
                    "consistency": "good"
                }
            },

            "liverpool": {
                "playing_style": {
                    "primary": "high_intensity_press",
                    "possession_percentage": 58,
                    "build_up_style": "direct_vertical",
                    "pressing_intensity": "extreme",
                    "width_focus": "full_back_overlaps",
                    "tempo": "very_high"
                },
                "home_away_split": {
                    "home_advantage": 0.22,  # +22% at Anfield (best atmosphere)
                    "away_resilience": 0.88,  # -12% away
                    "neutral_venue": 0.95    # -5% neutral
                },
                "squad_depth": {
                    "depth_quality": "good",
                    "injury_resilience": 0.75,        # -25% when injuries (aging squad)
                    "key_player_dependency": 0.40     # Very dependent on Salah/VVD
                },
                "manager_profile": {
                    "tactical_flexibility": "medium",  # Klopp has preferred system
                    "big_game_specialist": True,
                    "pressure_response": "excellent",
                    "in_game_adjustments": "good"
                },
                "psychological_traits": {
                    "pressure_handling": "excellent",
                    "big_game_mentality": "exceptional", # Champions League specialists
                    "comeback_ability": "legendary",     # Istanbul, Barcelona
                    "consistency": "high"
                }
            },

            "chelsea": {
                "playing_style": {
                    "primary": "flexible_tactical",
                    "possession_percentage": 55,
                    "build_up_style": "adaptable",
                    "pressing_intensity": "medium_high",
                    "width_focus": "balanced",
                    "tempo": "medium"
                },
                "home_away_split": {
                    "home_advantage": 0.14,  # +14% at Stamford Bridge
                    "away_resilience": 0.82,  # -18% away
                    "neutral_venue": 0.90    # -10% neutral
                },
                "squad_depth": {
                    "depth_quality": "exceptional",   # Huge expensive squad
                    "injury_resilience": 0.90,       # -10% when injuries
                    "key_player_dependency": 0.20    # Less dependent on individuals
                },
                "manager_profile": {
                    "tactical_flexibility": "very_high", # Pochettino adaptable
                    "big_game_specialist": True,
                    "pressure_response": "good",
                    "in_game_adjustments": "excellent"
                },
                "psychological_traits": {
                    "pressure_handling": "good",
                    "big_game_mentality": "strong",    # Cup specialists
                    "comeback_ability": "high",
                    "consistency": "inconsistent"      # Hot and cold
                }
            },

            "tottenham": {
                "playing_style": {
                    "primary": "counter_attack",
                    "possession_percentage": 48,
                    "build_up_style": "direct_transition",
                    "pressing_intensity": "medium",
                    "width_focus": "wing_backs",
                    "tempo": "explosive_bursts"
                },
                "home_away_split": {
                    "home_advantage": 0.16,  # +16% at new stadium
                    "away_resilience": 0.75,  # -25% away (mental weakness)
                    "neutral_venue": 0.85    # -15% neutral
                },
                "squad_depth": {
                    "depth_quality": "poor",          # Big drop-off after first XI
                    "injury_resilience": 0.70,       # -30% when injuries
                    "key_player_dependency": 0.45    # Extremely Kane-dependent historically
                },
                "manager_profile": {
                    "tactical_flexibility": "medium",
                    "big_game_specialist": False,      # Historically struggle
                    "pressure_response": "poor",       # Bottling reputation
                    "in_game_adjustments": "limited"
                },
                "psychological_traits": {
                    "pressure_handling": "poor",       # Famous for bottling
                    "big_game_mentality": "weak",      # Cup final record
                    "comeback_ability": "low",         # Rarely fight back
                    "consistency": "poor"              # Spursy moments
                }
            },

            # MID-TABLE PROFILES
            "west_ham": {
                "playing_style": {
                    "primary": "direct_physical",
                    "possession_percentage": 45,
                    "build_up_style": "long_ball_crosses",
                    "pressing_intensity": "medium",
                    "width_focus": "wide_crosses",
                    "tempo": "medium"
                },
                "home_away_split": {
                    "home_advantage": 0.20,  # +20% at London Stadium
                    "away_resilience": 0.70,  # -30% away (poor travelers)
                    "neutral_venue": 0.80    # -20% neutral
                },
                "squad_depth": {
                    "depth_quality": "limited",
                    "injury_resilience": 0.65,       # -35% when injuries
                    "key_player_dependency": 0.50    # Very dependent on few players
                },
                "manager_profile": {
                    "tactical_flexibility": "low",
                    "big_game_specialist": False,
                    "pressure_response": "medium",
                    "in_game_adjustments": "limited"
                },
                "psychological_traits": {
                    "pressure_handling": "medium",
                    "big_game_mentality": "inconsistent",
                    "comeback_ability": "medium",
                    "consistency": "poor"
                }
            },

            "burnley": {
                "playing_style": {
                    "primary": "defensive_low_block",
                    "possession_percentage": 38,
                    "build_up_style": "direct_long_ball",
                    "pressing_intensity": "low",
                    "width_focus": "central_compact",
                    "tempo": "slow_controlled"
                },
                "home_away_split": {
                    "home_advantage": 0.25,  # +25% at Turf Moor (fortress mentality)
                    "away_resilience": 0.60,  # -40% away (one-dimensional)
                    "neutral_venue": 0.75    # -25% neutral
                },
                "squad_depth": {
                    "depth_quality": "limited",
                    "injury_resilience": 0.60,       # -40% when injuries hit
                    "key_player_dependency": 0.35    # Dependent on key defenders
                },
                "manager_profile": {
                    "tactical_flexibility": "very_low", # Dyche one system
                    "big_game_specialist": True,        # Giant killers
                    "pressure_response": "excellent",   # Relegation fighters
                    "in_game_adjustments": "minimal"
                },
                "psychological_traits": {
                    "pressure_handling": "excellent",   # Used to pressure
                    "big_game_mentality": "strong",     # Love giant killing
                    "comeback_ability": "low",          # Score early or struggle
                    "consistency": "high"               # Consistent approach
                }
            }
        }

    def get_team_profile(self, team_name):
        """Get comprehensive team profile"""
        clean_name = team_name.lower().replace(" ", "_")
        return self.team_profiles.get(clean_name, self._get_default_profile())

    def _get_default_profile(self):
        """Default profile for teams not in database"""
        return {
            "playing_style": {
                "primary": "balanced",
                "possession_percentage": 50,
                "build_up_style": "mixed",
                "pressing_intensity": "medium",
                "width_focus": "balanced",
                "tempo": "medium"
            },
            "home_away_split": {
                "home_advantage": 0.08,
                "away_resilience": 0.90,
                "neutral_venue": 0.95
            },
            "squad_depth": {
                "depth_quality": "limited",
                "injury_resilience": 0.75,
                "key_player_dependency": 0.30
            },
            "manager_profile": {
                "tactical_flexibility": "medium",
                "big_game_specialist": False,
                "pressure_response": "medium",
                "in_game_adjustments": "medium"
            },
            "psychological_traits": {
                "pressure_handling": "medium",
                "big_game_mentality": "medium",
                "comeback_ability": "medium",
                "consistency": "medium"
            }
        }

    def calculate_style_matchup(self, home_team, away_team):
        """Calculate how team styles match up against each other"""
        home_profile = self.get_team_profile(home_team)
        away_profile = self.get_team_profile(away_team)

        home_style = home_profile["playing_style"]["primary"]
        away_style = away_profile["playing_style"]["primary"]

        # Style matchup matrix
        style_advantages = {
            "possession_based": {
                "defensive_low_block": -0.08,  # Struggle vs parked bus
                "high_intensity_press": 0.05,  # Good vs high press
                "counter_attack": 0.03
            },
            "high_intensity_press": {
                "possession_based": -0.05,     # Possession teams handle press
                "counter_attack": 0.08,        # Press stops counters
                "defensive_low_block": -0.12   # Can't press low block
            },
            "defensive_low_block": {
                "possession_based": 0.08,      # Frustrate possession teams
                "high_intensity_press": 0.12,  # Press gets tired
                "direct_physical": -0.05
            },
            "counter_attack": {
                "possession_based": -0.03,     # Less space vs possession
                "high_intensity_press": -0.08, # Press stops counters
                "defensive_low_block": 0.05
            }
        }

        home_advantage = style_advantages.get(home_style, {}).get(away_style, 0)
        away_advantage = style_advantages.get(away_style, {}).get(home_style, 0)

        return {
            "home_style_advantage": home_advantage,
            "away_style_advantage": away_advantage,
            "total_style_factor": home_advantage - away_advantage
        }
