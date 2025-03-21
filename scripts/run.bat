@echo off
REM Run script for the Lichess Puzzle Extractor

REM Default values
set MATE_IN=2
set NUM_PUZZLES=10
set OUTPUT_FILE=chess_puzzles.tex
set TITLE=Mate-in-%MATE_IN% Chess Puzzles
set COMPILE_PDF=true
set CSV_FILE=puzzles\lichess_db_puzzle.csv
set MIN_RATING=
set MAX_RATING=

REM Parse command line arguments
:parse_args
if "%~1"=="" goto run
if "%~1"=="-m" (
    set MATE_IN=%~2
    set TITLE=Mate-in-%MATE_IN% Chess Puzzles
    shift
    shift
    goto parse_args
)
if "%~1"=="--mate" (
    set MATE_IN=%~2
    set TITLE=Mate-in-%MATE_IN% Chess Puzzles
    shift
    shift
    goto parse_args
)
if "%~1"=="-n" (
    set NUM_PUZZLES=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--number" (
    set NUM_PUZZLES=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="-o" (
    set OUTPUT_FILE=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--output" (
    set OUTPUT_FILE=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="-t" (
    set TITLE=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--title" (
    set TITLE=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="-f" (
    set CSV_FILE=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--file" (
    set CSV_FILE=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="-r1" (
    set MIN_RATING=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--min-rating" (
    set MIN_RATING=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="-r2" (
    set MAX_RATING=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--max-rating" (
    set MAX_RATING=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--no-pdf" (
    set COMPILE_PDF=false
    shift
    goto parse_args
)
echo Unknown option: %~1
exit /b 1

:run
REM Build the command
set CMD=python lichess_puzzle_extractor.py -m %MATE_IN% -n %NUM_PUZZLES% -o %OUTPUT_FILE% -t "%TITLE%" -f "%CSV_FILE%"

REM Add rating parameters if provided
if defined MIN_RATING (
    set CMD=%CMD% -r1 %MIN_RATING%
)

if defined MAX_RATING (
    set CMD=%CMD% -r2 %MAX_RATING%
)

REM Run the Lichess Puzzle Extractor
echo Extracting %NUM_PUZZLES% mate-in-%MATE_IN% puzzles...
%CMD%

REM Compile to PDF if requested
if "%COMPILE_PDF%"=="true" (
    echo Compiling LaTeX document to PDF...
    pdflatex %OUTPUT_FILE%
    
    REM Run pdflatex twice to ensure references are resolved
    pdflatex %OUTPUT_FILE% > nul
    
    REM Check if PDF was created
    set PDF_FILE=%OUTPUT_FILE:.tex=.pdf%
    if exist "%PDF_FILE%" (
        echo PDF created successfully: %PDF_FILE%
    ) else (
        echo Failed to create PDF
        exit /b 1
    )
)

echo Done! 