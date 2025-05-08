"""
Module for handling chess puzzle themes and their configurations.
"""

from typing import List, Tuple, Dict, Optional

# Available tactical themes and their descriptions
TACTICAL_THEMES = {
    "fork": "A piece attacks two or more enemy pieces simultaneously",
    "pin": "A piece is unable to move because it would expose a more valuable piece to capture",
    "discovery": "Moving one piece reveals an attack from another piece",
    "skewer": "Similar to a pin, but the more valuable piece is in front",
    "sacrifice": "Giving up material for a tactical advantage",
    "attraction": "Forcing an enemy piece to move to a disadvantageous square",
    "deflection": "Forcing an enemy piece away from a key defensive square",
    "interference": "Blocking an enemy piece's line of attack or defense",
    "xRayAttack": "Attacking through an intervening piece",
    "zugzwang": "The opponent must make a move that weakens their position",
    "trappedPiece": "A piece has no safe squares to move to",
    "hangingPiece": "A piece that can be captured without immediate compensation"
}

def validate_themes(themes: str) -> List[str]:
    """
    Validate a comma-separated list of themes.
    
    Args:
        themes: Comma-separated list of themes
        
    Returns:
        List of valid themes
        
    Raises:
        ValueError: If any theme is invalid
    """
    theme_list = [t.strip() for t in themes.split(",")]
    invalid_themes = [t for t in theme_list if t not in TACTICAL_THEMES]
    
    if invalid_themes:
        raise ValueError(f"Invalid themes: {', '.join(invalid_themes)}")
    
    return theme_list

def parse_mix_ratio(ratio: str) -> Tuple[int, int]:
    """
    Parse a mix ratio string (e.g., '70:30').
    
    Args:
        ratio: String in format 'X:Y' where X and Y are integers that sum to 100
        
    Returns:
        Tuple of (tactical_ratio, mate_ratio)
        
    Raises:
        ValueError: If the ratio is invalid
    """
    try:
        tactical, mate = map(int, ratio.split(":"))
        if tactical + mate != 100:
            raise ValueError("Ratios must sum to 100")
        return (tactical, mate)
    except Exception as e:
        raise ValueError(f"Invalid mix ratio format. Expected 'X:Y' where X + Y = 100. Error: {str(e)}")

def get_theme_description(theme: str) -> str:
    """
    Get the description of a theme.
    
    Args:
        theme: Theme name
        
    Returns:
        Theme description
    """
    return TACTICAL_THEMES.get(theme, "Unknown theme")

def format_theme_list(themes: List[str]) -> str:
    """
    Format a list of themes for display.
    
    Args:
        themes: List of theme names
        
    Returns:
        Formatted string with theme names and descriptions
    """
    return ", ".join(f"{theme} ({get_theme_description(theme)})" for theme in themes) 