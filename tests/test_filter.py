"""
Tests for the puzzle filter module.
"""

import pytest
from puzzle_extractor.filter import PuzzleFilter

@pytest.fixture
def sample_puzzles():
    """Create sample puzzles for testing."""
    return [
        {
            "id": "puzzle1",
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "moves": ["e2e4", "e7e5", "d1h5", "g8f6"],
            "rating": 1500,
            "themes": ["mate", "middlegame"]
        },
        {
            "id": "puzzle2",
            "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
            "moves": ["d1h5"],
            "rating": 1600,
            "themes": ["mate", "opening"]
        },
        {
            "id": "puzzle3",
            "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
            "moves": ["d1h5", "g8f6", "h5f7"],
            "rating": 1700,
            "themes": ["middlegame", "advantage"]  # Not a mate puzzle
        }
    ]

def test_filter_mate_puzzles(sample_puzzles):
    """Test filtering mate puzzles."""
    puzzle_filter = PuzzleFilter()
    
    # Filter for mate-in-2 puzzles
    filtered = puzzle_filter.filter_mate_puzzles(
        puzzles=sample_puzzles,
        mate_in=2,
        count=10
    )
    
    # Should only include puzzles with "mate" theme
    assert len(filtered) == 2
    assert filtered[0]["id"] == "puzzle1"
    assert filtered[1]["id"] == "puzzle2"
    
    # Check that solutions were added
    assert "solution" in filtered[0]
    assert "solution" in filtered[1]

def test_filter_mate_puzzles_with_count_limit(sample_puzzles):
    """Test filtering mate puzzles with a count limit."""
    puzzle_filter = PuzzleFilter()
    
    # Filter for mate-in-2 puzzles, but limit to 1
    filtered = puzzle_filter.filter_mate_puzzles(
        puzzles=sample_puzzles,
        mate_in=2,
        count=1
    )
    
    # Should only include 1 puzzle
    assert len(filtered) == 1
    assert filtered[0]["id"] in ["puzzle1", "puzzle2"]

def test_convert_to_algebraic():
    """Test converting UCI moves to algebraic notation."""
    puzzle_filter = PuzzleFilter()
    
    # For Sprint 1, this just returns the UCI moves
    moves = ["e2e4", "e7e5", "d1h5"]
    algebraic = puzzle_filter._convert_to_algebraic(moves)
    
    assert algebraic == moves 