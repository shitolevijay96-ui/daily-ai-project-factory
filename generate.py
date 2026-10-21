import os
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_KEY = os.environ["GEMINI_API_KEY"]
MODEL = "gemini-2.5-flash-lite"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
ROOT = Path("projects") / TODAY

PROMPT = """
Generate exactly 2 original Python projects.
Each must have a unique name and at least 3 files:
README.md, main.py, and test_main.py.
Return only JSON:
{"projects":[{"name":"project-one","files":[
{"path":"README.md","content":"..."},
{"path":"main.py","content":"..."},
{"path":"test_main.py","content":"..."}
]}]}
Include two projects in the projects array.
Use useful real-world ideas and setup instructions.
"""

def main():
    if ROOT.exists():
        raise RuntimeError("Today's projects already exist.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": PROMPT}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "maxOutputTokens": 12000
        }
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": API_KEY
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=240) as response:
        result = json.loads(response.read())

    data = json.loads(result["candidates"][0]["content"]["parts"][0]["text"])
    projects = data["projects"]

    if len(projects) != 2:
        raise ValueError("Expected exactly two projects.")

    ROOT.mkdir(parents=True)

    for project in projects:
        name = project["name"]
        if not name.replace("-", "").isalnum():
            raise ValueError("Invalid project name.")

        folder = ROOT / name
        for item in project["files"]:
            path = Path(item["path"])
            if path.is_absolute() or ".." in path.parts:
                raise ValueError("Unsafe path.")

            target = folder / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(item["content"], encoding="utf-8")

        print("Created:", folder)

if __name__ == "__main__":
    main()
