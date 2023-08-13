import re

def extract_response_code(response_str):
    match = re.search(r'\[(\d+)\s*(?:\w+\s*)*\]', response_str)
    if match:
        return int(match.group(1))
    return None
