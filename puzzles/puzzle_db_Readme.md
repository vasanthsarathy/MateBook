This file was last updated on 2025-03-01.

## Format

Puzzles are formatted as standard CSV. The fields are as follows:

PuzzleId,FEN,Moves,Rating,RatingDeviation,Popularity,NbPlays,Themes,GameUrl,OpeningTags

## Sample

00sHx,q3k1nr/1pp1nQpp/3p4/1P2p3/4P3/B1PP1b2/B5PP/5K2 b k - 0 17,e8d7 a2e6 d7d8 f7f8,1760,80,83,72,mate mateIn2 middlegame short,https://lichess.org/yyznGmXs/black#34,Italian_Game Italian_Game_Classical_Variation
00sJ9,r3r1k1/p4ppp/2p2n2/1p6/3P1qb1/2NQR3/PPB2PP1/R1B3K1 w - - 5 18,e3g3 e8e1 g1h2 e1c1 a1c1 f4h6 h2g1 h6c1,2671,105,87,325,advantage attraction fork middlegame sacrifice veryLong,https://lichess.org/gyFeQsOE#35,French_Defense French_Defense_Exchange_Variation
00sJb,Q1b2r1k/p2np2p/5bp1/q7/5P2/4B3/PPP3PP/2KR1B1R w - - 1 17,d1d7 a5e1 d7d1 e1e3 c1b1 e3b6,2235,76,97,64,advantage fork long,https://lichess.org/kiuvTFoE#33,Sicilian_Defense Sicilian_Defense_Dragon_Variation
00sO1,1k1r4/pp3pp1/2p1p3/4b3/P3n1P1/8/KPP2PN1/3rBR1R b - - 2 31,b8c7 e1a5 b7b6 f1d1,998,85,94,293,advantage discoveredAttack master middlegame short,https://lichess.org/vsfFkG0s/black#62,
Notes
Moves are in UCI format. Use a chess library to convert them to SAN, for display.

All player moves of the solution are "only moves". I.e. playing any other move would considerably worsen the player position. An exception is made for mates in one: there can be several. Any move that checkmates should win the puzzle.

FEN is the position before the opponent makes their move.
The position to present to the player is after applying the first move to that FEN.
The second move is the beginning of the solution.

Popularity is a number between 100 (best) and -100 (worst).
It is calculated as 100 \* (upvotes - downvotes)/(upvotes + downvotes), although votes are weigthed by various factors such as whether the puzzle was solved successfully or the solver's puzzle rating in comparison to the puzzle's.

You can find a list of themes, their names and descriptions, in this file.

The OpeningTags field is only set for puzzles starting before move 20. Here's the list of possible openings.

Generating these chess puzzles took more than 50 years of CPU time.
We went through 300,000,000 analysed games from the Lichess database, and re-analyzed interesting positions with Stockfish 12/13/14/15 NNUE at 40 meganodes. The resulting puzzles were then automatically tagged. To determine the rating, each attempt to solve is considered as a Glicko2 rated game between the player and the puzzle. Finally, player votes refine the tags and define popularity.
