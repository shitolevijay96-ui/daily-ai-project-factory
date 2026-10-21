import sys
import json

REQUIRED_KEYS = {
    'host': str,
    'port': int,
    'debug': bool,
    'allowed_hosts': list
}

def validate_config(data):
    errors = []
    for key, expected_type in REQUIRED_KEYS.items():
        if key not in data:
            errors.append(f'Missing required key: "{key}"')
        elif not isinstance(data[key], expected_type):
            errors.append(f'Invalid type for "{key}": expected {expected_type.__name__}, got {type(data[key]).__name__}')
    return errors

def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py <config_json_file>')
        sys.exit(1)
        
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f'Failed to parse JSON: {e}')
        sys.exit(1)
        
    errors = validate_config(data)
    if errors:
        print('Configuration validation failed:')
        for err in errors:
            print(f' - {err}')
        sys.exit(1)
    else:
        print('Configuration is valid!')

if __name__ == '__main__':
    main()
