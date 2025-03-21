#!/usr/bin/env python3
"""
Lichess Puzzle Extractor

A command-line tool to extract chess puzzles from a Lichess puzzle database
and generate a LaTeX document.
"""

import argparse
import logging
import sys
import random
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
    
    # Replace the single mate-in argument with a more flexible approach
    mate_group = parser.add_mutually_exclusive_group(required=True)
    mate_group.add_argument(
        "-m", "--mate", 
        type=int,
        help="Mate-in-M puzzles (e.g., 2 for mate-in-2)"
    )
    mate_group.add_argument(
        "-mx", "--mate-mix",
        type=str,
        help="Comma-separated list of mate-in values (e.g., '1,2,3' for a mix of mate-in-1, mate-in-2, and mate-in-3)"
    )
    mate_group.add_argument(
        "-mlt", "--mate-less-than",
        type=int,
        help="All mate-in puzzles less than or equal to this value (e.g., 3 for mate-in-1, mate-in-2, and mate-in-3)"
    )
    
    # Add progressive difficulty option
    parser.add_argument(
        "-p", "--progressive",
        action="store_true",
        help="Arrange puzzles in progressive difficulty (from easier to harder)"
    )
    
    # Add option to hide ratings
    parser.add_argument(
        "--hide-ratings",
        action="store_true",
        help="Hide puzzle ratings in the output"
    )
    
    return parser.parse_args()

def main() -> int:
    """Main entry point for the application."""
    try:
        args = parse_arguments()
        
        # Process mate-in arguments
        mate_values = []
        if args.mate:
            mate_values = [args.mate]
            if not args.title:
                args.title = f"Mate-in-{args.mate} Chess Puzzles"
        elif args.mate_mix:
            try:
                mate_values = [int(m.strip()) for m in args.mate_mix.split(',')]
                if not args.title:
                    args.title = f"Mixed Mate Puzzles ({','.join(str(m) for m in mate_values)})"
            except ValueError:
                logger.error("Invalid mate-mix format. Use comma-separated integers (e.g., '1,2,3')")
                return 1
        elif args.mate_less_than:
            mate_values = list(range(1, args.mate_less_than + 1))
            if not args.title:
                args.title = f"Mate Puzzles (1 to {args.mate_less_than} moves)"
        
        # Initialize components
        csv_parser = PuzzleCSVParser(csv_path=args.file)
        puzzle_filter = PuzzleFilter()
        latex_generator = LaTeXGenerator()
        
        # Fetch and filter puzzles for each mate value
        all_puzzles = []
        puzzles_per_mate = max(1, args.number // len(mate_values))
        
        for mate_in in mate_values:
            # Fetch puzzles from the CSV file
            raw_puzzles = csv_parser.fetch_puzzles(
                mate_in=mate_in,
                count=puzzles_per_mate * 3,  # Get more puzzles for filtering
                min_rating=args.min_rating,
                max_rating=args.max_rating
            )
            
            # Filter puzzles
            filtered_puzzles = puzzle_filter.filter_mate_puzzles(
                puzzles=raw_puzzles,
                mate_in=mate_in,
                count=puzzles_per_mate,
                min_rating=args.min_rating,
                max_rating=args.max_rating
            )
            
            all_puzzles.extend(filtered_puzzles)
            logger.info(f"Found {len(filtered_puzzles)} mate-in-{mate_in} puzzles")
        
        # If we have more puzzles than requested, randomly select the correct number
        if len(all_puzzles) > args.number:
            random.shuffle(all_puzzles)
            all_puzzles = all_puzzles[:args.number]
        
        # Apply progressive difficulty if requested
        if args.progressive and all_puzzles:
            all_puzzles.sort(key=lambda p: p.get('rating', 0))
            logger.info("Puzzles arranged in progressive difficulty")
        
        if not all_puzzles:
            logger.warning(f"No puzzles found matching the criteria")
            return 1
            
        logger.info(f"Generated a collection of {len(all_puzzles)} puzzles")
        
        # Generate LaTeX document
        latex_generator.generate_document(
            puzzles=all_puzzles,
            output_file=args.output,
            title=args.title,
            mate_in=args.mate,
            hide_mate_count=True if (len(mate_values) > 1) else False,
            hide_ratings=args.hide_ratings,
            min_rating=args.min_rating,
            max_rating=args.max_rating,
            progressive=args.progressive,
            mate_values=mate_values
        )
        
        logger.info(f"Successfully generated LaTeX document: {args.output}")
        return 0
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 