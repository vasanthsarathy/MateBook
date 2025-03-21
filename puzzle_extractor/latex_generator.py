"""
Module for generating LaTeX documents from chess puzzles.
"""

import logging
import os
import re
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class LaTeXGenerator:
    """Generate LaTeX documents from chess puzzles."""
    
    def generate_document(
        self, 
        puzzles: List[Dict[str, Any]], 
        output_file: str, 
        title: str,
        mate_in: Optional[int] = None,
        hide_mate_count: bool = False,
        hide_ratings: bool = False
    ) -> None:
        """
        Generate a LaTeX document with the given puzzles.
        
        Args:
            puzzles: List of puzzles to include in the document
            output_file: Path to the output LaTeX file
            title: Title of the document
            mate_in: The mate-in-M value for the puzzles (optional for mixed sets)
            hide_mate_count: Whether to hide the mate-in count in the puzzle instructions
            hide_ratings: Whether to hide puzzle ratings in the output
        """
        logger.info(f"Generating LaTeX document with {len(puzzles)} puzzles")
        
        # Create the LaTeX content
        latex_content = self._create_latex_content(puzzles, title, mate_in, hide_mate_count, hide_ratings)
        
        # Write to file
        with open(output_file, "w") as f:
            f.write(latex_content)
        
        logger.info(f"LaTeX document written to {output_file}")
    
    def _create_latex_content(
        self, 
        puzzles: List[Dict[str, Any]], 
        title: str,
        mate_in: Optional[int] = None,
        hide_mate_count: bool = False,
        hide_ratings: bool = False
    ) -> str:
        """
        Create the LaTeX content for the document.
        
        Args:
            puzzles: List of puzzles to include in the document
            title: Title of the document
            mate_in: The mate-in-M value for the puzzles (optional for mixed sets)
            hide_mate_count: Whether to hide the mate-in count in the puzzle instructions
            hide_ratings: Whether to hide puzzle ratings in the output
            
        Returns:
            LaTeX content as a string
        """
        # LaTeX preamble
        latex = [
            r"\documentclass[12pt,a4paper]{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage{xskak}",
            r"\usepackage{chessboard}",
            r"\usepackage{geometry}",
            r"\usepackage{multicol}",
            r"\usepackage{titlesec}",
            r"\usepackage{fancyhdr}",
            r"\usepackage{lastpage}",
            r"\usepackage{enumitem}",
            r"",
            r"\geometry{margin=1in}",
            r"\setlength{\parindent}{0pt}",
            r"\setlength{\parskip}{6pt}",
            r"",
            r"\pagestyle{fancy}",
            r"\fancyhf{}",
            r"\fancyhead[L]{\slshape " + title + r"}",
            r"\fancyhead[R]{\slshape Page \thepage\ of \pageref{LastPage}}",
            r"\renewcommand{\headrulewidth}{0.4pt}",
            r"\renewcommand{\footrulewidth}{0.4pt}",
            r"",
            r"\title{" + title + r"}",
            r"\author{}",
            r"\date{\today}",
            r"",
            r"\begin{document}",
            r"",
            r"\maketitle",
            r"",
        ]
        
        # Update the instructions based on whether we're showing mate-in count
        if hide_mate_count:
            instructions = [
                r"\section*{Instructions}",
                f"This document contains {len(puzzles)} chess puzzles from Lichess.",
                r"For each puzzle, find the sequence of moves that leads to checkmate.",
                r"The exact number of moves required varies for each puzzle.",
                r"Solutions are provided on the last page.",
                r"",
                r"\newpage",
                r"\section*{Puzzles}",
                r""
            ]
        else:
            instructions = [
                r"\section*{Instructions}",
                f"This document contains {len(puzzles)} mate-in-{mate_in} puzzles from Lichess.",
                r"For each puzzle, find the sequence of moves that leads to checkmate in " + str(mate_in) + r" moves.",
                r"Solutions are provided on the last page.",
                r"",
                r"\newpage",
                r"\section*{Puzzles}",
                r""
            ]
        
        latex.extend(instructions)
        
        # Add each puzzle
        for i, puzzle in enumerate(puzzles, 1):
            fen = puzzle.get("fen", "")
            puzzle_id = puzzle.get("id", "")
            
            # Determine if this is a white-to-move or black-to-move position
            is_white_to_move = " w " in fen
            to_move_text = "White" if is_white_to_move else "Black"
            
            # Get player color and rating information
            rating = puzzle.get("rating", "")
            rating_info = f"Rating: {rating}" if (rating and not hide_ratings) else ""
            
            # Determine the mate-in value for this specific puzzle
            puzzle_mate_in = puzzle.get("mate_in", mate_in)
            
            # Create the puzzle instruction based on whether we're showing mate counts
            if hide_mate_count:
                instruction_text = f"{to_move_text} to move and checkmate"
            else:
                instruction_text = f"{to_move_text} to move and checkmate in {puzzle_mate_in}"
            
            puzzle_id_section = f"\\small{{Puzzle ID: {puzzle_id}}}"
            if rating_info:
                puzzle_id_section += f" \\quad {rating_info}"
            
            latex.extend([
                f"\\subsection*{{Puzzle {i}}}",
                r"\begin{center}",
                r"\newgame",
                f"\\fenboard{{{fen}}}",
                r"\chessboard",
                r"\end{center}",
                r"\begin{center}",
                f"\\textbf{{{instruction_text}}}",
                r"",
                puzzle_id_section,
                r"\end{center}",
                r"",
                r"\vspace{1cm}",
                r""
            ])
            
            # Add a page break after every 4 puzzles (except the last page)
            if i % 4 == 0 and i < len(puzzles):
                latex.append(r"\newpage")
        
        # Add solutions page
        latex.extend([
            r"\newpage",
            r"\section*{Solutions}",
            r""
        ])
        
        for i, puzzle in enumerate(puzzles, 1):
            solution = puzzle.get("solution", [])
            # Escape the "#" symbol in the solution text
            solution_text = ", ".join([self._escape_chess_notation(move) for move in solution])
            
            latex.extend([
                f"\\textbf{{Puzzle {i}:}} {solution_text}",
                r"",
            ])
        
        # End the document
        latex.append(r"\end{document}")
        
        return "\n".join(latex)
    
    def _escape_chess_notation(self, move: str) -> str:
        """
        Escape special LaTeX characters in chess notation.
        
        Args:
            move: A chess move in algebraic notation
            
        Returns:
            The move with special characters escaped for LaTeX
        """
        # Replace "#" (checkmate) with "\#" (escaped for LaTeX)
        return move.replace("#", r"\#") 