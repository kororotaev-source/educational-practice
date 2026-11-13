import storage

inventory = storage.load_data()

def load():
    inventory[:] = storage.load_data()

def get():
    return inventory

def find_by_id(item_id):
    for item in inventory:
        if str(item["id"]) == str(item_id).strip():
            return item
    return None

def val_add_item(item):
    for field in ["type", "name", "room", "status"]:
        if not str(item.get(field, "")).strip():
            return False, f"Ошибка: поле '{field}' не может быть пустым."
        if len(str(item.get(field, ""))) < 2:
            return False, f"Ошибка: значение {field} должно быть не менее 2 символов"
        
    if item["status"] not in ["исправно", "требует ремонта", "списано"]:
        return False, "Ошибка: неверное состояние (должно быть: исправно, требует ремонта, списано)."
        
    if find_by_id(item["id"]) is not None:
        return False, f"Ошибка: оборудование с номером {item['id']} уже существует."
    
    return True, "Успех, итем добавлен"

def add_item(item):
    ok, text = val_add_item(item)

    if ok:
        inventory.append(item)
        storage.save_data(inventory)
        return True, text
    return False, text

def search(type, request):
    types = {"id": "id", "type": "типа", "name": "названия", "room": "кабинета", "status": "статуса"}
    finds = []
    if not type:
        return False, "Ошибка. Пустое поле, попробуйте ещё раз"
    if type not in ['id','type','name','room','status']:
        return False, "Ошибка. Неверный ключ, попробуйте ещё раз (1:№, 2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние)"
    for x in range(len(inventory)):
        if request.lower() in str(inventory[x][type]).lower():
            finds.append(inventory[x])
    if finds:
        return True, finds
    return False, f"Такого {types[type]} не существует"

def change(id, type, request):
    er = 0
    if find_by_id(id) is None:
        return False, "Ошибка. Неверный ID, попробуйте ещё раз"
    if not type:
        return False, "Ошибка. Пустое поле, попробуйте ещё раз"
    if type not in ['id','type','name','room','status']:
        return False, "Ошибка. Неверный ключ, попробуйте ещё раз (1:№, 2:Тип, 3:Наименование, 4:Кабинет, 5:Состояние)"
    item = find_by_id(id)
    item[type] = request
    storage.save_data(inventory)
    return True, "Успешно изменено"

def remove(id):
    item = find_by_id(id)
    if item is None:
        return False, "Ошибка: такого номера нет"
    inventory.remove(item)
    storage.save_data(inventory)
    return True, "Успешно удалено"