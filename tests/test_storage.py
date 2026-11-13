import json

import pytest

import storage


def test_missing_file_is_created_empty():
    assert not storage.DATA_FILE.exists()
    assert storage.load_data() == []
    assert storage.DATA_FILE.exists()


def test_save_and_load_roundtrip():
    data = [{"id": 1, "type": "ПК", "name": "Тест", "room": "101", "status": "исправно"}]
    storage.save_data(data)
    assert storage.load_data() == data


def test_file_format_has_version_and_items():
    storage.save_data([{"id": 1}])
    raw = json.loads(storage.DATA_FILE.read_text(encoding="utf-8"))
    assert raw == {"version": 1, "items": [{"id": 1}]}


def test_russian_text_is_readable_in_file():
    storage.save_data([{"id": 1, "type": "Принтер"}])
    assert "Принтер" in storage.DATA_FILE.read_text(encoding="utf-8")


def test_blank_file_gives_empty_list():
    storage.DATA_FILE.parent.mkdir(parents=True)
    storage.DATA_FILE.write_text("\r\n", encoding="utf-8")
    assert storage.load_data() == []


def test_corrupted_file_raises_and_is_not_overwritten():
    storage.DATA_FILE.parent.mkdir(parents=True)
    broken = '{"version": 1, "items": [oops'
    storage.DATA_FILE.write_text(broken, encoding="utf-8")
    with pytest.raises(storage.StorageError):
        storage.load_data()
    assert storage.DATA_FILE.read_text(encoding="utf-8") == broken


def test_unknown_structure_raises():
    storage.DATA_FILE.parent.mkdir(parents=True)
    storage.DATA_FILE.write_text('"просто строка"', encoding="utf-8")
    with pytest.raises(storage.StorageError):
        storage.load_data()


def test_old_plain_list_format_is_still_read():
    storage.DATA_FILE.parent.mkdir(parents=True)
    storage.DATA_FILE.write_text('[{"id": 1}]', encoding="utf-8")
    assert storage.load_data() == [{"id": 1}]


def test_no_temp_files_left_behind():
    storage.save_data([])
    assert [p.name for p in storage.DATA_FILE.parent.iterdir()] == ["inventory.json"]
