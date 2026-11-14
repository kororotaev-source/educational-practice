import storage
from datetime import datetime

inventory = []                                        # заполняется в load() при старте программы
FIELDS = ["type", "name", "room", "status"]          # поля, которые вводит пользователь
SEARCHABLE = ["id"] + FIELDS                         # поля, по которым можно искать
NOT_FOUND = {"id": "id", "type": "типа", "name": "названия", "room": "кабинета", "status": "статуса"}
STATUSES = ["исправно", "требует ремонта", "списано"]
MIN_LENGTH = {"room": 1}                             # минимальная длина значения (у остальных полей - 2)
def load():
    inventory[:] = storage.load_data()

def get():
    return inventory

def find_by_id(item_id):
    for item in inventory:
        if str(item["id"]) == str(item_id).strip():
            return item
    return None

def normalize(value, key_type):
    if key_type == "status":
        if value in ['1', '2', '3']:
            return STATUSES[int(value) - 1]
    return value

def check_field(value, field=''):
    """Возвращает текст ошибки или None, если значение допустимо."""
    value = str(value).strip()
    min_length = MIN_LENGTH.get(field, 2)
    if not value:
        return f"Ошибка: поле '{field}' не может быть пустым."
    if len(value) < min_length:
        return f"Ошибка: значение {field} должно быть не менее {min_length} символов"
    if field == "status" and value not in STATUSES:
        return "Ошибка: неверное состояние (должно быть: исправно, требует ремонта, списано)."
    return None

def val_add_item(item):
    for field in FIELDS:
        error = check_field(item.get(field, ""), field)
        if error:
            return False, error

    if find_by_id(item["id"]) is not None:
        return False, f"Ошибка: оборудование с номером {item['id']} уже существует."

    return True, "Успех, итем добавлен"

def add_item(item):
    item = {
        "id": (max([x["id"] for x in inventory]) + 1) if inventory else 1,
        "type": item['type'].strip(),
        "name": item['name'].strip(),
        "room": item['room'].strip(),
        "status": item['status'].strip(),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ok, text = val_add_item(item)

    if ok:
        inventory.append(item)
        storage.save_data(inventory)
    return text

def search(key, request):
    finds = []
    if not key or not request:
        return False, "Ошибка. Пустое поле, попробуйте ещё раз"
    if key not in SEARCHABLE:
        return False, "Ошибка. Неверный ключ, попробуйте ещё раз (1:№, 2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние)"
    for x in range(len(inventory)):
        if request.lower() in str(inventory[x][key]).lower():
            finds.append(inventory[x])
    if finds:
        return True, finds
    return False, f"Такого {NOT_FOUND[key]} не существует"

def change(item_id, field, request):
    if find_by_id(item_id) is None:
        return "Ошибка. Неверный ID, попробуйте ещё раз"
    if not field:
        return "Ошибка. Пустое поле, попробуйте ещё раз"
    if field not in FIELDS:
        return "Ошибка. Неверный ключ, попробуйте ещё раз (2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние)"
    request = str(request).strip()
    error = check_field(request, field)
    if error:
        return error
    find_by_id(item_id)[field] = request
    storage.save_data(inventory)
    return "Успешно изменено"

def remove(item_id):
    item = find_by_id(item_id)
    if item is None:
        return "Ошибка: такого номера нет"
    inventory.remove(item)
    storage.save_data(inventory)
    return "Успешно удалено"