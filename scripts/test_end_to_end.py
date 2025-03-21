#!/usr/bin/env python3
"""
End-to-end test script for the Lichess Puzzle Extractor.
"""

import sys
import logging
import os
import subprocess
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
    """Perform an end-to-end test of the Lichess Puzzle Extractor."""
    try:
        logger.info("Starting end-to-end test...")
        
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
        output_file = "end_to_end_test.tex"
        title = "End-to-End Test"
        logger.info(f"Generating LaTeX document with {len(filtered_puzzles)} puzzles...")
        
        latex_generator.generate_document(
            puzzles=filtered_puzzles,
            output_file=output_file,
            title=title,
            mate_in=mate_in
        )
        
        # Check if the file was created
        if not os.path.exists(output_file):
            logger.error(f"Failed to generate LaTeX document: {output_file}")
            return 1
        
        # Try to compile the LaTeX document
        logger.info(f"Attempting to compile the LaTeX document...")
        
        try:
            # Check if pdflatex is available
            subprocess.run(["pdflatex", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Compile the LaTeX document
            result = subprocess.run(
                ["pdflatex", output_file],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            pdf_file = output_file.replace(".tex", ".pdf")
            if os.path.exists(pdf_file):
                logger.info(f"Successfully compiled LaTeX document to PDF: {pdf_file}")
            else:
                logger.warning(f"LaTeX compilation completed but PDF file not found: {pdf_file}")
        except subprocess.CalledProcessError:
            logger.warning("Failed to compile LaTeX document. Is pdflatex installed?")
        except FileNotFoundError:
            logger.warning("pdflatex not found. Skipping LaTeX compilation.")
        
        logger.info("End-to-end test completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 