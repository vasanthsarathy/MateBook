#!/bin/bash
# Run script for the Lichess Puzzle Extractor

# Default values
MATE_IN=""
MATE_MIX=""
MATE_LESS_THAN=""
PLY_COUNT=""
PLY_LESS_THAN=""
THEMES=""
MIX_RATIO=""
NUM_PUZZLES=10
OUTPUT_FILE="chess_puzzles.tex"
TITLE=""
COMPILE_PDF=true
CSV_FILE="puzzles/lichess_db_puzzle.csv"
MIN_RATING=""
MAX_RATING=""
PROGRESSIVE=false
HIDE_RATINGS=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -m|--mate)
      MATE_IN="$2"
      if [[ -z "$TITLE" ]]; then
        TITLE="Mate-in-$MATE_IN Chess Puzzles"
      fi
      shift 2
      ;;
    -mx|--mate-mix)
      MATE_MIX="$2"
      if [[ -z "$TITLE" ]]; then
        TITLE="Mixed Mate Chess Puzzles"
      fi
      shift 2
      ;;
    -mlt|--mate-less-than)
      MATE_LESS_THAN="$2"
      if [[ -z "$TITLE" ]]; then
        TITLE="Chess Puzzles (Mate in 1-$MATE_LESS_THAN moves)"
      fi
      shift 2
      ;;
    -k|--ply)
      PLY_COUNT="$2"
      if [[ -z "$TITLE" ]]; then
        TITLE="$PLY_COUNT-Ply Tactical Puzzles"
      fi
      shift 2
      ;;
    -klt|--ply-less-than)
      PLY_LESS_THAN="$2"
      if [[ -z "$TITLE" ]]; then
        TITLE="Tactical Puzzles (2 to $PLY_LESS_THAN ply)"
      fi
      shift 2
      ;;
    -th|--themes)
      THEMES="$2"
      if [[ -z "$TITLE" ]]; then
        TITLE="Tactical Puzzles ($THEMES)"
      fi
      shift 2
      ;;
    --mix-ratio)
      MIX_RATIO="$2"
      shift 2
      ;;
    -p|--progressive)
      PROGRESSIVE=true
      shift
      ;;
    -n|--number)
      NUM_PUZZLES="$2"
      shift 2
      ;;
    -o|--output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    -t|--title)
      TITLE="$2"
      shift 2
      ;;
    -f|--file)
      CSV_FILE="$2"
      shift 2
      ;;
    -r1|--min-rating)
      MIN_RATING="$2"
      shift 2
      ;;
    -r2|--max-rating)
      MAX_RATING="$2"
      shift 2
      ;;
    --no-pdf)
      COMPILE_PDF=false
      shift
      ;;
    --hide-ratings)
      HIDE_RATINGS=true
      shift
      ;;
    *)
      echo "Error: Unknown option: $1"
      echo "Usage: $0 [-m|--mate N] [-mx|--mate-mix LIST] [-mlt|--mate-less-than N] [-k|--ply N] [-klt|--ply-less-than N] [-th|--themes LIST] [options]"
      exit 1
      ;;
  esac
done

# Build the command
CMD="python lichess_puzzle_extractor.py"

# Add the appropriate puzzle type parameter
if [[ -n "$MATE_IN" ]]; then
  CMD="$CMD -m $MATE_IN"
elif [[ -n "$MATE_MIX" ]]; then
  CMD="$CMD -mx '$MATE_MIX'"
elif [[ -n "$MATE_LESS_THAN" ]]; then
  CMD="$CMD -mlt $MATE_LESS_THAN"
elif [[ -n "$PLY_COUNT" ]]; then
  CMD="$CMD -k $PLY_COUNT"
elif [[ -n "$PLY_LESS_THAN" ]]; then
  CMD="$CMD -klt $PLY_LESS_THAN"
elif [[ -n "$THEMES" ]]; then
  CMD="$CMD -th '$THEMES'"
else
  echo "Error: Must specify one of -m, -mx, -mlt, -k, -klt, or -th"
  exit 1
fi

# Add other parameters
CMD="$CMD -n $NUM_PUZZLES -o '$OUTPUT_FILE' -f '$CSV_FILE'"

# Add title if provided
if [[ -n "$TITLE" ]]; then
  CMD="$CMD -t '$TITLE'"
fi

# Add rating parameters if provided
if [[ -n "$MIN_RATING" ]]; then
  CMD="$CMD -r1 $MIN_RATING"
fi

if [[ -n "$MAX_RATING" ]]; then
  CMD="$CMD -r2 $MAX_RATING"
fi

# Add mix ratio if provided
if [[ -n "$MIX_RATIO" ]]; then
  CMD="$CMD --mix-ratio '$MIX_RATIO'"
fi

# Add progressive flag if enabled
if [[ "$PROGRESSIVE" = true ]]; then
  CMD="$CMD -p"
fi

# Add hide-ratings flag if enabled
if [[ "$HIDE_RATINGS" = true ]]; then
  CMD="$CMD --hide-ratings"
fi

# Run the Lichess Puzzle Extractor
echo "Extracting $NUM_PUZZLES puzzles..."
if ! eval $CMD; then
  echo "Error: Failed to extract puzzles"
  exit 1
fi

# Compile to PDF if requested
if [[ "$COMPILE_PDF" = true ]]; then
  echo "Compiling LaTeX document to PDF..."
  if ! pdflatex "$OUTPUT_FILE"; then
    echo "Error: First pdflatex run failed"
    exit 1
  fi
  
  # Run pdflatex twice to ensure references are resolved
  if ! pdflatex "$OUTPUT_FILE" > /dev/null; then
    echo "Error: Second pdflatex run failed"
    exit 1
  fi
  
  # Check if PDF was created
  PDF_FILE="${OUTPUT_FILE%.tex}.pdf"
  if [[ -f "$PDF_FILE" ]]; then
    echo "PDF created successfully: $PDF_FILE"
  else
    echo "Error: Failed to create PDF"
    exit 1
  fi
fi

echo "Done!" 