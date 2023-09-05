import re

def extract_response_code(response):
    """
    Extract the response code from a string containing a response.

    Args:
        response (str): The response string to extract the code from.
    Returns:
        int or None: The extracted response code as an integer, or None if not found
    """
    match = re.search(r'\[(\d+)\s*(?:\w+\s*)*\]', str(response))
    if match:
        return int(match.group(1))
    return None