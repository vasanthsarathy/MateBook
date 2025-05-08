"""
Module for parsing the Lichess puzzle database CSV file.
"""

import csv
import logging
import random
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PuzzleCSVParser:
    """Parse the Lichess puzzle database CSV file."""
    
    def __init__(self, csv_path: str = "puzzles/lichess_db_puzzle.csv"):
        """
        Initialize the parser with the path to the CSV file.
        
        Args:
            csv_path: Path to the Lichess puzzle database CSV file
        """
        self.csv_path = csv_path
        
    def fetch_puzzles(
        self,
        mate_in: Optional[int] = None,
        count: int = 20,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        themes: Optional[List[str]] = None,
        ply_values: Optional[List[int]] = None,
        mate_values: Optional[List[int]] = None,
        tactical_ratio: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch puzzles from the CSV database.
        
        Args:
            mate_in: The mate-in-M value to filter puzzles (None for any puzzle)
            count: Maximum number of puzzles to return
            min_rating: Minimum puzzle rating (optional)
            max_rating: Maximum puzzle rating (optional)
            themes: List of tactical themes to include
            ply_values: List of ply counts for tactical puzzles
            mate_values: List of mate-in values for mixed sets
            tactical_ratio: Percentage of tactical puzzles in mixed sets
            
        Returns:
            List of puzzle dictionaries
        """
        logger.info(f"Fetching {count} puzzles from CSV database")
        
        puzzles = []
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Skip header if it exists
                first_row = next(reader, None)
                if first_row and first_row[0].lower() == 'puzzleid':
                    logger.debug("Skipped header row")
                else:
                    puzzle = self._parse_row(first_row)
                    if self._matches_criteria(puzzle, mate_in, themes, ply_values, min_rating, max_rating):
                        puzzles.append(puzzle)
                
                # Read and filter puzzles
                for row in reader:
                    if not row:  # Skip empty rows
                        continue
                        
                    puzzle = self._parse_row(row)
                    if self._matches_criteria(puzzle, mate_in, themes, ply_values, min_rating, max_rating):
                        puzzles.append(puzzle)
                    
                    # Break if we have enough puzzles (with buffer)
                    if len(puzzles) >= count * 3:
                        break
            
            # Shuffle and select puzzles based on ratios if needed
            if tactical_ratio is not None and mate_values:
                tactical_count = (count * tactical_ratio) // 100
                mate_count = count - tactical_count
                
                # Split puzzles into tactical and mate
                tactical_puzzles = [p for p in puzzles if not any(f"mateIn{m}" in p.get("themes", []) for m in mate_values)]
                mate_puzzles = [p for p in puzzles if any(f"mateIn{m}" in p.get("themes", []) for m in mate_values)]
                
                # Randomly select the required number of each type
                random.shuffle(tactical_puzzles)
                random.shuffle(mate_puzzles)
                
                puzzles = tactical_puzzles[:tactical_count] + mate_puzzles[:mate_count]
            else:
                # Just select the required number of puzzles
                random.shuffle(puzzles)
                puzzles = puzzles[:count]
            
            logger.info(f"Found {len(puzzles)} puzzles matching criteria")
            return puzzles
            
        except FileNotFoundError:
            logger.error(f"CSV file not found: {self.csv_path}")
            return []
        except Exception as e:
            logger.error(f"Error parsing CSV file: {str(e)}")
            return []
    
    def _matches_criteria(
        self,
        puzzle: Dict[str, Any],
        mate_in: Optional[int],
        themes: Optional[List[str]],
        ply_values: Optional[List[int]],
        min_rating: Optional[int],
        max_rating: Optional[int]
    ) -> bool:
        """
        Check if a puzzle matches all specified criteria.
        
        Args:
            puzzle: The puzzle to check
            mate_in: Required mate-in-M value
            themes: Required tactical themes
            ply_values: List of allowed ply counts
            min_rating: Minimum rating
            max_rating: Maximum rating
            
        Returns:
            True if the puzzle matches all criteria
        """
        # Check rating range
        rating = puzzle.get("rating", 0)
        if min_rating is not None and rating < min_rating:
            return False
        if max_rating is not None and rating > max_rating:
            return False
        
        # Check themes
        puzzle_themes = puzzle.get("themes", [])
        if themes:
            if not any(theme in puzzle_themes for theme in themes):
                return False
        
        # Check mate-in value
        if mate_in is not None:
            mate_theme = f"mateIn{mate_in}"
            if mate_theme not in puzzle_themes:
                return False
        
        # Check ply count
        if ply_values is not None:
            moves = puzzle.get("moves", [])
            # The first move is the opponent's move that leads to the position
            # The remaining moves are the solution
            solution_ply_count = len(moves) - 1
            if solution_ply_count not in ply_values:
                return False
        
        return True
        
    def _parse_row(self, row: List[str]) -> Dict[str, Any]:
        """
        Parse a row from the CSV file into a puzzle dictionary.
        
        Args:
            row: A row from the CSV file
            
        Returns:
            A puzzle dictionary
        """
        if len(row) < 8:  # Ensure we have at least the minimum required fields
            logger.warning(f"Invalid row format: {row}")
            return {}
            
        # Extract fields based on the CSV format from the readme
        puzzle_id = row[0]
        fen = row[1]
        moves = row[2].split() if row[2] else []
        rating = int(row[3]) if row[3].isdigit() else 0
        themes = row[7].split() if len(row) > 7 and row[7] else []
        game_url = row[8] if len(row) > 8 else ""
        
        # Create a puzzle dictionary
        puzzle = {
            "id": puzzle_id,
            "fen": fen,
            "moves": moves,
            "solution": moves,  # Will be converted to algebraic later
            "rating": rating,
            "themes": themes,
            "url": game_url
        }
        
        return puzzle 