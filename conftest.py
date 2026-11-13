import sys
from pathlib import Path
 
import pytest
 
sys.path.insert(0, str(Path(__file__).parent))
 
import storage  # noqa: E402
 
@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    """Тесты пишут во временную папку и никогда не трогают настоящий data/inventory.json."""
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "data" / "inventory.json")
 