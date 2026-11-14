import pytest

import inventory
import storage


def make(i, **extra):
    item = {"id": i, "type": "ПК", "name": f"Test {i}", "room": "101",
            "status": "исправно", "created_at": "2026-01-01 00:00"}
    item.update(extra)
    return item


@pytest.fixture(autouse=True)
def setup_test_data(monkeypatch):
    monkeypatch.setattr(inventory, "inventory", [make(1)])


def test_add_item_success():
    ok = inventory.add_item({"type": "Монитор", "name": "Samsung 24", "room": "102", "status": "исправно"})
    assert ok is True
    items = inventory.get()
    assert len(items) == 2
    assert items[1]["id"] == 2
    assert items[1]["created_at"]  # проставляется автоматически


def test_add_item_duplicate_id():
    ok = inventory.add_item({"id": 1, "type": "Принтер", "name": "HP", "room": "103", "status": "исправно"})
    assert ok != 'Успех, итем добавлен'
    assert len(inventory.get()) == 1


def test_add_item_empty_fields():
    ok = inventory.add_item({"id": 3, "type": "", "name": "Без имени", "room": "101", "status": "исправно"})
    assert ok is False


def test_add_item_invalid_status():
    ok = inventory.add_item({"id": 3, "type": "ПК", "name": "Test", "room": "101", "status": "сломан"})
    assert ok is False


def test_add_item_status_number_and_case():
    ok = inventory.add_item({"id": 3, "type": "ПК", "name": "Test", "room": "101", "status": "2"})
    assert ok and inventory.find_by_id(3)["status"] == "требует ремонта"
    ok = inventory.add_item({"id": 4, "type": "ПК", "name": "Test", "room": "101", "status": "Исправно"})
    assert ok and inventory.find_by_id(4)["status"] == "исправно"


def test_next_id_after_removal():
    inventory.inventory[:] = [make(1), make(2), make(3)]
    inventory.remove("3")
    assert inventory.next_id() == 3
    assert inventory.next_id() > max(i["id"] for i in inventory.get())


def test_remove_by_id_not_by_position():
    inventory.inventory[:] = [make(1), make(2), make(3), make(4), make(5)]
    inventory.remove("2")
    ok= inventory.remove("4")
    assert ok
    assert [i["id"] for i in inventory.get()] == [1, 3, 5]


def test_remove_not_found():
    ok = inventory.remove("99")
    assert ok is False
    assert len(inventory.get()) == 1


def test_change_after_removal_hits_right_item():
    inventory.inventory[:] = [make(1), make(2), make(3)]
    inventory.remove("1")
    ok = inventory.change("3", "name", "Новое имя")
    assert ok
    assert inventory.find_by_id(3)["name"] == "Новое имя"
    assert inventory.find_by_id(2)["name"] == "Test 2"


def test_change_validates_value():
    ok = inventory.change("1", "status", "фыв")
    assert ok is False
    ok = inventory.change("1", "name", " ")
    assert ok is False
    assert inventory.find_by_id(1)["status"] == "исправно"
    assert inventory.find_by_id(1)["name"] == "Test 1"


def test_change_cannot_edit_id():
    ok = inventory.change("1", "id", "5")
    assert ok is False
    assert inventory.find_by_id(1) is not None


def test_change_unknown_id_and_key():
    assert inventory.change("42", "name", "Новое")[0] is False
    assert inventory.change("1", "color", "Красный")[0] is False


def test_search_id_is_exact():
    inventory.inventory[:] = [make(1), make(10), make(11)]
    ok, found = inventory.search("id", "1")
    assert ok and [i["id"] for i in found] == [1]


def test_search_is_case_insensitive():
    inventory.inventory[:] = [make(1, name="Samsung")]
    ok, found = inventory.search("name", "samsung")
    assert ok and len(found) == 1


def test_search_not_found_and_bad_key():
    assert inventory.search("name", "нет такого")[0] is False
    assert inventory.search("color", "x")[0] is False
    assert inventory.search("", "x")[0] is False


def test_changes_are_saved_to_file():
    inventory.add_item({"id": 2, "type": "ПК", "name": "Saved", "room": "101", "status": "исправно"})
    saved = storage.load_data()
    assert [i["id"] for i in saved] == [1, 2]
