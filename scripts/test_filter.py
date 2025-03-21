#!/usr/bin/env python3
"""
Test script for the puzzle filtering functionality.
"""

import sys
import logging
from puzzle_extractor.api import LichessAPI
from puzzle_extractor.filter import PuzzleFilter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Test the puzzle filtering functionality."""
    try:
        logger.info("Testing puzzle filtering...")
        
        # Create API client and filter
        api = LichessAPI()
        puzzle_filter = PuzzleFilter()
        
        # Fetch some puzzles
        mate_in = 2
        count = 10
        logger.info(f"Fetching {count} puzzles...")
        
        raw_puzzles = api.fetch_puzzles(mate_in=mate_in, count=count)
        
        # Filter the puzzles
        logger.info(f"Filtering {len(raw_puzzles)} puzzles for mate-in-{mate_in}...")
        
        filtered_puzzles = puzzle_filter.filter_mate_puzzles(
            puzzles=raw_puzzles,
            mate_in=mate_in,
            count=5
        )
        
        # Print the filtered puzzles
        logger.info(f"Successfully filtered {len(filtered_puzzles)} puzzles")
        for i, puzzle in enumerate(filtered_puzzles, 1):
            logger.info(f"Filtered Puzzle {i}:")
            logger.info(f"  ID: {puzzle['id']}")
            logger.info(f"  Rating: {puzzle['rating']}")
            logger.info(f"  Moves: {puzzle['moves']}")
            logger.info(f"  Solution: {puzzle['solution']}")
        
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 