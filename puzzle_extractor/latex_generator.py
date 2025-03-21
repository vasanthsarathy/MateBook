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
        hide_ratings: bool = False,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        progressive: bool = False,
        mate_values: Optional[List[int]] = None
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
            min_rating: Minimum puzzle rating
            max_rating: Maximum puzzle rating
            progressive: Whether puzzles are arranged in progressive difficulty
            mate_values: List of mate-in values for mixed sets
        """
        logger.info(f"Generating LaTeX document with {len(puzzles)} puzzles")
        
        # Create the LaTeX content
        latex_content = self._create_latex_content(
            puzzles, 
            title, 
            mate_in, 
            hide_mate_count, 
            hide_ratings,
            min_rating,
            max_rating,
            progressive,
            mate_values
        )
        
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
        hide_ratings: bool = False,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        progressive: bool = False,
        mate_values: Optional[List[int]] = None
    ) -> str:
        """
        Create the LaTeX content for the document.
        
        Args:
            puzzles: List of puzzles to include in the document
            title: Title of the document
            mate_in: The mate-in-M value for the puzzles (optional for mixed sets)
            hide_mate_count: Whether to hide the mate-in count in the puzzle instructions
            hide_ratings: Whether to hide puzzle ratings in the output
            min_rating: Minimum puzzle rating
            max_rating: Maximum puzzle rating
            progressive: Whether puzzles are arranged in progressive difficulty
            mate_values: List of mate-in values for mixed sets
            
        Returns:
            LaTeX content as a string
        """
        # LaTeX preamble with adjusted settings for 2x2 grid
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
            r"\geometry{margin=0.75in}",
            r"\setlength{\parindent}{0pt}",
            r"\setlength{\parskip}{6pt}",
            r"",
            r"% Increase headheight to avoid fancyhdr warning",
            r"\setlength{\headheight}{15pt}",
            r"",
            r"\pagestyle{fancy}",
            r"\fancyhf{}",
            r"\fancyhead[L]{\slshape " + title + r"}",
            r"\fancyhead[R]{\slshape Page \thepage\ of \pageref{LastPage}}",
            r"\renewcommand{\headrulewidth}{0.4pt}",
            r"\renewcommand{\footrulewidth}{0.4pt}",
            r"",
            r"% Settings for the chess board - increased size",
            r"\setchessboard{boardfontsize=18pt, showmover=false}",
            r"",
            r"% Format subsection titles (puzzle headings)",
            r"\titleformat*{\subsection}{\centering\normalfont\large\bfseries}",
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
                r"\section*{Puzzle Parameters}",
                r"\begin{itemize}",
            ]
            
            # Add mate values information
            if mate_values:
                instructions.append(f"\\item \\textbf{{Mate-in}}: Mixed set containing mate-in " + ", ".join([str(m) for m in mate_values]))
            elif mate_in:
                instructions.append(f"\\item \\textbf{{Mate-in}}: All puzzles are mate-in-{mate_in}")
            
            # Add rating range if provided
            if min_rating and max_rating:
                instructions.append(f"\\item \\textbf{{Rating range}}: {min_rating} to {max_rating}")
            elif min_rating:
                instructions.append(f"\\item \\textbf{{Rating range}}: Minimum {min_rating}")
            elif max_rating:
                instructions.append(f"\\item \\textbf{{Rating range}}: Maximum {max_rating}")
            
            # Add progressive difficulty info if enabled
            if progressive:
                instructions.append(r"\item \textbf{Ordering}: Puzzles are arranged in progressive difficulty (easier to harder)")
            
            # Add rating visibility
            if hide_ratings:
                instructions.append(r"\item \textbf{Ratings}: Puzzle ratings are hidden")
            else:
                instructions.append(r"\item \textbf{Ratings}: Puzzle ratings are shown")
            
            instructions.extend([
                r"\end{itemize}",
                r"",
                r"\newpage",
                r"\section*{Puzzles}",
                r""
            ])
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
        
        # Calculate how many pages we need (4 puzzles per page)
        total_puzzles = len(puzzles)
        pages_needed = (total_puzzles + 3) // 4  # Round up to the nearest multiple of 4
        
        # Add puzzles, 4 per page in a 2x2 grid
        for page in range(pages_needed):
            # Start a new page for each set of 4 puzzles (except the first page)
            if page > 0:
                latex.append(r"\newpage")
            
            # Instead of using tabular environment, we'll manage the layout more directly
            latex.append(r"\vspace*{0.2cm}")  # Add some space at the top
            
            # Process puzzles for this page
            for i in range(4):
                puzzle_index = page * 4 + i
                if puzzle_index >= total_puzzles:
                    break
                    
                # Determine row and column
                row = i // 2  # 0 for top row, 1 for bottom row
                col = i % 2   # 0 for left column, 1 for right column
                
                puzzle = puzzles[puzzle_index]
                puzzle_number = puzzle_index + 1
                
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
                
                # Start a new row if this is the first puzzle in a row
                if col == 0:
                    latex.append(r"\noindent\begin{minipage}{0.49\textwidth}")
                else:
                    latex.append(r"\begin{minipage}{0.49\textwidth}")
                
                # Add the puzzle content
                latex.append(f"\\subsection*{{Puzzle {puzzle_number}}}")
                latex.append(r"\begin{center}")
                latex.append(r"\newgame")
                latex.append(f"\\fenboard{{{fen}}}")
                latex.append(r"\chessboard")
                latex.append(r"\end{center}")
                
                # Start a new center environment for the text
                latex.append(r"\begin{center}")
                latex.append(f"\\textbf{{{instruction_text}}}")
                latex.append(r"\\[0.2cm]")
                
                # Add puzzle ID and rating
                if rating_info:
                    latex.append(f"\\small{{Puzzle ID: {puzzle_id}}} \\quad {rating_info}")
                else:
                    latex.append(f"\\small{{Puzzle ID: {puzzle_id}}}")
                
                latex.append(r"\end{center}")
                latex.append(r"\end{minipage}")
                
                # Handle column spacing
                if col == 0:
                    latex.append(r"\hfill")  # Add horizontal fill between columns
                elif row == 0 and puzzle_index + 1 < total_puzzles:
                    # After the first row, add significant vertical space
                    latex.append(r"\vspace{2.5cm}")  # Slightly reduced vertical space to accommodate larger boards
                
                # End the row if this is the last puzzle in a row or the last puzzle overall
                if col == 1 or puzzle_index + 1 == total_puzzles:
                    latex.append(r"")  # Empty line for clarity
            
            # Add some space at the bottom of the page
            latex.append(r"\vspace*{0.5cm}")
        
        # Add solutions page
        latex.extend([
            r"\newpage",
            r"\section*{Solutions}",
            r"",
            r"\begin{multicols}{2}",
            r"\begin{enumerate}"
        ])
        
        for i, puzzle in enumerate(puzzles, 1):
            solution = puzzle.get("solution", [])
            # Escape the "#" symbol in the solution text
            solution_text = ", ".join([self._escape_chess_notation(move) for move in solution])
            
            latex.append(f"\\item[{i}.] {solution_text}")
        
        latex.extend([
            r"\end{enumerate}",
            r"\end{multicols}",
            r"\end{document}"
        ])
        
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