from fastapi import APIRouter

router = APIRouter()

@router.get("/player-timeline")
def get_player_timeline(player: str, game: str):
    # check playbyplay cache for game
    # if not in cache, get play-by-play
    # compute player-timeline and return
    return None