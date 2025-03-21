#!/usr/bin/env python3
"""
Lichess Puzzle Extractor

A command-line tool to extract chess puzzles from a Lichess puzzle database
and generate a LaTeX document.
"""

import argparse
import logging
import sys
from typing import Dict, List, Any

from puzzle_extractor.csv_parser import PuzzleCSVParser
from puzzle_extractor.filter import PuzzleFilter
from puzzle_extractor.latex_generator import LaTeXGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract chess puzzles from Lichess database and generate a LaTeX document."
    )
    parser.add_argument(
        "-n", "--number", 
        type=int, 
        default=20,
        help="Number of puzzles to extract (default: 20)"
    )
    parser.add_argument(
        "-m", "--mate", 
        type=int, 
        required=True,
        help="Mate-in-M puzzles (e.g., 2 for mate-in-2)"
    )
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default="chess_puzzles.tex",
        help="Output filename (default: chess_puzzles.tex)"
    )
    parser.add_argument(
        "-t", "--title", 
        type=str, 
        default=None,
        help="Document title (default: 'Mate-in-M Chess Puzzles')"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        default="puzzles/lichess_db_puzzle.csv",
        help="Path to the Lichess puzzle database CSV file"
    )
    parser.add_argument(
        "-r1", "--min-rating",
        type=int,
        default=None,
        help="Minimum puzzle rating (optional)"
    )
    parser.add_argument(
        "-r2", "--max-rating",
        type=int,
        default=None,
        help="Maximum puzzle rating (optional)"
    )
    
    return parser.parse_args()

def main() -> int:
    """Main function to run the puzzle extractor."""
    try:
        args = parse_arguments()
        
        # Set default title if not provided
        if args.title is None:
            args.title = f"Mate-in-{args.mate} Chess Puzzles"
        
        rating_range_str = ""
        if args.min_rating is not None and args.max_rating is not None:
            rating_range_str = f" (Rating range: {args.min_rating}-{args.max_rating})"
        elif args.min_rating is not None:
            rating_range_str = f" (Rating: {args.min_rating}+)"
        elif args.max_rating is not None:
            rating_range_str = f" (Rating: up to {args.max_rating})"
        
        logger.info(f"Extracting {args.number} mate-in-{args.mate} puzzles{rating_range_str}...")
        
        # Initialize components
        csv_parser = PuzzleCSVParser(csv_path=args.file)
        puzzle_filter = PuzzleFilter()
        latex_generator = LaTeXGenerator()
        
        # Fetch puzzles from the CSV file
        raw_puzzles = csv_parser.fetch_puzzles(
            mate_in=args.mate,
            count=args.number * 3  # Get more puzzles for filtering
        )
        
        logger.info(f"Fetched {len(raw_puzzles)} puzzles from database")
        
        # Filter puzzles
        filtered_puzzles = puzzle_filter.filter_mate_puzzles(
            puzzles=raw_puzzles,
            mate_in=args.mate,
            count=args.number,
            min_rating=args.min_rating,
            max_rating=args.max_rating
        )
        
        if len(filtered_puzzles) < args.number:
            logger.warning(
                f"Only found {len(filtered_puzzles)} mate-in-{args.mate} puzzles, "
                f"which is less than the requested {args.number}"
            )
        
        # Generate LaTeX document
        latex_generator.generate_document(
            puzzles=filtered_puzzles,
            output_file=args.output,
            title=args.title,
            mate_in=args.mate
        )
        
        logger.info(f"Successfully generated LaTeX document: {args.output}")
        return 0
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 