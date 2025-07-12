from collections.abc import Sequence

def build_input(name: str, message: str):
    return {
        "type": "input",
        "name": name,
        "message": message
    }

def build_inputs(names: Sequence[str], messages: Sequence[str]):
    if len(names) != len(messages):
        raise ValueError("Expected 'names' and 'messages' to be the same length")
    
    return [build_input(names[i], messages[i]) for i in range(len(names))]