from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_player_timeline_nocache():
    response = client.get("/player-timeline?player=Giannis&game=MIL@MIA")
    assert response.status_code == 200

def test_player_timeline_cached():
    response = client.get("/player-timeline")
    assert response.status_code == 200

def test_player_timeline_nogame():
    response = client.get("/player-timeline")
    assert response.status_code == 200

def test_player_timeline_noplayer():
    response = client.get("/player-timeline")
    assert response.status_code == 200

def test_player_timeline_noplay():
    """
        Test that the calculation does not fail if the player is never subbed in
    """
    response = client.get("/player-timeline")
    assert response.status_code == 200