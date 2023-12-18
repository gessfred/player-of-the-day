from fastapi import APIRouter, Depends

from nba_api.stats.endpoints import leaguegamefinder, playbyplayv2
from datetime import datetime
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import LeagueGameFinder
import datetime
import pandas as pd
from nba_api.stats.endpoints import Scoreboard, BoxScoreTraditionalV2
from dependencies import get_db
import json
import psycopg2

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
def get_player_timeline(player: str, game_id: str, db = Depends(get_db)):
    
    # check playbyplay cache for game
    # if not in cache, get play-by-play
    # Get yesterday's date
    
    game_id = "0022300002"
    pbp = playbyplayv2.PlayByPlayV2(game_id)
    play_by_play = pbp.get_data_frames()[0]
    play_by_play.to_sql(name="play_by_play", con=db.bind, if_exists="append", index=False)
    search_term = "SUB:%G. Antetokounmpo%"
    sub_search = "% FOR G. Antetokounmpo%"
    # compute player-timeline and return
    query = pd.read_sql("""
    with neutral_play_by_play as (
        select 
            "EVENTNUM" as event_num,
            coalesce(
                "HOMEDESCRIPTION",
                "NEUTRALDESCRIPTION",
                "VISITORDESCRIPTION"
            ) as play_description,
            "PERIOD" as quarter_num,
            "PCTIMESTRING" as shot_clock,
            "WCTIMESTRING" as real_time,
            "SCORE" as score
        from play_by_play
    ),
    player_sub_times as (
        select 
            *,
            play_description like %(flow_search)s as is_leaving
        from neutral_play_by_play
        where play_description ilike %(player_search)s
    ),
    sub_with_score as (
        select 
            sub.is_leaving,
            sub.quarter_num as sub_quarter,
            sub.shot_clock as sub_time, 
            pbp.shot_clock as score_time, 
            sub.event_num as sub_event_id,
            pbp.event_num as score_event_id,
            pbp.score as score_before_sub
        from player_sub_times sub 
        inner join neutral_play_by_play pbp
            on pbp.event_num < sub.event_num
            and pbp.score is not null
    ),
    score_by_sub as (
        select 
            *,
            row_number() over (
                partition by sub_event_id
                order by score_event_id desc
            ) = 1 as is_sub
        from sub_with_score
    )
    select * from score_by_sub where is_sub
    """, con=db.bind, params={"player_search": search_term, "flow_search": sub_search})
    #res = pd.read_sql("select * from play_by_play limit 7", db.bind)
    return  json.loads(query.to_json(orient="records"))