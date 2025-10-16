import json
from pathlib import Path

FILE_NAME = Path("clients.json")


def _load_data() -> dict:
    """Load JSON data from file, returning an empty dict if missing or invalid."""
    if not FILE_NAME.exists():
        return {}
    try:
        with FILE_NAME.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def _save_data(data: dict):
    """Save the given dictionary to the JSON file."""
    with FILE_NAME.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def change(key: str, data=None, subkey: str = None):
    """
    Add or modify data for a given key.
    If subkey is None, initializes a new client entry with default structure.
    """
    data_from_file = _load_data()

    if subkey is None:
        # Initialize client structure
        data_from_file[key] = {'command': None, 'additional': None}
    else:
        # Modify or add subkey data
        if key not in data_from_file:
            data_from_file[key] = {}
        data_from_file[key][subkey] = data

    _save_data(data_from_file)


def select(key: str, subkey: str):
    """Retrieve the value of a subkey for a given key. Returns -1 if not found."""
    data_from_file = _load_data()
    return data_from_file.get(key, {}).get(subkey, -1)


def remove(key: str):
    """Remove a key from the data file. Returns -1 if key not found."""
    data_from_file = _load_data()

    if key not in data_from_file:
        print("Can't find key")
        return -1

    del data_from_file[key]
    _save_data(data_from_file)
