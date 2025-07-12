def snake_to_proper(s: str) -> str:
    """
    Transforms snake_case to Snake Case for use in user outputs

    Args:
        s (str): The snake_case string to transform
    
    Returns:
        str: s transformed to Proper Noun with capitalised first letters and _ changed to a space
    """
    return " ".join(word.capitalize() for word in s.strip().split("_"))

def spaced_to_snake(s: str) -> str:
    """
    Transforms a spaced out string to snake case

    Args:
        s (str): the string to transform e.g. "Project title"
    
    Returns:
        str: s transformed to snake case e.g. "project_title"
    """
    return "_".join(word.lower() for word in s.strip().split())