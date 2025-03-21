"""
Module for interacting with the Lichess API to fetch puzzles.
"""

import logging
import requests
import time
from typing import List, Dict, Any
from puzzle_extractor.puzzle_db import get_mate_puzzles

logger = logging.getLogger(__name__)

class LichessAPI:
    """Client for interacting with the Lichess API."""
    
    def __init__(self, base_url: str = "https://lichess.org/api"):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Lichess Puzzle Extractor (https://github.com/yourusername/lichess-puzzle-extractor)"
        }
    
    def fetch_puzzles(self, mate_in: int, count: int = 20) -> List[Dict[str, Any]]:
        """
        Fetch puzzles from Lichess API.
        
        Args:
            mate_in: The mate-in-M value to filter puzzles
            count: Number of puzzles to fetch
            
        Returns:
            List of puzzle dictionaries
        """
        logger.info(f"Fetching {count} mate-in-{mate_in} puzzles...")
        
        # Try the Lichess API first
        api_puzzles = self._fetch_puzzles_from_api(mate_in, count)
        
        # If we got enough puzzles from the API, return them
        if len(api_puzzles) >= count:
            return api_puzzles[:count]
        
        # If we didn't get enough puzzles from the API, use our fallback database
        logger.warning(f"Only found {len(api_puzzles)} puzzles from API, using fallback database")
        fallback_puzzles = get_mate_puzzles(mate_in, count - len(api_puzzles))
        
        # Add the fallback puzzles to our list
        puzzles = api_puzzles + fallback_puzzles
        
        # If we still don't have enough puzzles, log a warning
        if len(puzzles) < count:
            logger.warning(f"Only found {len(puzzles)} mate-in-{mate_in} puzzles (including fallback), "
                          f"which is less than the requested {count}")
        
        logger.info(f"Returning {len(puzzles)} puzzles ({len(api_puzzles)} from API, "
                   f"{len(fallback_puzzles)} from fallback database)")
        
        return puzzles[:count]  # Return only the requested count
    
    def _fetch_puzzles_from_api(self, mate_in: int, count: int) -> List[Dict[str, Any]]:
        """
        Try to fetch puzzles from the Lichess API.
        
        Args:
            mate_in: The mate-in-M value to filter puzzles
            count: Number of puzzles to fetch
            
        Returns:
            List of puzzle dictionaries
        """
        puzzles = []
        try:
            # Try the puzzle/daily endpoint
            endpoint = f"{self.base_url}/puzzle/daily"
            
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            
            puzzle_data = response.json()
            logger.debug(f"Got puzzle data from daily endpoint: {puzzle_data.get('puzzle', {}).get('id', 'unknown')}")
            
            # Extract the puzzle, but don't add it if we're looking for mate puzzles (since daily puzzles are rarely mate puzzles)
            if mate_in is None or self._is_mate_in_m(self._convert_puzzle_format(puzzle_data), mate_in):
                puzzles.append(self._convert_puzzle_format(puzzle_data))
        except Exception as e:
            logger.error(f"Error fetching puzzles from daily endpoint: {str(e)}")
        
        return puzzles
    
    def _convert_puzzle_format(self, puzzle_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert the puzzle data from the API into our internal format.
        
        Args:
            puzzle_data: Puzzle data from the API
            
        Returns:
            Puzzle in our internal format
        """
        # Extract puzzle and game data
        puzzle = puzzle_data.get("puzzle", {})
        game = puzzle_data.get("game", {})
        
        # The real FEN for the puzzle position needs to be constructed
        # from the game FEN and puzzle position data
        game_fen = game.get("fen", "")
        
        # Debug the raw puzzle data to understand its structure
        logger.debug(f"Raw puzzle data: {puzzle_data}")
        
        # In the Lichess API, the puzzle position is often specified by:
        # 1. A base game FEN (game.fen)
        # 2. A list of moves to get to the puzzle position (game.moves or puzzle.line)
        # We need to extract the proper FEN for the puzzle starting position
        
        # Check for puzzle line or puzzle position fields
        moves_to_position = []
        
        # Try different possible fields where the position moves might be stored
        if "line" in puzzle:
            moves_to_position = puzzle.get("line", "").split()
        elif "moves" in game:
            moves_to_position = game.get("moves", "").split()
        
        # Try to get the puzzle position directly if available
        position_fen = ""
        if "fen" in puzzle:
            position_fen = puzzle.get("fen", "")
        
        logger.debug(f"Game FEN: {game_fen}")
        logger.debug(f"Moves to position: {moves_to_position}")
        logger.debug(f"Position FEN (if available): {position_fen}")
        
        # Use the position FEN if available, otherwise fall back to the game FEN
        fen = position_fen if position_fen else game_fen
        
        # If we still don't have a valid position, log a warning
        if not fen or fen == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
            logger.warning(f"Could not determine proper puzzle position for puzzle {puzzle.get('id', 'unknown')}")
            
            # Let's try to extract it from the game PGN if available
            pgn = game.get("pgn", "")
            if pgn:
                logger.debug(f"Game PGN: {pgn}")
                # TODO: If needed, implement PGN parsing to extract position
        
        # DEBUG: Print the full puzzle data to examine its structure
        import json
        logger.debug(f"Full puzzle data: {json.dumps(puzzle_data, indent=2)}")
        
        # Convert to our internal format
        return {
            "id": puzzle.get("id", ""),
            "fen": fen,
            "moves": puzzle.get("solution", []),
            "rating": puzzle.get("rating", 0),
            "themes": puzzle.get("themes", []),
            "url": f"https://lichess.org/training/{puzzle.get('id', '')}"
        }
    
    def _is_mate_in_m(self, puzzle: Dict[str, Any], mate_in: int) -> bool:
        """
        Check if a puzzle is a mate-in-M puzzle.
        
        Args:
            puzzle: Puzzle dictionary
            mate_in: The mate-in-M value to check for
            
        Returns:
            True if the puzzle is a mate-in-M puzzle, False otherwise
        """
        # Check if the puzzle has a theme that indicates it's a mate puzzle
        themes = puzzle.get("themes", [])
        if not any(theme in themes for theme in ["mate", "mateIn1", "mateIn2", "mateIn3", "mateIn4", "mateIn5"]):
            return False
        
        # For mate-in-M puzzles, the solution should have approximately 2*M-1 moves
        # (M moves by the player, M-1 moves by the opponent)
        # We'll allow some flexibility in the number of moves
        moves = puzzle.get("moves", [])
        expected_min_moves = mate_in
        expected_max_moves = 2 * mate_in
        
        return expected_min_moves <= len(moves) <= expected_max_moves
    
    def _flip_fen_turn(self, fen: str) -> str:
        """
        Flip the turn in a FEN string.
        
        Args:
            fen: FEN string
            
        Returns:
            FEN string with flipped turn
        """
        if not fen:
            return fen
            
        parts = fen.split()
        if len(parts) < 2:
            return fen
            
        # Flip the turn (w -> b, b -> w)
        parts[1] = "b" if parts[1] == "w" else "w"
        
        return " ".join(parts) 