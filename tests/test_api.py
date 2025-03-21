"""
Tests for the Lichess API module.
"""

import pytest
from unittest.mock import patch, MagicMock
from puzzle_extractor.api import LichessAPI

@pytest.fixture
def mock_response():
    """Create a mock response for the Lichess API."""
    mock = MagicMock()
    mock.text = """{"id":"abcd1234","fen":"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1","moves":["e2e4","e7e5","d1h5","g8f6"],"rating":1500,"themes":["mate","middlegame"]}
{"id":"efgh5678","fen":"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2","moves":["d1h5","g8f6"],"rating":1600,"themes":["mate","opening"]}
{"id":"ijkl9012","fen":"rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2","moves":["d1h5","g8f6","h5f7"],"rating":1700,"themes":["middlegame","advantage"]}"""
    mock.raise_for_status = MagicMock()
    return mock

def test_fetch_puzzles(mock_response):
    """Test fetching puzzles from the Lichess API."""
    with patch('requests.get', return_value=mock_response) as mock_get:
        api = LichessAPI()
        puzzles = api.fetch_puzzles(mate_in=2, count=2)
        
        # Check that the API was called with the correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params']['themes'] == 'mate'
        assert kwargs['params']['max'] == 2
        
        # Check that the puzzles were parsed correctly
        assert len(puzzles) <= 2  # We might get fewer puzzles if they don't match the mate-in-M criteria
        if puzzles:
            assert 'mate' in puzzles[0]['themes']
            assert len(puzzles[0]['moves']) >= 2  # At least mate_in moves

def test_parse_puzzle_line():
    """Test parsing a single line of puzzle data."""
    api = LichessAPI()
    line = '{"id":"abcd1234","fen":"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1","moves":["e2e4","e7e5"],"rating":1500,"themes":["mate","middlegame"]}'
    
    puzzle = api._parse_puzzle_line(line)
    
    assert puzzle['id'] == 'abcd1234'
    assert puzzle['fen'] == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    assert puzzle['moves'] == ['e2e4', 'e7e5']
    assert puzzle['rating'] == 1500
    assert puzzle['themes'] == ['mate', 'middlegame']
    assert puzzle['url'] == 'https://lichess.org/training/abcd1234'

def test_parse_puzzle_line_invalid_json():
    """Test parsing an invalid JSON line."""
    api = LichessAPI()
    line = 'not valid json'
    
    with pytest.raises(ValueError):
        api._parse_puzzle_line(line)

def test_is_mate_in_m():
    """Test checking if a puzzle is a mate-in-M puzzle."""
    api = LichessAPI()
    
    # Mate-in-2 puzzle with 4 moves (2 by player, 2 by opponent)
    puzzle1 = {
        "id": "puzzle1",
        "moves": ["e2e4", "e7e5", "d1h5", "g8f6"],
        "themes": ["mate", "middlegame"]
    }
    assert api._is_mate_in_m(puzzle1, 2)
    
    # Mate-in-2 puzzle with 2 moves (2 by player, 0 by opponent)
    puzzle2 = {
        "id": "puzzle2",
        "moves": ["d1h5", "g8f6"],
        "themes": ["mate", "opening"]
    }
    assert api._is_mate_in_m(puzzle2, 2)
    
    # Not a mate puzzle
    puzzle3 = {
        "id": "puzzle3",
        "moves": ["d1h5", "g8f6", "h5f7"],
        "themes": ["middlegame", "advantage"]
    }
    assert not api._is_mate_in_m(puzzle3, 2)
    
    # Mate puzzle but too many moves for mate-in-2
    puzzle4 = {
        "id": "puzzle4",
        "moves": ["e2e4", "e7e5", "d1h5", "g8f6", "h5f7", "e8e7", "f7e7"],
        "themes": ["mate", "middlegame"]
    }
    assert not api._is_mate_in_m(puzzle4, 2)

def test_flip_fen_turn():
    """Test flipping the turn in a FEN string."""
    api = LichessAPI()
    
    # Test flipping white to black
    fen_w = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen_b = api._flip_fen_turn(fen_w)
    assert fen_b == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
    
    # Test flipping black to white
    fen_b = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
    fen_w = api._flip_fen_turn(fen_b)
    assert fen_w == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    # Test empty string
    assert api._flip_fen_turn("") == ""
    
    # Test invalid FEN
    assert api._flip_fen_turn("invalid") == "invalid" 