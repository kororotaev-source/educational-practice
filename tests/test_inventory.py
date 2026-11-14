import pytest

import inventory
import storage


def make(i, **extra):
    item = {"id": i, "type": "ПК", "name": f"Test {i}", "room": "101",
            "status": "исправно", "created_at": "2026-01-01 00:00"}
    item.update(extra)
    return item


def is_error(result):
    """add_item / change / remove возвращают текст; ошибка - это текст, начинающийся с 'Ошибка'."""
    return isinstance(result, str) and result.startswith("Ошибка")


@pytest.fixture(autouse=True)
def setup_test_data(monkeypatch):
    monkeypatch.setattr(inventory, "inventory", [make(1)])


def test_add_item_success():
    # комната из одного символа - допустима; id присваивается автоматически
    result = inventory.add_item({"type": "Монитор", "name": "Samsung 24", "room": "5", "status": "исправно"})
    assert not is_error(result)
    items = inventory.get()
    assert len(items) == 2
    assert items[1]["id"] == 2
    assert items[1]["room"] == "5"
    assert items[1]["created_at"]  # проставляется автоматически


def test_add_item_ignores_given_id_and_never_duplicates():
    # id всегда выдаёт сама программа (max + 1), поэтому дубликата не будет
    result = inventory.add_item({"id": 1, "type": "Принтер", "name": "HP", "room": "103", "status": "исправно"})
    assert not is_error(result)
    assert [i["id"] for i in inventory.get()] == [1, 2]


def test_add_item_empty_fields():
    result = inventory.add_item({"id": 3, "type": "", "name": "Без имени", "room": "101", "status": "исправно"})
    assert is_error(result)
    assert len(inventory.get()) == 1


def test_add_item_invalid_status():
    result = inventory.add_item({"id": 3, "type": "ПК", "name": "Test", "room": "101", "status": "сломан"})
    assert is_error(result)
    assert len(inventory.get()) == 1


def test_add_item_status_number_and_spaces():
    # цифра 1-3 превращается в статус через normalize (его вызывает main.py); пробелы по краям убираются
    assert [inventory.normalize(d, "status") for d in "123"] == inventory.STATUSES
    result = inventory.add_item({"type": " ПК ", "name": " Test ", "room": "101",
                                 "status": inventory.normalize("2", "status")})
    assert not is_error(result)
    added = inventory.get()[-1]
    assert (added["type"], added["name"], added["status"]) == ("ПК", "Test", "требует ремонта")


def test_new_id_is_max_plus_one_after_removal():
    inventory.inventory[:] = [make(1), make(2), make(3)]
    inventory.remove("2")
    inventory.add_item({"type": "ПК", "name": "Test", "room": "101", "status": "исправно"})
    ids = [i["id"] for i in inventory.get()]
    assert ids == [1, 3, 4]
    assert len(ids) == len(set(ids))


def test_remove_by_id_not_by_position():
    inventory.inventory[:] = [make(1), make(2), make(3), make(4), make(5)]
    inventory.remove("2")
    result = inventory.remove("4")
    assert not is_error(result)
    assert [i["id"] for i in inventory.get()] == [1, 3, 5]


def test_remove_not_found():
    result = inventory.remove("99")
    assert is_error(result)
    assert len(inventory.get()) == 1


def test_change_after_removal_hits_right_item():
    inventory.inventory[:] = [make(1), make(2), make(3)]
    inventory.remove("1")
    result = inventory.change("3", "name", "Новое имя")
    assert not is_error(result)
    assert inventory.find_by_id(3)["name"] == "Новое имя"
    assert inventory.find_by_id(2)["name"] == "Test 2"


def test_change_validates_value():
    assert is_error(inventory.change("1", "status", "фыв"))
    assert is_error(inventory.change("1", "name", " "))
    assert is_error(inventory.change("1", "name", "X"))       # у названия минимум 2 символа
    assert not is_error(inventory.change("1", "room", "7"))   # а кабинет может быть из одного
    assert inventory.find_by_id(1)["status"] == "исправно"
    assert inventory.find_by_id(1)["name"] == "Test 1"
    assert inventory.find_by_id(1)["room"] == "7"


def test_change_cannot_edit_id():
    result = inventory.change("1", "id", "5")
    assert is_error(result)
    assert inventory.find_by_id(1) is not None


def test_change_unknown_id_and_key():
    assert is_error(inventory.change("42", "name", "Новое"))
    assert is_error(inventory.change("1", "color", "Красный"))


def test_search_by_id_matches_part_of_number():
    # поиск по подстроке - так задумано (в том числе для №)
    inventory.inventory[:] = [make(1), make(10), make(11), make(2)]
    ok, found = inventory.search("id", "1")
    assert ok and [i["id"] for i in found] == [1, 10, 11]


def test_search_is_case_insensitive():
    inventory.inventory[:] = [make(1, name="Samsung")]
    ok, found = inventory.search("name", "samsung")
    assert ok and len(found) == 1


def test_search_not_found_and_bad_key():
    assert inventory.search("name", "нет такого")[0] is False
    assert inventory.search("color", "x")[0] is False
    assert inventory.search("", "x")[0] is False


def test_changes_are_saved_to_file():
    inventory.add_item({"type": "ПК", "name": "Saved", "room": "101", "status": "исправно"})
    saved = storage.load_data()
    assert [i["id"] for i in saved] == [1, 2]