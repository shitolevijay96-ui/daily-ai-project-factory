import sys
import re
import requests

def extract_links(content):
    pattern = r'\[.*?\]\((http[s]?://.*?)\)'
    return re.findall(pattern, content)

def check_link(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        return False

def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py <markdown_file>')
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        sys.exit(1)
        
    links = extract_links(content)
    print(f'Found {len(links)} links. Checking...')
    
    for link in links:
        ok = check_link(link)
        status = 'OK' if ok else 'BROKEN'
        print(f'[{status}] {link}')

if __name__ == '__main__':
    main()
