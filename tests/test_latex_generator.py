"""
Tests for the LaTeX generator module.
"""

import pytest
import os
from puzzle_extractor.latex_generator import LaTeXGenerator

@pytest.fixture
def sample_puzzles():
    """Create sample puzzles for testing."""
    return [
        {
            "id": "puzzle1",
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "moves": ["e2e4", "e7e5"],
            "rating": 1500,
            "themes": ["mate", "middlegame"],
            "solution": ["e2e4", "e7e5"]
        },
        {
            "id": "puzzle2",
            "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2",
            "moves": ["d8h4", "g1f3"],
            "rating": 1600,
            "themes": ["mate", "opening"],
            "solution": ["d8h4", "g1f3"]
        }
    ]

def test_generate_latex_content(sample_puzzles):
    """Test generating LaTeX content."""
    generator = LaTeXGenerator()
    
    latex_content = generator._generate_latex_content(
        puzzles=sample_puzzles,
        title="Test Puzzles",
        mate_in=2
    )
    
    # Check that the LaTeX content contains expected elements
    assert r"\documentclass" in latex_content
    assert r"\title{Test Puzzles}" in latex_content
    assert r"This document contains 2 mate-in-2 puzzles" in latex_content
    
    # Check that both puzzles are included
    assert r"Puzzle 1" in latex_content
    assert r"Puzzle 2" in latex_content
    
    # Check that the FEN positions are included
    assert sample_puzzles[0]["fen"] in latex_content
    assert sample_puzzles[1]["fen"] in latex_content
    
    # Check that the solutions are included
    assert r"\section*{Solutions}" in latex_content
    assert "e2e4, e7e5" in latex_content
    assert "d8h4, g1f3" in latex_content
    
    # Check for correct "to move" text
    assert r"White to move and mate in 2" in latex_content
    assert r"Black to move and mate in 2" in latex_content

def test_generate_document(sample_puzzles, tmp_path):
    """Test generating a LaTeX document file."""
    generator = LaTeXGenerator()
    output_file = os.path.join(tmp_path, "test_puzzles.tex")
    
    generator.generate_document(
        puzzles=sample_puzzles,
        output_file=output_file,
        title="Test Puzzles",
        mate_in=2
    )
    
    # Check that the file was created
    assert os.path.exists(output_file)
    
    # Check the file content
    with open(output_file, "r") as f:
        content = f.read()
        assert r"\documentclass" in content
        assert r"\title{Test Puzzles}" in content
        assert r"Puzzle 1" in content
        assert r"Puzzle 2" in content 