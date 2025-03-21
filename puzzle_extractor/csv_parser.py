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
        mate_values: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch puzzles from the CSV database.
        
        Args:
            mate_in: The mate-in-M value to filter puzzles (None for any puzzle)
            count: Maximum number of puzzles to return
            min_rating: Minimum puzzle rating (optional)
            max_rating: Maximum puzzle rating (optional)
            mate_values: List of mate-in values for mixed sets (overrides mate_in)
            
        Returns:
            List of puzzle dictionaries
        """
        rating_range_str = ""
        if min_rating is not None and max_rating is not None:
            rating_range_str = f" with rating between {min_rating} and {max_rating}"
        elif min_rating is not None:
            rating_range_str = f" with rating at least {min_rating}"
        elif max_rating is not None:
            rating_range_str = f" with rating at most {max_rating}"
            
        # Use mate_values if provided, otherwise use the single mate_in value
        if mate_values:
            theme_to_match = [f"mateIn{m}" for m in mate_values]
            logger.info(f"Fetching {count} puzzles with mate-in values {mate_values}{rating_range_str} from CSV database")
        else:
            theme_to_match = f"mateIn{mate_in}" if mate_in else None
            logger.info(f"Fetching {count} puzzles{rating_range_str} from CSV database")
        
        puzzles = []
        
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Skip header if it exists (check first row)
                first_row = next(reader, None)
                if first_row and first_row[0].lower() == 'puzzleid':
                    logger.debug("Skipped header row")
                else:
                    # If it wasn't a header, process it as data
                    puzzle = self._parse_row(first_row)
                    if self._matches_criteria(puzzle, theme_to_match, min_rating, max_rating):
                        puzzles.append(puzzle)
                
                # Read rows and convert to puzzle dictionaries
                for row in reader:
                    if not row:  # Skip empty rows
                        continue
                        
                    puzzle = self._parse_row(row)
                    
                    # Check if puzzle matches criteria
                    if self._matches_criteria(puzzle, theme_to_match, min_rating, max_rating):
                        puzzles.append(puzzle)
                    
                    # Break if we have enough puzzles (with some buffer)
                    if len(puzzles) >= count * 3:
                        break
            
            # Shuffle and limit to requested count
            random.shuffle(puzzles)
            puzzles = puzzles[:count * 2]  # Keep some buffer for filtering
            
            logger.info(f"Found {len(puzzles)} puzzles in the database")
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
        theme: Optional[str], 
        min_rating: Optional[int], 
        max_rating: Optional[int]
    ) -> bool:
        """
        Check if a puzzle matches the specified criteria.
        
        Args:
            puzzle: The puzzle to check
            theme: The theme to match (or None)
            min_rating: Minimum rating (or None)
            max_rating: Maximum rating (or None)
            
        Returns:
            True if the puzzle matches all specified criteria, False otherwise
        """
        # Check theme
        if theme and theme not in puzzle.get('themes', []):
            return False
            
        # Check rating range
        rating = puzzle.get('rating', 0)
        if min_rating is not None and rating < min_rating:
            return False
        if max_rating is not None and rating > max_rating:
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