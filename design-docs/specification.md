# Lichess Puzzle Extractor Specification

## Overview

This application extracts N mate-in-M puzzles from the Lichess API within a specified rating range (R1 to R2) and generates a LaTeX document that can be compiled into a printable PDF. The document will display numbered chess puzzles with diagrams and include solutions on the last page.

## Functional Requirements

### 1. Command Line Interface

The application should accept the following command-line parameters:

- `-n, --number`: Number of puzzles to extract (default: 20)
- `-m, --mate`: Mate-in-M puzzles (e.g., 2 for mate-in-2, 3 for mate-in-3, etc.)
- `-r1, --min-rating`: Minimum puzzle rating (default: 1200)
- `-r2, --max-rating`: Maximum puzzle rating (default: 2000)
- `-o, --output`: Output filename (default: "chess_puzzles.tex")
- `-t, --title`: Document title (default: "Mate-in-M Chess Puzzles")
- `-p, --puzzles-per-page`: Number of puzzles per page (default: 4)
- `--theme`: LaTeX chess theme (default: "merida")

Example usage:

```
python lichess_puzzle_extractor.py -n 10 -m 3 -r1 1500 -r2 1800 -o mate_in_3.tex -t "10 Challenging Mate-in-3 Puzzles"
```

### 2. Lichess API Integration

The application should:

- Query the Lichess Puzzle API to find mate-in-M puzzles within the specified rating range
- Use the Lichess Puzzle API database endpoint (https://lichess.org/api/puzzle/db)
- Filter puzzles by mate-in-M and rating range
- Download the minimum required number of puzzles plus a buffer (to ensure unique puzzles)
- Handle API pagination and rate limiting appropriately

### 3. Puzzle Data Processing

The application should:

- Parse and validate the PGN/FEN data from Lichess
- Verify that each puzzle is indeed a mate-in-M puzzle
- Extract the initial position, correct solution moves, and puzzle metadata
- Remove duplicate puzzles
- Randomly select N puzzles from the filtered set if more are available

### 4. LaTeX Document Generation

The application should create a well-formatted LaTeX document with:

- Title page with the specified document title
- Instructions page explaining chess notation and how to use the document
- Puzzle pages containing:
  - Numbered puzzles (1 to N)
  - Chess diagrams showing the initial position
  - Text indicating "White/Black to move and mate in M"
  - Lichess puzzle ID (small font, for reference)
  - Puzzle rating (optional, configurable)
- Solution page(s) with:
  - Each puzzle's number
  - The complete solution in algebraic notation
  - Optional mini diagram of the final position

### 5. LaTeX Document Compilation

The application should:

- Generate a complete, compilable LaTeX document
- Include all necessary LaTeX packages (skak, xskak, chessboard, etc.)
- Automatically compile the LaTeX document to PDF (optional feature)
- Handle any LaTeX special characters or formatting requirements

## Technical Requirements

### 1. Technology Stack

- Programming Language: Python 3.8+
- Libraries:
  - `requests` or `aiohttp` for API calls
  - `python-chess` for chess position verification
  - `jinja2` for LaTeX templating
  - `argparse` for command-line argument parsing
  - `PyLaTeX` (optional) for LaTeX document generation

### 2. API Handling

- Implement proper error handling for API requests
- Respect Lichess API rate limits (avoid getting blocked)
- Include user-agent headers as per Lichess API guidelines
- Support authentication with Lichess API token (optional, for higher rate limits)

### 3. LaTeX Integration

- Use the `skak` or `xskak` LaTeX package for chess diagrams
- Ensure compatibility with standard LaTeX distributions (TeXLive, MiKTeX)
- Generate clean, well-structured LaTeX code
- Include all required LaTeX package dependencies

### 4. Error Handling

- Provide clear error messages for API issues, invalid parameters, etc.
- Implement graceful failure if not enough puzzles match the criteria
- Verify that generated LaTeX compiles without errors

### 5. Performance Considerations

- Implement pagination for large API responses
- Use asynchronous requests for better performance (optional)
- Cache puzzle data to avoid repeated API calls during development

## Data Structures

### Puzzle Object

```python
{
  "id": "string",  # Lichess puzzle ID
  "fen": "string",  # FEN notation of the initial position
  "moves": ["string"],  # List of moves in UCI notation
  "rating": int,  # Puzzle rating
  "themes": ["string"],  # List of puzzle themes including "mate"
  "solution": ["string"],  # List of moves in algebraic notation
  "url": "string"  # URL to the puzzle on Lichess
}
```

### LaTeX Template Structure

- Document Preamble (packages, document class, etc.)
- Title Page Template
- Instructions Page Template
- Puzzle Page Template
- Solutions Page Template

## User Interface

### Command Line Interface

- Clear help text for all command-line options
- Progress indicators during API fetching and LaTeX generation
- Feedback on successful completion or errors

### Output Document

- Clean, consistent design
- Diagrams with clear piece representation
- Numbered puzzles for easy reference
- Well-formatted solutions page
