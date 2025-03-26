import json
from typing import Dict, List, Any

notes:Dict[str, Dict[str, List[str]]] = {}

def file_operation(file_name: str, operation: str, enc: str):
    with open(file_name, operation, encoding=enc) as file:
        if operation == "w" or operation == "a":
            json.dump(notes, file, ensure_ascii=False, indent=4)
        elif operation == "r":
            return json.load(file)
