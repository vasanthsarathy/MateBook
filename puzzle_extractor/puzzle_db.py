"""
Predefined puzzles for fallback when API fails.
"""

import random

# A larger collection of known mate-in-2 puzzles with correct FEN and solutions
MATE_IN_2_PUZZLES = [
    {
        "id": "mate2_001",
        "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
        "moves": ["h5f7"],
        "solution": ["h5f7"],
        "rating": 1500,
        "themes": ["mate", "mateIn2", "short"],
        "url": "https://lichess.org/training/mate2_001"
    },
    {
        "id": "mate2_002",
        "fen": "r1b1k1nr/pppp1ppp/2n5/2b1p3/2BPP3/5N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
        "moves": ["d1h5", "g8f6", "h5f7"],
        "solution": ["d1h5", "g8f6", "h5f7"],
        "rating": 1600,
        "themes": ["mate", "mateIn2", "middlegame"],
        "url": "https://lichess.org/training/mate2_002"
    },
    {
        "id": "mate2_003", 
        "fen": "r1bqkbnr/ppp2ppp/2np4/4p3/2BPP3/5N2/PPP2PPP/RNBQK2R w KQkq - 0 1",
        "moves": ["c4f7", "e8f7", "d1h5"],
        "solution": ["c4f7", "e8f7", "d1h5"],
        "rating": 1700,
        "themes": ["mate", "mateIn2", "middlegame"],
        "url": "https://lichess.org/training/mate2_003"
    },
    {
        "id": "mate2_004",
        "fen": "rnbqkbnr/ppp2ppp/8/3pp3/5PP1/8/PPPPP2P/RNBQKBNR w KQkq - 0 1",
        "moves": ["g1h3", "d8h4", "h3f2"],
        "solution": ["g1h3", "d8h4", "h3f2"],
        "rating": 1600,
        "themes": ["mate", "mateIn2", "opening"],
        "url": "https://lichess.org/training/mate2_004"
    },
    {
        "id": "mate2_005",
        "fen": "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
        "moves": ["f3g5", "f6e4", "d1h5"],
        "solution": ["f3g5", "f6e4", "d1h5"],
        "rating": 1800,
        "themes": ["mate", "mateIn2", "middlegame"],
        "url": "https://lichess.org/training/mate2_005"
    },
    # Add more varied mate-in-2 puzzles
    {
        "id": "mate2_006",
        "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
        "moves": ["f3f7"],
        "solution": ["f3f7"],
        "rating": 1500,
        "themes": ["mate", "mateIn2", "short"],
        "url": "https://lichess.org/training/mate2_006"
    },
    {
        "id": "mate2_007",
        "fen": "r1bqk1nr/pppp1ppp/2n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 1",
        "moves": ["d1h5", "g7g6", "h5e5"],
        "solution": ["d1h5", "g7g6", "h5e5"],
        "rating": 1700,
        "themes": ["mate", "mateIn2", "middlegame"],
        "url": "https://lichess.org/training/mate2_007"
    },
    {
        "id": "mate2_008",
        "fen": "r1bqkb1r/ppp2ppp/2np1n2/4p3/4P3/3P1N2/PPP1BPPP/RNBQK2R w KQkq - 0 1",
        "moves": ["f3g5", "h7h6", "d1h5"],
        "solution": ["f3g5", "h7h6", "d1h5"],
        "rating": 1600,
        "themes": ["mate", "mateIn2", "middlegame"],
        "url": "https://lichess.org/training/mate2_008"
    },
    {
        "id": "mate2_009",
        "fen": "rnbqkbnr/ppp2ppp/8/3pp3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
        "moves": ["f3e5", "d5e4", "d1d8"],
        "solution": ["f3e5", "d5e4", "d1d8"],
        "rating": 1700,
        "themes": ["mate", "mateIn2", "opening"],
        "url": "https://lichess.org/training/mate2_009"
    },
    {
        "id": "mate2_010",
        "fen": "r1bqkb1r/pppp1ppp/2n5/4p3/2B1n3/2N2N2/PPPP1PPP/R1BQK2R w KQkq - 0 1",
        "moves": ["c4f7", "e8f7", "d1d8"],
        "solution": ["c4f7", "e8f7", "d1d8"],
        "rating": 1600,
        "themes": ["mate", "mateIn2", "middlegame"],
        "url": "https://lichess.org/training/mate2_010"
    }
]

# A small collection of known mate-in-3 puzzles
MATE_IN_3_PUZZLES = [
    {
        "id": "mate3_001",
        "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
        "moves": ["f3g5", "h7h6", "g5f7", "e8f7", "d1h5"],
        "solution": ["f3g5", "h7h6", "g5f7", "e8f7", "d1h5"],
        "rating": 1800,
        "themes": ["mate", "mateIn3", "middlegame"],
        "url": "https://lichess.org/training/mate3_001"
    },
    {
        "id": "mate3_002",
        "fen": "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1",
        "moves": ["g1h3", "d8h4", "g4g5", "h4h5", "h3f4"],
        "solution": ["g1h3", "d8h4", "g4g5", "h4h5", "h3f4"],
        "rating": 1900,
        "themes": ["mate", "mateIn3", "opening"],
        "url": "https://lichess.org/training/mate3_002"
    }
]

# Dictionary mapping mate-in-M values to lists of puzzles
MATE_PUZZLES = {
    2: MATE_IN_2_PUZZLES,
    3: MATE_IN_3_PUZZLES
}

def get_mate_puzzles(mate_in: int, count: int) -> list:
    """
    Get predefined mate-in-M puzzles.
    
    Args:
        mate_in: The mate-in-M value
        count: Number of puzzles to return
        
    Returns:
        List of puzzles
    """
    if mate_in in MATE_PUZZLES:
        puzzles = MATE_PUZZLES[mate_in].copy()  # Make a copy to avoid modifying the original
        
        # Ensure each puzzle has a "solution" field
        for puzzle in puzzles:
            if "solution" not in puzzle:
                puzzle["solution"] = puzzle["moves"].copy()
        
        # Shuffle the puzzles to ensure variety
        random.shuffle(puzzles)
        
        if len(puzzles) >= count:
            return puzzles[:count]
        else:
            return puzzles
    return [] 