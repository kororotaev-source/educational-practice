import storage
from datetime import datetime

inventory = storage.load_data()
FIELDS = ["type", "name", "room", "status"]          # поля, которые вводит пользователь
SEARCHABLE = ["id"] + FIELDS                         # поля, по которым можно искать
NOT_FOUND = {"id": "id", "type": "типа", "name": "названия", "room": "кабинета", "status": "статуса"}
STATUSES = ["исправно", "требует ремонта", "списано"]
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
    elif key_type == "search_key":
        if value in ['1', '2', '3', '4', '5']:
            return ["id", "type", "name", "room", "status"][int(value) - 1]
    elif key_type == "change_key":
        if value in ['2', '3', '4', '5']:
            return ["type", "name", "room", "status"][int(value) - 2]
    return value

def check_field(value, field=''):
    value = str(value).strip()
    if not value:
        return f"Ошибка: поле '{field}' не может быть пустым."
    if len(value) < 2:
        return f"Ошибка: значение {field} должно быть не менее 2 символов"
    if field == "status" and value not in STATUSES:
        return "Ошибка: неверное состояние (должно быть: исправно, требует ремонта, списано)."
    return "Успех"

def val_add_item(item):
    for field in ["type", "name", "room", "status"]:
        if not str(item.get(field, "")).strip():
            return False, f"Ошибка: поле '{field}' не может быть пустым."
        if len(str(item.get(field, ""))) < 2:
            return False, f"Ошибка: значение {field} должно быть не менее 2 символов"
        
    if item["status"] not in STATUSES:
        return False, "Ошибка: неверное состояние (должно быть: исправно, требует ремонта, списано)."
        
    if find_by_id(item["id"]) is not None:
        return False, f"Ошибка: оборудование с номером {item['id']} уже существует."
    
    return True, "Успех, итем добавлен"

def add_item(item):
    item = {
        "id": (max([x["id"] for x in inventory]) + 1) if inventory else 1,
        "type": item['type'], 
        "name": item['name'],
        "room": item['room'],
        "status": item['status'],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    ok, text = val_add_item(item)

    if ok:
        inventory.append(item)
        storage.save_data(inventory)
        return text
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

def change(id, type, request):
    if find_by_id(id) is None:
        return "Ошибка. Неверный ID, попробуйте ещё раз"
    if not type:
        return "Ошибка. Пустое поле, попробуйте ещё раз"
    if type not in FIELDS:
        return "Ошибка. Неверный ключ, попробуйте ещё раз (2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние)"
    if type == "status" and request not in STATUSES:
        return "Ошибка: неверное состояние (должно быть: исправно, требует ремонта, списано)."
    if not request:
        return "Ошибка. Пустое значение, попробуйте ещё раз"
    item = find_by_id(id)
    item[type] = request
    storage.save_data(inventory)
    return "Успешно изменено"

def remove(id):
    item = find_by_id(id)
    if item is None:
        return "Ошибка: такого номера нет"
    inventory.remove(item)
    storage.save_data(inventory)
    return "Успешно удалено"