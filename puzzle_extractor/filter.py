"""
Module for filtering and processing chess puzzles.
"""

import logging
import random
import chess
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PuzzleFilter:
    """Filter and process chess puzzles."""
    
    def filter_puzzles(
        self,
        puzzles: List[Dict[str, Any]],
        count: int,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        themes: Optional[List[str]] = None,
        ply_values: Optional[List[int]] = None,
        mate_values: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Filter puzzles based on various criteria.
        
        Args:
            puzzles: List of puzzles to filter
            count: Maximum number of puzzles to return
            min_rating: Minimum puzzle rating (optional)
            max_rating: Maximum puzzle rating (optional)
            themes: List of tactical themes to include (optional)
            ply_values: List of ply counts for tactical puzzles (optional)
            mate_values: List of mate-in values for mixed sets (optional)
            
        Returns:
            Filtered list of puzzles
        """
        logger.info(f"Filtering {len(puzzles)} puzzles")
        
        # Track unique puzzles by FEN to ensure variety
        unique_puzzles = {}
        for puzzle in puzzles:
            puzzle_id = puzzle.get("id", "")
            puzzle_fen = puzzle.get("fen", "")
            moves = puzzle.get("moves", [])
            
            # Skip puzzles without proper FEN, ID, or moves
            if not puzzle_fen or not puzzle_id or not moves:
                continue
            
            # Check rating range if specified
            rating = puzzle.get("rating", 0)
            if min_rating is not None and rating < min_rating:
                continue
            if max_rating is not None and rating > max_rating:
                continue
            
            # Check themes if specified
            puzzle_themes = puzzle.get("themes", [])
            if themes and not any(theme in puzzle_themes for theme in themes):
                continue
            
            # Check ply count if specified
            # Each ply is a single move by one side
            # The first move in the list is the opponent's move that leads to the position
            # The remaining moves are the solution
            solution_ply_count = len(moves) - 1  # Subtract 1 for the opponent's move
            if ply_values is not None and solution_ply_count not in ply_values:
                continue
            
            # Check mate values if specified
            if mate_values:
                mate_theme_found = False
                for mate_in in mate_values:
                    if f"mateIn{mate_in}" in puzzle_themes:
                        mate_theme_found = True
                        break
                if not mate_theme_found:
                    continue
            
            # Process the puzzle data for proper presentation
            processed_puzzle = self._process_puzzle(puzzle)
            
            # Use both ID and FEN as a key to ensure uniqueness
            key = f"{puzzle_id}_{processed_puzzle['fen']}"
            
            if key not in unique_puzzles:
                unique_puzzles[key] = processed_puzzle
        
        filtered_puzzles = list(unique_puzzles.values())
        logger.info(f"Found {len(filtered_puzzles)} unique puzzles matching criteria")
        
        # Randomly select up to 'count' puzzles
        if len(filtered_puzzles) > count:
            random.shuffle(filtered_puzzles)
            filtered_puzzles = filtered_puzzles[:count]
            
        return filtered_puzzles
    
    def filter_mate_puzzles(
        self, 
        puzzles: List[Dict[str, Any]], 
        mate_in: int, 
        count: int,
        min_rating: int = None,
        max_rating: int = None
    ) -> List[Dict[str, Any]]:
        """
        Filter puzzles to find mate-in-M puzzles within a rating range.
        
        Args:
            puzzles: List of puzzles to filter
            mate_in: The mate-in-M value to filter for
            count: Maximum number of puzzles to return
            min_rating: Minimum puzzle rating (optional)
            max_rating: Maximum puzzle rating (optional)
            
        Returns:
            Filtered list of puzzles
        """
        return self.filter_puzzles(
            puzzles=puzzles,
            count=count,
            min_rating=min_rating,
            max_rating=max_rating,
            mate_values=[mate_in]
        )
    
    def _process_puzzle(self, puzzle: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a puzzle to prepare it for display.
        
        This applies the first move to get the actual starting position,
        and extracts the solution moves.
        
        Args:
            puzzle: The original puzzle data
        
        Returns:
            Processed puzzle with correct FEN and solution
        """
        processed = puzzle.copy()  # Create a copy to avoid modifying the original
        
        # Extract mate-in value if present
        themes = puzzle.get("themes", [])
        for theme in themes:
            if theme.startswith("mateIn"):
                processed["mate_in"] = int(theme[6:])
                break
        
        fen = puzzle.get("fen", "")
        moves = puzzle.get("moves", [])
        
        if not fen or not moves:
            return processed
        
        try:
            # Create a board with the original FEN
            board = chess.Board(fen)
            
            # Apply the first move (opponent's move) to get the actual starting position
            if len(moves) > 0:
                first_move = chess.Move.from_uci(moves[0])
                board.push(first_move)
            
            # The new FEN represents the actual position shown to the player
            processed["fen"] = board.fen()
            
            # The solution starts from the second move
            player_moves = moves[1:]
            
            # Convert solution moves to algebraic notation
            processed["solution"] = self._convert_to_algebraic(player_moves, board.fen())
            
            # Store the ply count (number of moves in the solution)
            processed["ply_count"] = len(player_moves)
            
            return processed
            
        except Exception as e:
            logger.warning(f"Error processing puzzle: {e}")
            return processed
    
    def _convert_to_algebraic(self, moves: List[str], fen: str) -> List[str]:
        """
        Convert UCI moves to algebraic notation.
        
        Args:
            moves: List of moves in UCI format
            fen: The starting position in FEN format
            
        Returns:
            List of moves in algebraic notation
        """
        try:
            board = chess.Board(fen)
            algebraic_moves = []
            
            for move_str in moves:
                move = chess.Move.from_uci(move_str)
                algebraic_moves.append(board.san(move))
                board.push(move)
            
            return algebraic_moves
            
        except Exception as e:
            logger.warning(f"Error converting moves to algebraic notation: {e}")
            return moves  # Return original moves if conversion fails 