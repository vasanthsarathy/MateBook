# MateBook - Lichess Puzzle Extractor

A command-line tool to extract chess puzzles from a Lichess puzzle database
and generate a LaTeX document with mate-in-N puzzles.

## Features

- Extract puzzles for mate-in-1, mate-in-2, or any value of N
- Create mixed puzzle sets with different mate-in values
- Arrange puzzles in progressive difficulty order
- Filter puzzles by rating
- Show or hide puzzle ratings
- Generate print-ready PDFs with 4 puzzles per page
- Include solutions on the last page

## Requirements

- Python 3.6 or higher
- LaTeX installation with the `xskak` package for chess diagrams
- Lichess puzzle database CSV file

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/matebook.git
cd matebook
```

2. Download the Lichess puzzle database:

```
mkdir -p puzzles
wget -O puzzles/lichess_db_puzzle.csv https://database.lichess.org/lichess_db_puzzle.csv.zst
unzstd puzzles/lichess_db_puzzle.csv.zst
```

## Usage

### Basic Usage

```
python lichess_puzzle_extractor.py -m 2 -n 10
```

This will generate a document with 10 mate-in-2 puzzles.

### Command-Line Options

| Option                  | Description                                                  |
| ----------------------- | ------------------------------------------------------------ |
| `-n, --number NUMBER`   | Number of puzzles to extract (default: 20)                   |
| `-o, --output OUTPUT`   | Output filename (default: chess_puzzles.tex)                 |
| `-t, --title TITLE`     | Document title (default: based on puzzle type)               |
| `-f, --file FILE`       | Path to the Lichess puzzle database CSV file                 |
| `-r1, --min-rating MIN` | Minimum puzzle rating (optional)                             |
| `-r2, --max-rating MAX` | Maximum puzzle rating (optional)                             |
| `-p, --progressive`     | Arrange puzzles in progressive difficulty (easier to harder) |
| `--hide-ratings`        | Hide puzzle ratings in the output                            |

You must specify one of the following mate puzzle options:

| Option                     | Description                                                         |
| -------------------------- | ------------------------------------------------------------------- |
| `-m, --mate M`             | Generate mate-in-M puzzles (e.g., 2 for mate-in-2)                  |
| `-mx, --mate-mix LIST`     | Generate mixed mate puzzles (e.g., '1,2,3' for a mix)               |
| `-mlt, --mate-less-than N` | Generate all mate puzzles up to N moves (e.g., 3 for mate-in-1,2,3) |

### Example Commands

1. Generate 12 mate-in-1 puzzles:

```
python lichess_puzzle_extractor.py -m 1 -n 12
```

2. Generate a mix of mate-in-1, mate-in-2, and mate-in-3 puzzles:

```
python lichess_puzzle_extractor.py -mx "1,2,3" -n 12
```

3. Generate all mate-in puzzles up to 3 moves:

```
python lichess_puzzle_extractor.py -mlt 3 -n 12
```

4. Generate puzzles in progressive difficulty order:

```
python lichess_puzzle_extractor.py -m 2 -n 12 -p
```

5. Generate puzzles with a rating range:

```
python lichess_puzzle_extractor.py -m 2 -n 12 -r1 1500 -r2 2000
```

6. Hide puzzle ratings:

```
python lichess_puzzle_extractor.py -m 2 -n 12 --hide-ratings
```

### Build Scripts

For convenience, you can use the provided scripts:

**Linux/macOS:**

```
./scripts/run.sh -m 2 -n 12
```

**Windows:**

```
scripts\run.bat -m 2 -n 12
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Lichess.org for providing the open puzzle database
- The xskak LaTeX package for chess diagrams
