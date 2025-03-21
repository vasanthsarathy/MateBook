#!/usr/bin/env python3
"""
Test script for the Lichess API integration.
"""

import sys
import logging
from puzzle_extractor.api import LichessAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Test the Lichess API integration."""
    try:
        logger.info("Testing Lichess API integration...")
        
        # Create an API client
        api = LichessAPI()
        
        # Fetch some puzzles
        mate_in = 2
        count = 3
        logger.info(f"Fetching {count} mate-in-{mate_in} puzzles...")
        
        puzzles = api.fetch_puzzles(mate_in=mate_in, count=count)
        
        # Print the puzzles
        logger.info(f"Successfully fetched {len(puzzles)} puzzles")
        for i, puzzle in enumerate(puzzles, 1):
            logger.info(f"Puzzle {i}:")
            logger.info(f"  ID: {puzzle['id']}")
            logger.info(f"  Rating: {puzzle['rating']}")
            logger.info(f"  Moves: {puzzle['moves']}")
            logger.info(f"  URL: {puzzle['url']}")
        
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 