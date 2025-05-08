# MateBook - Chess Puzzle Generator

A command-line tool to extract chess puzzles from the Lichess database and generate LaTeX documents with tactical and mate-in-N puzzles.

## Features

### Puzzle Types

- Mate-in-N puzzles (1 to N moves)
- Tactical puzzles with specific themes (fork, pin, discovery, etc.)
- Mixed puzzle sets combining different tactical motifs
- Solution length specification (K-ply)

### Filtering & Organization

- Filter puzzles by rating range
- Arrange puzzles in progressive difficulty
- Mix mating and tactical puzzles with custom ratios
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
wget -O puzzles/lichess_db_puzzle.csv.zst https://database.lichess.org/lichess_db_puzzle.csv.zst
unzstd puzzles/lichess_db_puzzle.csv.zst
```

## Usage

### Command-Line Options

#### Basic Options

| Option                  | Description                                    |
| ----------------------- | ---------------------------------------------- |
| `-n, --number NUMBER`   | Number of puzzles to extract (default: 20)     |
| `-o, --output OUTPUT`   | Output filename (default: chess_puzzles.tex)   |
| `-t, --title TITLE`     | Document title (default: based on puzzle type) |
| `-f, --file FILE`       | Path to the Lichess puzzle database CSV file   |
| `-r1, --min-rating MIN` | Minimum puzzle rating (optional)               |
| `-r2, --max-rating MAX` | Maximum puzzle rating (optional)               |
| `-p, --progressive`     | Arrange puzzles in progressive difficulty      |
| `--hide-ratings`        | Hide puzzle ratings in the output              |

#### Puzzle Selection Options

You must specify one of the following puzzle type options:

| Option                     | Description                                       |
| -------------------------- | ------------------------------------------------- |
| `-m, --mate M`             | Generate mate-in-M puzzles                        |
| `-mx, --mate-mix LIST`     | Generate mixed mate puzzles (e.g., '1,2,3')       |
| `-mlt, --mate-less-than N` | Generate all mate puzzles up to N moves           |
| `-k, --ply K`              | Generate K-ply tactical puzzles                   |
| `-th, --themes LIST`       | Generate puzzles with specific themes             |
| `--mix-ratio RATIO`        | Ratio of tactical to mate puzzles (e.g., '70:30') |

#### Available Themes

- `mate`: Checkmate puzzles
- `fork`: Fork tactics
- `pin`: Pin tactics
- `discovery`: Discovered attack
- `skewer`: Skewer tactics
- `sacrifice`: Sacrificial tactics
- `attraction`: Attraction tactics
- `deflection`: Deflection tactics
- `interference`: Interference tactics
- `xRayAttack`: X-ray attack tactics
- `zugzwang`: Zugzwang tactics
- `trappedPiece`: Trapped piece tactics
- `hangingPiece`: Hanging piece tactics

### Example Commands

1. Generate 12 mate-in-2 puzzles:

```bash
python lichess_puzzle_extractor.py -m 2 -n 12
```

2. Generate 15 tactical puzzles with 4-ply solutions:

```bash
python lichess_puzzle_extractor.py -k 4 -n 15
```

3. Generate mixed tactical puzzles with specific themes:

```bash
python lichess_puzzle_extractor.py -th "fork,pin,discovery" -n 20
```

4. Generate a mix of tactical and mate puzzles (70% tactical, 30% mate):

```bash
python lichess_puzzle_extractor.py -th "fork,pin" -mx "2,3" --mix-ratio 70:30 -n 20
```

5. Generate 4-ply tactical puzzles with rating range:

```bash
python lichess_puzzle_extractor.py -k 4 -n 15 -r1 1500 -r2 2000
```

6. Generate progressive difficulty mixed set:

```bash
python lichess_puzzle_extractor.py -th "fork,pin,discovery" -mx "2,3" --mix-ratio 60:40 -n 20 -p
```

### Build Scripts

For convenience, you can use the provided scripts:

**Linux/macOS:**

```bash
./scripts/run.sh -k 4 -th "fork,pin" -n 15
```

**Windows:**

```bash
scripts\run.bat -k 4 -th "fork,pin" -n 15
```

## Understanding Puzzle Themes

### Tactical Themes

- **Fork**: A piece attacks two or more enemy pieces simultaneously
- **Pin**: A piece is unable to move because it would expose a more valuable piece to capture
- **Discovery**: Moving one piece reveals an attack from another piece
- **Skewer**: Similar to a pin, but the more valuable piece is in front
- **Sacrifice**: Giving up material for a tactical advantage
- **Attraction**: Forcing an enemy piece to move to a disadvantageous square
- **Deflection**: Forcing an enemy piece away from a key defensive square
- **Interference**: Blocking an enemy piece's line of attack or defense
- **X-Ray Attack**: Attacking through an intervening piece
- **Zugzwang**: The opponent must make a move that weakens their position
- **Trapped Piece**: A piece has no safe squares to move to
- **Hanging Piece**: A piece that can be captured without immediate compensation

### Solution Length (Ply)

A ply is a single move by one player. For example:

- 2-ply = 1 full move (White + Black)
- 4-ply = 2 full moves
- 6-ply = 3 full moves

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Lichess.org for providing the open puzzle database
- The xskak LaTeX package for chess diagrams
