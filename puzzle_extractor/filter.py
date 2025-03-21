"""
Module for filtering and processing chess puzzles.
"""

import logging
import random
import chess
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PuzzleFilter:
    """Filter and process chess puzzles."""
    
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
        logger.info(f"Filtering {len(puzzles)} puzzles for mate-in-{mate_in}")
        
        # Track unique puzzles by FEN to ensure variety
        unique_puzzles = {}
        for puzzle in puzzles:
            puzzle_id = puzzle.get("id", "")
            puzzle_fen = puzzle.get("fen", "")
            moves = puzzle.get("moves", [])
            
            # Skip puzzles without proper FEN, ID, or moves
            if not puzzle_fen or not puzzle_id or not moves:
                continue
                
            # Check if this is a proper mate-in-M puzzle
            themes = puzzle.get("themes", [])
            if not self._is_mate_in_m(themes, mate_in, moves, puzzle_fen):
                continue
            
            # Check rating range if specified
            rating = puzzle.get("rating", 0)
            if min_rating is not None and rating < min_rating:
                continue
            if max_rating is not None and rating > max_rating:
                continue
                
            # Process the puzzle data for proper presentation
            processed_puzzle = self._process_puzzle(puzzle, mate_in)
            
            # Use both ID and FEN as a key to ensure uniqueness
            key = f"{puzzle_id}_{processed_puzzle['fen']}"
            
            if key not in unique_puzzles:
                unique_puzzles[key] = processed_puzzle
        
        mate_puzzles = list(unique_puzzles.values())
        logger.info(f"Found {len(mate_puzzles)} unique mate-in-{mate_in} puzzles within rating range")
        
        # Randomly select up to 'count' puzzles
        if len(mate_puzzles) > count:
            random.shuffle(mate_puzzles)
            mate_puzzles = mate_puzzles[:count]
            
        return mate_puzzles
    
    def _process_puzzle(self, puzzle: Dict[str, Any], mate_in: int) -> Dict[str, Any]:
        """
        Process a puzzle to prepare it for display.
        
        This applies the first move to get the actual starting position,
        and extracts the solution moves.
        
        Args:
            puzzle: The original puzzle data
            mate_in: The mate-in-M value
        
        Returns:
            Processed puzzle with correct FEN and solution
        """
        processed = puzzle.copy()  # Create a copy to avoid modifying the original
        
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
            
            return processed
            
        except Exception as e:
            logger.warning(f"Error processing puzzle: {e}")
            return processed
    
    def _is_mate_in_m(self, themes: List[str], mate_in: int, moves: List[str], fen: str) -> bool:
        """
        Check if a puzzle is a proper mate-in-M puzzle.
        
        Args:
            themes: List of puzzle themes
            mate_in: The mate-in-M value to check for
            moves: List of moves in the solution
            fen: Starting position in FEN format
            
        Returns:
            True if the puzzle is a proper mate-in-M puzzle, False otherwise
        """
        # Basic theme check
        target_theme = f"mateIn{mate_in}"
        if not ("mate" in themes and target_theme in themes):
            return False
        
        # We need at least M*2-1 moves (first move + solution moves)
        if len(moves) < mate_in + 1:
            return False
        
        try:
            # Create a board with the starting position
            board = chess.Board(fen)
            
            # Apply the first move (opponent's move)
            first_move = chess.Move.from_uci(moves[0])
            board.push(first_move)
            
            # Now we're at the position presented to the player
            # Check that the color to move matches with who should deliver mate
            player_to_move = board.turn
            
            # Process the remaining moves (the solution)
            solution_moves = moves[1:]
            moves_to_mate = 0
            
            for i, move_str in enumerate(solution_moves):
                # Check if we're past the expected mate move
                if moves_to_mate > mate_in:
                    return False
                
                move = chess.Move.from_uci(move_str)
                board.push(move)
                moves_to_mate = (i + 2) // 2  # Count player's moves
                
                # Check if this move delivers checkmate
                if board.is_checkmate():
                    # Verify it's exactly mate in M
                    if moves_to_mate == mate_in:
                        # Check it's the player who's delivering mate
                        return board.turn != player_to_move
                    return False
            
            return False  # No checkmate found
            
        except Exception as e:
            logger.warning(f"Error analyzing puzzle: {e}")
            return False
    
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
            # Create a board with the starting position
            board = chess.Board(fen)
            
            # Convert each move to algebraic notation
            algebraic_moves = []
            for move_str in moves:
                # Parse the UCI move
                move = chess.Move.from_uci(move_str)
                
                # Get the SAN (Standard Algebraic Notation)
                san = board.san(move)
                
                # Add to the list
                algebraic_moves.append(san)
                
                # Make the move on the board
                board.push(move)
            
            # Check if the last move should have a checkmate symbol
            if algebraic_moves and board.is_checkmate():
                last_move = algebraic_moves[-1]
                if not last_move.endswith('#'):
                    algebraic_moves[-1] = last_move + '#'
            
            return algebraic_moves
        except Exception as e:
            logger.warning(f"Failed to convert moves to algebraic notation: {e}")
            # Return the original UCI moves if conversion fails
            return moves 