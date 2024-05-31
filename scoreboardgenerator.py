import pandas as pd
from pandasgui import show
import time

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

    def __init__(self, parser):
        ## initializ all class variables here
        self.parser = parser
        self.scoreboard = None

        self.players = None
        self.round_starts = None
        self.round_ends = None
        self.all_round_deaths = []
        self.SetupScoreboardVariables()
        self.GenerateScoreboard()
        self.DisplayScoreboard()

    def SetupScoreboardVariables(self):
        self.SetPlayers()
        self.FilterRoundEvents()

    def SetPlayers(self):
        max_tick = self.parser.parse_event("round_end")["tick"].max()
        players_df = self.parser.parse_ticks(["team_name"], ticks=[max_tick])
        self.players = pd.DataFrame(players_df['name'].unique(), columns=['name'])

    def FilterRoundEvents(self):
        round_starts = self.parser.parse_event("round_start", other=["total_rounds_played"])
        round_ends = self.parser.parse_event("round_end", other=["total_rounds_played"])
    
        ## Need to filter out knife round, first we remove the 0th tick round from round_starts
        round_starts = round_starts[round_starts['tick'] != 0]
        ## Faceit resets server multiple times for 1st pistol, if multiple ticks for a round take the highest tick
        round_starts = round_starts.loc[round_starts.groupby('total_rounds_played')['tick'].idxmax()]
        ## Repeat for round_ends, to remove knife round
        round_ends = round_ends.loc[round_ends.groupby('total_rounds_played')['tick'].idxmax()]
        ## Reset index for both for clarity
        round_starts.reset_index(drop=True, inplace=True)
        round_ends.reset_index(drop=True, inplace=True)
        ## Store cleaned round starts and ends
        self.round_starts = round_starts
        self.round_ends = round_ends

        ## Get max rounds & all deaths for loop
        max_rounds = round_ends["total_rounds_played"].max()
        deaths = self.parser.parse_event("player_death", other=["total_rounds_played"])
        deaths_headers = deaths.columns

        ## get all deaths that occur between the start tick and end tick of a round
        for round_idx in range(0,max_rounds):
            round_deaths = pd.DataFrame(columns = deaths_headers)
            for _,death in deaths.iterrows():
                death_round = death["total_rounds_played"]
                death_tick = death["tick"]
                is_death_in_round = death_round == round_idx
                has_round_started = round_starts.iloc[round_idx]["tick"] < death_tick
                round_hasnt_finished = round_ends.iloc[round_idx]["tick"] > death_tick
                if is_death_in_round and has_round_started and round_hasnt_finished:
                    round_deaths = pd.concat([round_deaths, death.to_frame().T], ignore_index=True)        
            self.all_round_deaths.append(round_deaths)

    def GenerateScoreboard(self):
        ##TODO opening kills & Zeus kills
        ## Get all stats
        aggregate_stats = self.GetAggregateStats()
        rounds_won = self.GetRoundsWon()
        clutches = self.GetClutches()

        ## Merge in preferred order
        scoreboard = pd.merge(self.players,rounds_won, on="name")
        scoreboard = pd.merge(scoreboard,aggregate_stats, on = "name")
        scoreboard = pd.merge(scoreboard,clutches,on="name")

        ## Sort and return
        scoreboard = scoreboard.sort_values(by=['team_rounds_total', 'kills_total'], ascending=[False, False])
        scoreboard.reset_index(drop=True, inplace=True)
        self.scoreboard = scoreboard

    def GetAggregateStats(self):
        max_tick = self.parser.parse_event("round_end")["tick"].max()
        wanted_fields = ["kills_total","assists_total", "deaths_total", "headshot_kills_total",
                        "ace_rounds_total", "4k_rounds_total", "3k_rounds_total",
                        "damage_total", "enemies_flashed_total"]
        aggregate_stats = self.parser.parse_ticks(wanted_fields, ticks=[max_tick])
        aggregate_stats = aggregate_stats.drop(columns=['steamid', 'tick'])
        return aggregate_stats

    def GetRoundsWon(self):
        max_tick = self.parser.parse_event("round_end")["tick"].max()
        rounds_won = self.parser.parse_ticks(["team_rounds_total"], ticks=[max_tick])
        rounds_won = rounds_won.drop(columns=['steamid', 'tick'])
        return rounds_won

    def GetClutches(self):
        total_rounds_played = 0
        round_ends = self.round_ends
        clutches = self.players.copy(deep=True)
        clutches['1vsX'] = 0
        is_alive_df = self.parser.parse_ticks(["is_alive", "team_name"])
        for round_deaths in self.all_round_deaths:
            total_rounds_played += 1
            for _, death in round_deaths.iterrows():
                is_alive_in_round_df = is_alive_df[is_alive_df["tick"] == death["tick"]]
                ct_alive = is_alive_in_round_df[(is_alive_in_round_df["team_name"] == "CT") & (is_alive_in_round_df["is_alive"] == True)]
                t_alive = is_alive_in_round_df[(is_alive_in_round_df["team_name"] == "TERRORIST") & (is_alive_in_round_df["is_alive"] == True)]
                winner = round_ends[round_ends['total_rounds_played'] == total_rounds_played]['winner']
                winner = winner.item()
                # 3 = CT
                if len(ct_alive) == 1 and winner == "CT":
                    name = ct_alive["name"].iloc[0]
                    clutches.loc[clutches['name'] == name, '1vsX'] += 1
                    break
                # 2 = T
                if len(t_alive) == 1 and winner == "T":
                    name = t_alive["name"].iloc[0]
                    clutches.loc[clutches['name'] == name, '1vsX'] += 1
                    break
        return clutches

    def DisplayScoreboard(self):
        show(self.scoreboard)

