from collections.abc import Sequence
from typing import Callable, Optional, Tuple, List, Dict, Any
from functools import reduce
from string_utils import snake_to_proper

ValidatorFunc = Callable[[str], bool | str]
FilterFunc = Callable[[str], Any]
PromptValidator = Tuple[Optional[FilterFunc], ValidatorFunc]

def non_empty_validator(name: str) -> PromptValidator:
    """
    Creates a validator that checks if input is non-empty (ignoring whitespace).
    Does not provide a filter function.

    Args:
        name (str): The name of the input field, used in error messages.

    Returns:
        PromptValidator: A tuple with None as the filter function
        and a validator function that returns True if input is valid or an error message string.
    """
    # bool(val.strip()) checks if val is empty aside for whitespace
    validate = lambda val: bool(val.strip()) or f"{snake_to_proper(name)} cannot be empty."
    return (None, validate)

def yes_no_validator(name: str) -> PromptValidator:
    """
    Creates a validator that checks if input is a variant of 'yes' or 'no'.
    Provides a filter function converting 'yes'/'y' to True, others to False.

    Args:
        name (str): The name of the input field, used in error messages.

    Returns:
        PromptValidator: A tuple containing:
            - a filter function converting input to boolean
            - a validator function returning True if input is valid or an error message string.
    """
    validate = lambda val: val.strip().lower() in ["yes", "y", "no", "n"] or f"{snake_to_proper(name)} must be yes, no, y or n"
    # filter output to boolean
    filter_fn = lambda val: val.strip().lower() in ["yes", "y"]
    return (filter_fn, validate)

VALIDATORS = {
    "non_empty": non_empty_validator,
    "y_n": yes_no_validator
}

def build_input(name: str, message: str, validator: str = "non_empty") -> Dict[str, Any]:
    """
    Builds a single input question dictionary compatible with the prompt system.

    Args:
        name (str): The identifier for the input.
        message (str): The prompt message shown to the user.
        validator (str, optional): The key of the validator to use from VALIDATORS.
                                   Defaults to "non_empty".

    Raises:
        ValueError: If the specified validator is not found in VALIDATORS.

    Returns:
        Dict[str, Any]: A dictionary representing a prompt input question, including
                        validation and optional filtering.
    """
    if validator not in VALIDATORS:
        raise ValueError(f"Unknown validator: {validator}")
    
    filter_fn, validate_fn = VALIDATORS[validator](name)

    question = {
        "type": "input",
        "name": name,
        "message": message,
        "validate": validate_fn
    }

    if filter_fn:
        question["filter"] = filter_fn

    return question

def build_inputs(names: Sequence[str], messages: Sequence[str], validators: Optional[Sequence[str]] = None) -> List[Dict[str, Any]]:
    """
    Builds a list of input question dictionaries from sequences of names, messages, and optional validators.

    Args:
        names (Sequence[str]): A sequence of input field identifiers.
        messages (Sequence[str]): A sequence of prompt messages corresponding to each name.
        validators (Optional[Sequence[str]], optional): A sequence of validator keys to apply to each input.
                                                        Must be the same length as names if provided.
                                                        Defaults to None.

    Raises:
        ValueError: If lengths of names and messages do not match, or if validators
                    is provided and its length does not match names.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing prompt input questions.
    """
    if len(names) != len(messages) or (validators and len(names) != len(validators)):
        raise ValueError("Expected 'names' and 'messages' to be the same length, and if validators given it must match the same length too.")
    
    if validators:
        return [build_input(names[i], messages[i], validators[i]) for i in range(len(names))]
    else:
        return [build_input(names[i], messages[i]) for i in range(len(names))]