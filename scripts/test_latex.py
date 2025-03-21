#!/usr/bin/env python3
"""
Test script for the LaTeX generation functionality.
"""

import sys
import logging
import os
from puzzle_extractor.api import LichessAPI
from puzzle_extractor.filter import PuzzleFilter
from puzzle_extractor.latex_generator import LaTeXGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Test the LaTeX generation functionality."""
    try:
        logger.info("Testing LaTeX generation...")
        
        # Create components
        api = LichessAPI()
        puzzle_filter = PuzzleFilter()
        latex_generator = LaTeXGenerator()
        
        # Fetch and filter puzzles
        mate_in = 2
        count = 3
        logger.info(f"Fetching and filtering {count} mate-in-{mate_in} puzzles...")
        
        raw_puzzles = api.fetch_puzzles(mate_in=mate_in, count=count)
        filtered_puzzles = puzzle_filter.filter_mate_puzzles(
            puzzles=raw_puzzles,
            mate_in=mate_in,
            count=count
        )
        
        # Generate LaTeX document
        output_file = "test_latex.tex"
        title = "Test LaTeX Generation"
        logger.info(f"Generating LaTeX document with {len(filtered_puzzles)} puzzles...")
        
        latex_generator.generate_document(
            puzzles=filtered_puzzles,
            output_file=output_file,
            title=title,
            mate_in=mate_in
        )
        
        # Check if the file was created
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            logger.info(f"Successfully generated LaTeX document: {output_file} ({file_size} bytes)")
        else:
            logger.error(f"Failed to generate LaTeX document: {output_file}")
            return 1
        
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 