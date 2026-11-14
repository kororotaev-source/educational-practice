import contextlib
import json
import os
import tempfile
from pathlib import Path

# Файл лежит рядом с программой, независимо от того, откуда её запустили
DATA_FILE = Path(__file__).parent / "data" / "inventory.json"
FORMAT_VERSION = 1
REQUIRED_FIELDS = ["type", "name", "room", "status", "created_at"]   # обязательные текстовые поля записи


class StorageError(Exception):
    """Ошибка чтения или записи файла данных."""
 
 
def save_data(data):
    """Записывает {"version": 1, "items": [...]} в JSON.
    Сначала пишет во временный файл, потом заменяет основной,
    поэтому сбой посреди записи не уничтожит старые данные."""
    payload = {"version": FORMAT_VERSION, "items": data}
    tmp_path = None
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=DATA_FILE.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        os.replace(tmp_path, DATA_FILE)
    except (OSError, TypeError, ValueError) as e:
        if tmp_path:
            with contextlib.suppress(OSError):
                os.remove(tmp_path)
        raise StorageError(f"не удалось сохранить файл {DATA_FILE}: {e}") from e
 
 
def _problem_with(item):
    """Возвращает описание проблемы с записью или None, если запись в порядке."""
    if not isinstance(item, dict):
        return "это не запись"
    item_id = item.get("id")
    if not isinstance(item_id, int) or isinstance(item_id, bool):
        return "поле 'id' должно быть целым числом"
    for field in REQUIRED_FIELDS:
        if not isinstance(item.get(field), str) or not item[field].strip():
            return f"поле '{field}' отсутствует или пустое"
    return None


def load_data():
    """Читает список записей из JSON.
 
    - файла нет            -> создаёт пустой, возвращает []
    - файл пустой          -> возвращает []
    - файл повреждён       -> StorageError, файл НЕ изменяется
    Старый формат (просто список) тоже читается."""
    if not DATA_FILE.exists():
        save_data([])
        return []
 
    try:
        text = DATA_FILE.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as e:
        raise StorageError(f"не удалось прочитать файл {DATA_FILE}: {e}") from e
 
    if not text.strip():
        save_data([])
        return []
 
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise StorageError(
            f"файл {DATA_FILE} повреждён (строка {e.lineno}, позиция {e.colno}: {e.msg})"
        ) from e
 
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        items = data["items"]
    elif isinstance(data, list):
        items = data
    else:
        raise StorageError(f"неизвестный формат файла {DATA_FILE}")
 
    seen_ids = set()
    for number, item in enumerate(items, start=1):
        problem = _problem_with(item)
        if problem is None and item["id"] in seen_ids:
            problem = f"номер {item['id']} встречается дважды"
        if problem:
            raise StorageError(f"в файле {DATA_FILE} запись №{number} неверна: {problem}")
        seen_ids.add(item["id"])
    return items