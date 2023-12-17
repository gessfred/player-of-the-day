from fastapi import APIRouter

from nba_api.stats.endpoints import leaguegamefinder, playbyplayv2
from datetime import datetime
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import LeagueGameFinder
import datetime
import pandas as pd
from nba_api.stats.endpoints import Scoreboard, BoxScoreTraditionalV2

router = APIRouter()

def get_teams_static_data():
    teams_static_data = teams.get_teams()
    teams_by_abb = {t["abbreviation"]: t for t in teams_static_data}

def get_daily_scores():
    yesterday = datetime.date.today() - datetime.timedelta(days=2)

    # Get scoreboard for yesterday's date
    scoreboard = Scoreboard(game_date=yesterday.strftime('%m/%d/%Y'))

    # Get list of game IDs for yesterday's games
    game_ids = [game['GAME_ID'] for game in scoreboard.game_header.get_data_frame().to_dict('records')]
    scoreboard.game_header.get_data_frame()

@router.get("/player-timeline")
def get_player_timeline(player: str, game_id: str):
    
    # check playbyplay cache for game
    # if not in cache, get play-by-play
    # Get yesterday's date
    
    game_id = "0022300002"
    pbp = playbyplayv2.PlayByPlayV2(game_id)
    play_by_play = pbp.get_data_frames()[0]

    # compute player-timeline and return
    return play_by_play