"""
Module for generating LaTeX documents from chess puzzles.
"""

import logging
import os
import re
from typing import List, Dict, Any, Optional

from puzzle_extractor.themes import format_theme_list

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
        mate_values: Optional[List[int]] = None,
        themes: Optional[List[str]] = None,
        ply_values: Optional[List[int]] = None
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
            themes: List of tactical themes to include
            ply_values: List of ply counts for tactical puzzles
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
            mate_values,
            themes,
            ply_values
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
        mate_values: Optional[List[int]] = None,
        themes: Optional[List[str]] = None,
        ply_values: Optional[List[int]] = None
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
            themes: List of tactical themes to include
            ply_values: List of ply counts for tactical puzzles
            
        Returns:
            LaTeX content as a string
        """
        # LaTeX preamble with adjusted settings for 2x2 grid
        latex = [
            r"\documentclass[12pt,a4paper]{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage{xskak}",
            r"\usepackage{chessboard}",
            r"\usepackage[margin=0.75in]{geometry}",  # Portrait mode with standard margins
            r"\usepackage{multicol}",
            r"\usepackage{titlesec}",
            r"\usepackage{fancyhdr}",
            r"\usepackage{lastpage}",
            r"\usepackage{enumitem}",
            r"\usepackage{paracol}",  # For better column control
            r"",
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
            r"% Settings for the chess board",
            r"\setchessboard{",
            r"    boardfontsize=16pt,",  # Increased from 12pt to 16pt
            r"    showmover=true,",
            r"    moverstyle=square,",
            r"    label=false,",
            r"    labelleft=false,",
            r"    labelbottom=false,",
            r"    labeltop=false,",
            r"    labelright=false",
            r"}",
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
        
        # Create instructions based on puzzle type
        instructions = [
            r"\section*{Instructions}",
            f"This document contains {len(puzzles)} chess puzzles from Lichess.",
        ]
        
        if themes:
            instructions.append(f"Each puzzle features one or more of the following tactical themes: {format_theme_list(themes)}.")
        elif ply_values:
            if len(ply_values) == 1:
                instructions.append(f"Each puzzle requires {ply_values[0]//2} moves to reach the winning position.")
            else:
                instructions.append(f"Each puzzle requires between {min(ply_values)//2} and {max(ply_values)//2} moves to reach the winning position.")
        elif mate_values:
            if len(mate_values) == 1:
                instructions.append(f"For each puzzle, find the sequence of moves that leads to checkmate in {mate_values[0]} moves.")
            else:
                instructions.append("For each puzzle, find the sequence of moves that leads to checkmate. The number of moves required varies.")
        
        instructions.extend([
            "Solutions are provided on the last page.",
            "",
            r"\section*{Puzzle Parameters}",
            r"\begin{itemize}[leftmargin=*]",  # Adjust itemize margins
        ])
        
        # Add puzzle type information
        if themes:
            instructions.append(f"\\item \\textbf{{Themes}}: {format_theme_list(themes)}")
        elif ply_values:
            if len(ply_values) == 1:
                instructions.append(f"\\item \\textbf{{Solution length}}: {ply_values[0]//2} moves ({ply_values[0]} ply)")
            else:
                instructions.append(f"\\item \\textbf{{Solution length}}: {min(ply_values)//2} to {max(ply_values)//2} moves ({min(ply_values)} to {max(ply_values)} ply)")
        elif mate_values:
            if len(mate_values) == 1:
                instructions.append(f"\\item \\textbf{{Mate-in}}: All puzzles are mate-in-{mate_values[0]}")
            else:
                instructions.append(f"\\item \\textbf{{Mate-in}}: Mixed set containing mate-in " + ", ".join([str(m) for m in mate_values]))
        
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
            r"",
        ])
        
        latex.extend(instructions)
        
        # Add puzzles in a 2x2 grid using paracol
        latex.extend([
            r"\begin{paracol}{2}",
            r"\setlength{\columnsep}{20pt}",  # Standard column separation
            r"",
        ])
        
        # Process puzzles in pairs for side-by-side layout
        for i in range(0, len(puzzles), 2):
            # First puzzle in the pair
            latex.extend(self._create_puzzle_section(puzzles[i], i + 1, hide_ratings))
            latex.append(r"\switchcolumn")  # Switch to second column
            
            # Second puzzle in the pair (if it exists)
            if i + 1 < len(puzzles):
                latex.extend(self._create_puzzle_section(puzzles[i + 1], i + 2, hide_ratings))
                latex.append(r"\switchcolumn")  # Switch back to first column
            
            latex.append("")  # Add blank line for spacing
        
        latex.extend([
            r"\end{paracol}",
            r"",
            r"\newpage",
            r"",
            r"\section*{Solutions}",
            r"",
        ])
        
        # Add solutions
        for i, puzzle in enumerate(puzzles, 1):
            latex.extend(self._create_solution_section(puzzle, i))
        
        latex.extend([
            r"",
            r"\end{document}",
        ])
        
        return "\n".join(latex)
    
    def _create_puzzle_section(self, puzzle: Dict[str, Any], puzzle_num: int, hide_ratings: bool) -> List[str]:
        """
        Create the LaTeX content for a single puzzle section.
        
        Args:
            puzzle: Puzzle data dictionary
            puzzle_num: Puzzle number
            hide_ratings: Whether to hide puzzle ratings
            
        Returns:
            List of LaTeX lines for the puzzle section
        """
        latex = []
        
        # Add puzzle number and rating
        puzzle_header = f"Puzzle {puzzle_num}"
        if not hide_ratings:
            rating = puzzle.get("rating", 0)
            puzzle_header += f" (Rating: {rating})"
        latex.append(r"\subsection*{" + puzzle_header + r"}")
        
        # Add the chess position
        fen = puzzle.get("fen", "")
        if fen:
            # Set mover based on whose turn it is (2 for White, 1 for Black)
            mover = "2" if "w" in fen else "1"
            latex.extend([
                r"\begin{center}",
                r"\newchessgame",
                r"\fenboard{" + fen + r"}",
                r"\chessboard[showmover=true, boardfontsize=16pt]",  # Increased from 12pt to 16pt
                r"\end{center}"
            ])
        
        latex.append("")  # Add blank line for spacing
        return latex
    
    def _create_solution_section(self, puzzle: Dict[str, Any], puzzle_num: int) -> List[str]:
        """
        Create the LaTeX content for a single puzzle's solution.
        
        Args:
            puzzle: Puzzle data dictionary
            puzzle_num: Puzzle number
            
        Returns:
            List of LaTeX lines for the solution section
        """
        latex = []
        
        # Add puzzle number
        latex.append(f"\\textbf{{Puzzle {puzzle_num}:}}")
        
        # Add solution moves
        solution = puzzle.get("solution", [])
        if solution:
            latex.append(", ".join(self._escape_chess_notation(move) for move in solution))
        
        latex.append("")  # Add blank line for spacing
        return latex
    
    def _escape_chess_notation(self, move: str) -> str:
        """
        Escape special characters in chess notation for LaTeX.
        
        Args:
            move: Chess move in algebraic notation
            
        Returns:
            Escaped move string
        """
        # Escape special LaTeX characters
        move = re.sub(r"([#\$%&_\{\}])", r"\\\1", move)
        return move 