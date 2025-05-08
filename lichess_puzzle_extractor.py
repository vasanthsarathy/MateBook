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
from typing import Dict, List, Any, Optional, Tuple

from puzzle_extractor.csv_parser import PuzzleCSVParser
from puzzle_extractor.filter import PuzzleFilter
from puzzle_extractor.latex_generator import LaTeXGenerator
from puzzle_extractor.themes import validate_themes, parse_mix_ratio, TACTICAL_THEMES

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
        help="Document title (default: based on puzzle type)"
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
    
    # Puzzle type selection group (mutually exclusive)
    puzzle_group = parser.add_mutually_exclusive_group(required=True)
    
    # Mate puzzle options
    puzzle_group.add_argument(
        "-m", "--mate", 
        type=int,
        help="Mate-in-M puzzles (e.g., 2 for mate-in-2)"
    )
    puzzle_group.add_argument(
        "-mx", "--mate-mix",
        type=str,
        help="Comma-separated list of mate-in values (e.g., '1,2,3')"
    )
    puzzle_group.add_argument(
        "-mlt", "--mate-less-than",
        type=int,
        help="All mate-in puzzles less than or equal to this value"
    )
    
    # Tactical puzzle options
    puzzle_group.add_argument(
        "-k", "--ply",
        type=int,
        help="Generate K-ply tactical puzzles"
    )
    puzzle_group.add_argument(
        "-klt", "--ply-less-than",
        type=int,
        help="Generate tactical puzzles with ply count less than or equal to this value"
    )
    puzzle_group.add_argument(
        "-th", "--themes",
        type=str,
        help=f"Generate puzzles with specific themes (comma-separated). Available themes: {', '.join(TACTICAL_THEMES.keys())}"
    )
    
    # Mix ratio for combined tactical and mate puzzles
    parser.add_argument(
        "--mix-ratio",
        type=str,
        help="Ratio of tactical to mate puzzles (e.g., '70:30')"
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

def process_puzzle_options(args: argparse.Namespace) -> Tuple[List[int], Optional[List[str]], Optional[List[int]], Optional[Tuple[int, int]]]:
    """
    Process puzzle selection options from command line arguments.
    
    Args:
        args: Command line arguments
        
    Returns:
        Tuple of (mate_values, themes, ply_values, mix_ratio)
    """
    mate_values = []
    themes = None
    ply_values = None
    mix_ratio = None
    
    # Process mate puzzle options
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
            raise ValueError("Invalid mate-mix format. Use comma-separated integers (e.g., '1,2,3')")
    elif args.mate_less_than:
        mate_values = list(range(1, args.mate_less_than + 1))
        if not args.title:
            args.title = f"Mate Puzzles (1 to {args.mate_less_than} moves)"
    elif args.ply:
        ply_values = [args.ply]
        if not args.title:
            args.title = f"{args.ply}-Ply Tactical Puzzles"
    elif args.ply_less_than:
        # For ply count, we want odd numbers since each full move is 2 ply
        # and we want to include the last move
        ply_values = list(range(1, args.ply_less_than + 1))
        if not args.title:
            args.title = f"Tactical Puzzles (1 to {args.ply_less_than} ply)"
    elif args.themes:
        themes = validate_themes(args.themes)
        if not args.title:
            args.title = f"Tactical Puzzles ({', '.join(themes)})"
    
    # Process mix ratio if provided
    if args.mix_ratio:
        mix_ratio = parse_mix_ratio(args.mix_ratio)
        if not args.title:
            tactical_ratio, mate_ratio = mix_ratio
            args.title = f"Mixed Puzzles ({tactical_ratio}% Tactical, {mate_ratio}% Mate)"
    
    return mate_values, themes, ply_values, mix_ratio

def main() -> int:
    """Main entry point for the application."""
    try:
        args = parse_arguments()
        
        # Process puzzle options
        mate_values, themes, ply_values, mix_ratio = process_puzzle_options(args)
        
        # Initialize components
        csv_parser = PuzzleCSVParser(csv_path=args.file)
        puzzle_filter = PuzzleFilter()
        latex_generator = LaTeXGenerator()
        
        # Fetch puzzles based on the selected options
        tactical_ratio = mix_ratio[0] if mix_ratio else None
        puzzles = puzzle_filter.filter_puzzles(
            puzzles=csv_parser.fetch_puzzles(
                count=args.number * 3,  # Get more puzzles for filtering
                min_rating=args.min_rating,
                max_rating=args.max_rating,
                themes=themes,
                ply_values=ply_values,
                mate_values=mate_values,
                tactical_ratio=tactical_ratio
            ),
            count=args.number,
            min_rating=args.min_rating,
            max_rating=args.max_rating,
            themes=themes,
            ply_values=ply_values,
            mate_values=mate_values
        )
        
        # Apply progressive difficulty if requested
        if args.progressive and puzzles:
            puzzles.sort(key=lambda p: p.get('rating', 0))
            logger.info("Puzzles arranged in progressive difficulty")
        
        if not puzzles:
            logger.warning(f"No puzzles found matching the criteria")
            return 1
            
        logger.info(f"Generated a collection of {len(puzzles)} puzzles")
        
        # Generate LaTeX document
        latex_generator.generate_document(
            puzzles=puzzles,
            output_file=args.output,
            title=args.title,
            mate_in=args.mate if args.mate else None,
            hide_mate_count=True if (len(mate_values) > 1) else False,
            hide_ratings=args.hide_ratings,
            min_rating=args.min_rating,
            max_rating=args.max_rating,
            progressive=args.progressive,
            mate_values=mate_values,
            themes=themes,
            ply_values=ply_values
        )
        
        logger.info(f"Successfully generated LaTeX document: {args.output}")
        return 0
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 