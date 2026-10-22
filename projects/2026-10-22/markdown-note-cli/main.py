import argparse
import os
import glob

NOTE_DIR = "notes"

def init_storage():
    if not os.path.exists(NOTE_DIR):
        os.makedirs(NOTE_DIR)

def create_note(title, content):
    init_storage()
    filename = f"{title.lower().replace(' ', '_')}.md"
    filepath = os.path.join(NOTE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n{content}\n")
    return filepath

def search_notes(query):
    init_storage()
    results = []
    for filepath in glob.glob(os.path.join(NOTE_DIR, "*.md")):
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            if query.lower() in text.lower():
                results.append(filepath)
    return results

def main():
    parser = argparse.ArgumentParser(description="Markdown Note CLI")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create", help="Create a new note")
    create_parser.add_argument("--title", required=True, help="Note title")
    create_parser.add_argument("--content", required=True, help="Note content")

    search_parser = subparsers.add_parser("search", help="Search notes")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()
    if args.command == "create":
        path = create_note(args.title, args.content)
        print(f"Note created at {path}")
    elif args.command == "search":
        matches = search_notes(args.query)
        print(f"Found {len(matches)} matching notes:")
        for m in matches:
            print(f" - {m}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()