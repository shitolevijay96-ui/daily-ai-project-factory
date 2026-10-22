import os
import shutil
import pytest
from main import create_note, search_notes, NOTE_DIR

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists(NOTE_DIR):
        shutil.rmtree(NOTE_DIR)

def test_create_note():
    path = create_note("Test Title", "This is a test body")
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        assert "# Test Title" in content
        assert "This is a test body" in content

def test_search_notes():
    create_note("Python Guide", "Learning python is fun and useful.")
    create_note("Cooking Recipe", "How to bake a cake.")
    
    matches = search_notes("python")
    assert len(matches) == 1
    assert "python_guide.md" in matches[0]
