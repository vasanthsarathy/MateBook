# MateBook: Chess Mate Puzzle Generator

MateBook is a command-line tool that generates collections of mate-in-M puzzles from the Lichess puzzle database. It creates LaTeX documents that can be compiled into printable PDFs, perfect for chess coaches, students, or anyone who wants to practice chess tactics offline.

## Features

- Extract mate-in-M puzzles from a Lichess puzzle database CSV file
- Filter puzzles by mate-in-M value (e.g., mate-in-1, mate-in-2, mate-in-3)
- Filter puzzles by rating range to match player skill level
- Generate a LaTeX document with chess diagrams
- Include solutions on a separate page
- Customizable document title and output filename

## Installation

### Prerequisites

- Python 3.8 or higher
- A LaTeX distribution (e.g., TeX Live, MiKTeX) for compiling the generated LaTeX files
- The following LaTeX packages: xskak, chessboard, geometry, multicol, titlesec, fancyhdr, lastpage, enumitem
- ZStandard compression tools (for decompressing the puzzle database)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/matebook.git
cd matebook
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. For development and testing, install the development dependencies (optional):

```bash
pip install -r requirements-dev.txt
```

4. Make the scripts executable (Linux/macOS):

```bash
chmod +x scripts/*.py
chmod +x scripts/run.sh
```

### Downloading and Extracting the Puzzle Database

1. Download the Lichess puzzle database from [https://database.lichess.org/#puzzles](https://database.lichess.org/#puzzles)
2. Save the file `lichess_db_puzzle.csv.zst` to the `puzzles/` directory

#### Extract the database using ZStandard:

**On Linux/macOS:**

```bash
# Install ZStandard if you don't have it
# Ubuntu/Debian:
sudo apt-get install zstd

# macOS:
brew install zstd

# Extract the database
cd puzzles
pzstd -d lichess_db_puzzle.csv.zst
```

**On Windows:**

1. Install [PeaZip](https://peazip.github.io/) or another tool that supports zstd files, or
2. Install ZStandard for Windows and use the command line:

```bash
cd puzzles
zstd -d lichess_db_puzzle.csv.zst
```

**Note:** The puzzle database is quite large - the compressed file is around 550MB and expands to over 3.5GB when extracted.

## Usage

### Command Line Options

- `-m, --mate`: Mate-in-M puzzles (e.g., 2 for mate-in-2, 3 for mate-in-3, etc.)
- `-n, --number`: Number of puzzles to extract (default: 20)
- `-o, --output`: Output filename (default: "chess_puzzles.tex")
- `-t, --title`: Document title (default: "Mate-in-M Chess Puzzles")
- `-f, --file`: Path to the Lichess puzzle database CSV file (default: "puzzles/lichess_db_puzzle.csv")
- `-r1, --min-rating`: Minimum puzzle rating (optional)
- `-r2, --max-rating`: Maximum puzzle rating (optional)
- `--no-pdf`: Skip PDF compilation (the convenience scripts compile to PDF by default)

### Examples

Extract 5 mate-in-3 puzzles with a custom title:

```bash
python lichess_puzzle_extractor.py -m 3 -n 5 -o mate_in_3.tex -t "5 Challenging Mate-in-3 Puzzles"
```

Extract 10 mate-in-2 puzzles with rating between 1200 and 1800:

```bash
python lichess_puzzle_extractor.py -m 2 -n 10 -o mate_in_2.tex -r1 1200 -r2 1800
```

Use the convenience scripts:

**Linux/macOS:**

```bash
./scripts/run.sh -m 1 -n 5 -o mate_in_1.tex -r1 1200 -r2 2000
```

**Windows:**

```bash
scripts\run.bat -m 1 -n 5 -o mate_in_1.tex -r1 1200 -r2 2000
```

## Puzzle Database Format

The Lichess puzzle database is in CSV format with the following fields:

```
PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl,OpeningTags
```

Example:

```
00sHx,q3k1nr/1pp1nQpp/3p4/1P2p3/4P3/B1PP1b2/B5PP/5K2 b k - 0 17,e8d7 a2e6 d7d8 f7f8,1760,80,83,72,mate mateIn2 middlegame short,https://lichess.org/yyznGmXs/black#34,Italian_Game Italian_Game_Classical_Variation
```

## Troubleshooting

### CSV File Issues

If you're having trouble with the CSV file:

1. Make sure the file exists in the specified path
2. Check that the file has the correct format
3. Try with a smaller number of puzzles first
4. Enable debug logging to see more detailed information about the CSV parsing

### LaTeX Generation Issues

If the LaTeX file is generated but has errors:

1. Check the generated .tex file for syntax errors
2. Make sure you have all the required LaTeX packages installed
3. Try compiling it manually with pdflatex

### Common Errors

- **File Not Found Error**: Make sure the CSV file exists at the specified path
- **LaTeX Compilation Errors**: Make sure you have all the required LaTeX packages installed
- **No Puzzles Found**: The database might not contain puzzles with the specified mate-in-M value

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Lichess](https://lichess.org/) for providing the puzzle database
- [LaTeX](https://www.latex-project.org/) and the [skak](https://ctan.org/pkg/skak) package for chess diagrams
