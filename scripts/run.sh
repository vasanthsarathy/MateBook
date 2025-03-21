#!/bin/bash
# Run script for the Lichess Puzzle Extractor

# Default values
MATE_IN=2
NUM_PUZZLES=10
OUTPUT_FILE="chess_puzzles.tex"
TITLE="Mate-in-$MATE_IN Chess Puzzles"
COMPILE_PDF=true
CSV_FILE="puzzles/lichess_db_puzzle.csv"
MIN_RATING=""
MAX_RATING=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -m|--mate)
      MATE_IN="$2"
      TITLE="Mate-in-$MATE_IN Chess Puzzles"
      shift 2
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
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Build the command
CMD="python lichess_puzzle_extractor.py -m $MATE_IN -n $NUM_PUZZLES -o $OUTPUT_FILE -t \"$TITLE\" -f \"$CSV_FILE\""

# Add rating parameters if provided
if [ -n "$MIN_RATING" ]; then
  CMD="$CMD -r1 $MIN_RATING"
fi

if [ -n "$MAX_RATING" ]; then
  CMD="$CMD -r2 $MAX_RATING"
fi

# Run the Lichess Puzzle Extractor
echo "Extracting $NUM_PUZZLES mate-in-$MATE_IN puzzles..."
eval $CMD

# Compile to PDF if requested
if [ "$COMPILE_PDF" = true ]; then
  echo "Compiling LaTeX document to PDF..."
  pdflatex "$OUTPUT_FILE"
  
  # Run pdflatex twice to ensure references are resolved
  pdflatex "$OUTPUT_FILE" > /dev/null
  
  # Check if PDF was created
  PDF_FILE="${OUTPUT_FILE%.tex}.pdf"
  if [ -f "$PDF_FILE" ]; then
    echo "PDF created successfully: $PDF_FILE"
  else
    echo "Failed to create PDF"
    exit 1
  fi
fi

echo "Done!" 