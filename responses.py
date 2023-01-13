def responses(message: str) -> str:

    # Checks if a message ends with quoi
    if ''.join(filter(str.isalpha, message)).lower().endswith("quoi"):
        return "**FEUR**"

    # Return empty string if no condition is checked
    return ''
