import pandas as pd
from pandasgui import show

"""
TODO:
Scoreboard requirements:
Player Names (split into the two teams)
Round wins
Round losses
Kills
Deaths
Kills per round
Average Damage per round
Multikill rounds (3K, 4K, 5K)
Deaths per round
Rounds survived
Zeus kills
Knife kills
Win
Opening kills
1vX rounds
"""

class ScoreboardGenerator:
    parser = None
    scoreboard = None

    def __init__(self, parser):
        self.parser = parser
        self.GenerateScoreboard()
        self.DisplayScoreboard()


    def GenerateScoreboard(self):
        ##TODO
        ## current code is a sample, use separate functions for each field. 
        ## Similar code can be found on Awpy's awpy2 branch
        max_tick = self.parser.parse_event("round_end")["tick"].max()
        wanted_fields = ["kills_total", "deaths_total", "mvps", "headshot_kills_total",
                        "ace_rounds_total", "4k_rounds_total", "3k_rounds_total",
                        "objective_total", "damage_total", "enemies_flashed_total"]
        self.scoreboard= self.parser.parse_ticks(wanted_fields, ticks=[max_tick])

    def DisplayScoreboard(self):
        show(self.scoreboard)

